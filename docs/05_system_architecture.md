# System Architecture

## End-To-End Blocks

```text
+-------------+      +-------------+      +--------+      +-------------+
| ESP32-CAM   | ---> | Packetiser  | ---> | CC1101 | ---> | RF channel  |
| OV2640 JPEG |      | CRC/seq/sync|      | FSK    |      | or bench RF |
+-------------+      +-------------+      +--------+      +-------------+
                                                                  |
                                                                  v
+-------------+      +-------------+      +-------------+      +--------+
| JPEG/viewer | <--- | Packet      | <--- | GNU Radio   | <--- | RTL-SDR|
| output      |      | decoder     |      | demod chain |      | IQ     |
+-------------+      +-------------+      +-------------+      +--------+
```

## Transmit Side

The ESP32-CAM captures a small image payload, initially a tiny JPEG or test fixture. Firmware splits bytes into packets with headers, payload length, sequence information, and CRC. The CC1101 sends those packets using a conservative FSK/GFSK configuration.

## Receive Side

The Nooelec NESDR records IQ samples. GNU Radio performs frequency selection, filtering, demodulation, clock recovery, and bit slicing. Python searches for sync, validates packet CRCs, tracks missing packets, and reconstructs complete image frames.

## Development Order

1. Receive-only SDR operation.
2. Python packet simulation.
3. CC1101 known text packets.
4. Offline SDR demod of known packets.
5. Still image transport.
6. Slow repeated frame stream.

## Key Interfaces

- Packet byte format: documented in `docs/06_packet_protocol.md`.
- CC1101 settings: documented in `docs/08_esp32cam_cc1101_design.md`.
- GNU Radio receiver chain: documented in `docs/07_gnuradio_receiver_design.md`.
- Measurement plan: documented in `docs/09_link_budget_and_measurements.md`.

