"""Small packet encode/decode demo.

Run from receiver/python:

    python examples/encode_decode_example.py
"""

from subghz_lab.packet import encode_packet, parse_packet


raw = encode_packet(b"SUBGHZ_LAB_TEST_0", frame_id=7)
packet = parse_packet(raw)

print(f"encoded packet length: {len(raw)} bytes")
print(f"encoded packet hex: {raw.hex(' ')}")
print(f"frame_id: {packet.frame_id}")
print(f"packet_id: {packet.packet_id}/{packet.total_packets - 1}")
print(f"payload: {packet.payload!r}")
print(f"crc: 0x{packet.crc:04X}")
