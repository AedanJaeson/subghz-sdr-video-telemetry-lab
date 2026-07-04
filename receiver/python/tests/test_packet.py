import pytest

from subghz_lab.packet import (
    CRCError,
    PacketParseError,
    ProtocolError,
    crc16_ccitt_false,
    deframe_payload,
    encode_packet,
    fragment_payload,
    parse_packet,
)


def test_crc16_ccitt_false_reference_vector():
    assert crc16_ccitt_false(b"123456789") == 0x29B1


def test_encode_parse_round_trip_single_packet():
    raw = encode_packet(b"SUBGHZ_LAB_TEST_0", frame_id=7)
    packet = parse_packet(raw)

    assert packet.version == 1
    assert packet.frame_id == 7
    assert packet.packet_id == 0
    assert packet.total_packets == 1
    assert packet.payload == b"SUBGHZ_LAB_TEST_0"
    assert packet.is_single_packet_frame()


def test_crc_error_when_payload_is_corrupted():
    raw = bytearray(encode_packet(b"hello", frame_id=1))
    raw[-3] ^= 0x01

    with pytest.raises(CRCError):
        parse_packet(raw)


def test_sync_error_is_rejected():
    raw = bytearray(encode_packet(b"hello"))
    raw[0] = 0x00

    with pytest.raises(PacketParseError, match="sync word mismatch"):
        parse_packet(raw)


def test_payload_length_mismatch_is_rejected():
    raw = encode_packet(b"hello") + b"extra"

    with pytest.raises(PacketParseError, match="length mismatch"):
        parse_packet(raw)


def test_payload_limit_is_enforced():
    with pytest.raises(ProtocolError, match="max is 4 bytes"):
        encode_packet(b"12345", max_payload_bytes=4)


def test_fragment_and_deframe_payload_round_trip_out_of_order():
    payload = b"abcdefghijklmnopqrstuvwxyz"
    encoded = fragment_payload(payload, frame_id=42, max_payload_bytes=8)
    parsed = [parse_packet(raw) for raw in encoded]

    assert len(parsed) == 4
    assert [packet.packet_id for packet in parsed] == [0, 1, 2, 3]
    assert deframe_payload(reversed(parsed)) == payload


def test_deframe_rejects_missing_packet():
    payload = b"abcdefghijklmnopqrstuvwxyz"
    parsed = [parse_packet(raw) for raw in fragment_payload(payload, frame_id=42, max_payload_bytes=8)]

    with pytest.raises(ProtocolError, match="missing packet_id"):
        deframe_payload(parsed[:-1])


def test_deframe_rejects_duplicate_packet_id():
    first = parse_packet(encode_packet(b"a", frame_id=1, packet_id=0, total_packets=1))

    with pytest.raises(ProtocolError, match="duplicate packet_id"):
        deframe_payload([first, first])
