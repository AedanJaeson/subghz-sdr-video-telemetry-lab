"""MVP packet protocol helpers.

This module deliberately stays offline and public-safe: it turns bytes into a
small framed packet format and parses those packets back into Python objects.
It does not transmit, tune a radio, or control SDR hardware.

The CC1101/RadioLib path can carry small byte arrays, so the MVP keeps packets
short and easy to inspect while the receiver DSP is still being learned.
"""

from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Iterable

SYNC_WORD = 0xA55A
VERSION = 1
MAX_PAYLOAD_BYTES = 48
_HEADER = struct.Struct(">HBBHHHH")
_CRC = struct.Struct(">H")


class ProtocolError(ValueError):
    """Base class for packet protocol errors."""


class PacketParseError(ProtocolError):
    """Raised when bytes cannot be parsed as an MVP packet."""


class CRCError(PacketParseError):
    """Raised when the received CRC does not match the calculated CRC."""


@dataclass(frozen=True)
class Packet:
    """Parsed MVP packet.

    Fields are intentionally small and explicit so they can later be mirrored in
    firmware without dragging in a complicated serialization dependency.
    """

    version: int
    flags: int
    frame_id: int
    packet_id: int
    total_packets: int
    payload: bytes
    crc: int

    @property
    def payload_length(self) -> int:
        return len(self.payload)

    def is_single_packet_frame(self) -> bool:
        return self.packet_id == 0 and self.total_packets == 1


def crc16_ccitt_false(data: bytes, *, init: int = 0xFFFF) -> int:
    """Return CRC-16/CCITT-FALSE for *data*.

    Parameters:
        data: Bytes to check.
        init: Initial CRC value. CCITT-FALSE uses 0xFFFF.

    Polynomial: 0x1021. No reflection. No final XOR.
    Reference vector: b"123456789" -> 0x29B1.
    """

    crc = init & 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def _require_uint(name: str, value: int, max_value: int) -> None:
    if not isinstance(value, int):
        raise ProtocolError(f"{name} must be an int")
    if not 0 <= value <= max_value:
        raise ProtocolError(f"{name} must be in range 0..{max_value}")


def encode_packet(
    payload: bytes | bytearray | memoryview,
    *,
    frame_id: int = 0,
    packet_id: int = 0,
    total_packets: int = 1,
    flags: int = 0,
    version: int = VERSION,
    max_payload_bytes: int = MAX_PAYLOAD_BYTES,
) -> bytes:
    """Encode one packet.

    The returned bytes are:

    ``sync | version | flags | frame_id | packet_id | total_packets | payload_len | payload | crc``

    Multi-byte fields are big-endian so hex dumps read consistently across
    Python, firmware, and documentation.
    """

    payload_bytes = bytes(payload)

    _require_uint("version", version, 0xFF)
    _require_uint("flags", flags, 0xFF)
    _require_uint("frame_id", frame_id, 0xFFFF)
    _require_uint("packet_id", packet_id, 0xFFFF)
    _require_uint("total_packets", total_packets, 0xFFFF)
    _require_uint("max_payload_bytes", max_payload_bytes, 0xFFFF)

    if total_packets < 1:
        raise ProtocolError("total_packets must be at least 1")
    if packet_id >= total_packets:
        raise ProtocolError("packet_id must be less than total_packets")
    if len(payload_bytes) > max_payload_bytes:
        raise ProtocolError(
            f"payload is {len(payload_bytes)} bytes; max is {max_payload_bytes} bytes"
        )

    header = _HEADER.pack(
        SYNC_WORD,
        version,
        flags,
        frame_id,
        packet_id,
        total_packets,
        len(payload_bytes),
    )
    body = header + payload_bytes
    crc = crc16_ccitt_false(body)
    return body + _CRC.pack(crc)


