# Python Receiver Tools

Python receiver tooling decodes packet streams from GNU Radio output or offline captures after the RF/DSP layer has recovered bytes.

## Current MVP

The first implemented layer is the deterministic packet protocol helper:

```text
subghz_lab/packet.py
```

It provides:

- CRC-16/CCITT-FALSE calculation
- packet encoding
- packet parsing and CRC validation
- payload fragmentation into small packets
- frame payload reconstruction
- pytest coverage for normal and corrupted packets

## Local Setup

From this directory:

```powershell
python -m pip install -r requirements.txt
pytest
```

Expected result:

```text
9 passed
```

## Example Use

```python
from subghz_lab.packet import encode_packet, parse_packet

raw = encode_packet(b"SUBGHZ_LAB_TEST_0", frame_id=7)
packet = parse_packet(raw)

print(packet.frame_id)
print(packet.payload)
```

## Planned Modules

- packet synchronisation from a recovered byte stream
- CRC validation against bytes produced by GNU Radio
- frame reconstruction from packet files
- missing-packet reporting
- simple image viewer/export

## Development Boundary

This receiver package is offline tooling. It should not transmit RF, tune hardware, or control the CC1101. Live RF and GNU Radio work stays behind the safety checklist and measurement workflow documented in `docs/`.
