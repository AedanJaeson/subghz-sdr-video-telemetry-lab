# Packet Protocol

This page documents the current **MVP byte-packet format** used by the Python receiver tooling.

The protocol is deliberately small, boring, and inspectable. It is not a video codec and it is not an RF waveform. It is the byte format that sits above the FSK/GFSK bitstream once the receiver has recovered bytes.

## MVP Format

Multi-byte fields are **big-endian**.

| Field | Size | Purpose |
| --- | ---: | --- |
| Sync word | 2 bytes | Marks the start of a packet. Current value: `0xA55A`. |
| Protocol version | 1 byte | Current value: `1`. Allows future format changes. |
| Flags | 1 byte | Reserved for future use. Current default: `0`. |
| Frame ID | 2 bytes | Identifies the image/frame or test payload group. |
| Packet ID | 2 bytes | Identifies this packet within the frame. Starts at `0`. |
| Total packets | 2 bytes | Number of packets required to reconstruct the frame. |
| Payload length | 2 bytes | Number of valid payload bytes in this packet. |
| Payload | 0-48 bytes | Image bytes or test bytes. MVP default limit: 48 bytes. |
| CRC | 2 bytes | CRC-16/CCITT-FALSE over all bytes from sync word through payload. |

Python implementation:

```text
receiver/python/subghz_lab/packet.py
```

Test suite:

```text
receiver/python/tests/test_packet.py
```

## Why 48 Payload Bytes?

The payload limit is conservative on purpose. The early project goal is not throughput. The goal is to make packets short enough to inspect, recover, corrupt, test, and reason about while the RF/DSP chain is still being learned.

With the current header and CRC, a 48-byte payload creates a 62-byte encoded packet:

```text
12-byte header + 48-byte payload + 2-byte CRC = 62 bytes
```

That keeps the MVP packet small and friendly for CC1101-style experiments, serial logs, hexdumps, and recorded-IQ debugging.

## CRC Decision

Current CRC:

```text
CRC-16/CCITT-FALSE
Polynomial: 0x1021
Initial value: 0xFFFF
No reflection
No final XOR
Reference vector: b"123456789" -> 0x29B1
```

The CRC is for corruption detection only. It is not encryption, authentication, whitening, FEC, or interleaving.

## Preamble vs Sync

The **preamble** is a PHY/radio concern. It helps receiver settling and clock recovery.

The **sync word** is a packet concern. It marks where the decoded byte packet begins.

For the MVP Python packet tools, only the sync word appears in the encoded packet bytes. Radio/PHY preamble handling remains part of the firmware/CC1101/GNU Radio layer.

## Current Open Decisions

These are intentionally deferred until packet recovery from recorded IQ is working:

- Whitening.
- FEC.
- Interleaving.
- Larger payload sizes.
- More advanced image-frame metadata.
- Whether the firmware packetiser mirrors this exact format or uses a smaller transitional test format first.

## Local Test Command

From the repository root on Windows PowerShell:

```powershell
cd receiver\python
python -m pip install -r requirements.txt
pytest
```

Expected result after this MVP change:

```text
9 passed
```