def parse_packet(raw: bytes | bytearray | memoryview, *, require_version: int = VERSION) -> Packet:
    """Parse a complete encoded packet and validate its CRC."""

    packet = bytes(raw)
    min_len = _HEADER.size + _CRC.size
    if len(packet) < min_len:
        raise PacketParseError(f"packet too short: {len(packet)} bytes")

    header = packet[: _HEADER.size]
    sync_word, version, flags, frame_id, packet_id, total_packets, payload_len = _HEADER.unpack(header)

    if sync_word != SYNC_WORD:
        raise PacketParseError(f"sync word mismatch: got 0x{sync_word:04X}")
    if version != require_version:
        raise PacketParseError(f"unsupported protocol version: {version}")
    if total_packets < 1:
        raise PacketParseError("total_packets must be at least 1")
    if packet_id >= total_packets:
        raise PacketParseError("packet_id must be less than total_packets")

    expected_len = _HEADER.size + payload_len + _CRC.size
    if len(packet) != expected_len:
        raise PacketParseError(f"length mismatch: header says {expected_len} bytes, got {len(packet)}")

    payload_start = _HEADER.size
    payload_end = payload_start + payload_len
    payload = packet[payload_start:payload_end]
    (received_crc,) = _CRC.unpack(packet[payload_end:payload_end + _CRC.size])
    calculated_crc = crc16_ccitt_false(packet[:payload_end])

    if received_crc != calculated_crc:
        raise CRCError(
            f"CRC mismatch: received 0x{received_crc:04X}, calculated 0x{calculated_crc:04X}"
        )

    return Packet(
        version=version,
        flags=flags,
        frame_id=frame_id,
        packet_id=packet_id,
        total_packets=total_packets,
        payload=payload,
        crc=received_crc,
    )


def fragment_payload(
    payload: bytes | bytearray | memoryview,
    *,
    frame_id: int,
    max_payload_bytes: int = MAX_PAYLOAD_BYTES,
    flags: int = 0,
) -> list[bytes]:
    """Split a frame payload into encoded packets."""

    if max_payload_bytes < 1:
        raise ProtocolError("max_payload_bytes must be at least 1")

    payload_bytes = bytes(payload)
    chunks = [
        payload_bytes[index:index + max_payload_bytes]
        for index in range(0, len(payload_bytes), max_payload_bytes)
    ] or [b""]

    if len(chunks) > 0xFFFF:
        raise ProtocolError("payload requires too many packets")

    total_packets = len(chunks)
    return [
        encode_packet(
            chunk,
            frame_id=frame_id,
            packet_id=packet_id,
            total_packets=total_packets,
            flags=flags,
            max_payload_bytes=max_payload_bytes,
        )
        for packet_id, chunk in enumerate(chunks)
    ]


def deframe_payload(packets: Iterable[Packet]) -> bytes:
    """Reconstruct a frame payload from parsed packets.

    Packets may be passed in any order. Missing or duplicate packet IDs are
    rejected because silent image corruption is worse than a loud failure.
    """

    packet_list = list(packets)
    if not packet_list:
        raise ProtocolError("no packets supplied")

    frame_ids = {packet.frame_id for packet in packet_list}
    total_counts = {packet.total_packets for packet in packet_list}
    if len(frame_ids) != 1:
        raise ProtocolError(f"packets belong to multiple frames: {sorted(frame_ids)}")
    if len(total_counts) != 1:
        raise ProtocolError(f"packets disagree on total_packets: {sorted(total_counts)}")

    total_packets = packet_list[0].total_packets
    by_id: dict[int, Packet] = {}
    for packet in packet_list:
        if packet.packet_id in by_id:
            raise ProtocolError(f"duplicate packet_id: {packet.packet_id}")
        by_id[packet.packet_id] = packet

    missing = [packet_id for packet_id in range(total_packets) if packet_id not in by_id]
    if missing:
        raise ProtocolError(f"missing packet_id(s): {missing}")

    return b"".join(by_id[packet_id].payload for packet_id in range(total_packets))
