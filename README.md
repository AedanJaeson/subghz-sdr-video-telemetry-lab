# Sub-GHz SDR Video Telemetry Lab

Public-safe guided learning project for building a very low-rate digital image telemetry link from an ESP32-CAM through a CC1101 FSK/GFSK transmitter and an RTL-SDR receiver chain.

## What This Project Is

This is a communications engineering lab. It walks from receive-only SDR setup through packet framing, RF observation, digital link simulation, CC1101 experiments, GNU Radio/Python demodulation, and eventual JPEG frame reconstruction.

Target chain:

```text
ESP32-CAM OV2640
  -> JPEG capture
  -> packetiser: preamble, sync, sequence, CRC
  -> CC1101 low-power FSK/GFSK transmitter
  -> legal short-range RF path or controlled bench link
  -> Nooelec NESDR SMArt v5 RTL-SDR
  -> GNU Radio demodulation
  -> Python packet decoder
  -> JPEG frame reconstruction/viewer
```

## What This Project Is Not

This is not a Wi-Fi replacement, FPV system, surveillance tool, high-power transmitter, spectrum scanner for private content, jammer, spoofer, or operational radio product. Any transmit work is optional, low-power, legal-band, short-range, and gated by the RF safety checklist in [docs/04_rf_safety_and_legal_notes.md](docs/04_rf_safety_and_legal_notes.md).

## Why This Is A Good Learning Project

Video over CC1101 is technically weak as a product: the data rate is low, JPEG frames are fragile under packet loss, latency is high, and Wi-Fi/BLE/LoRa-style alternatives are usually more practical. That weakness is the point. It forces the engineering questions into the open: bit rate, deviation, occupied bandwidth, packet overhead, CRC failures, sync loss, goodput, antenna effects, and SNR.

## Hardware

- Nooelec NESDR SMArt v5 RTL-SDR kit
- ESP32-CAM board with OV2640 camera
- CC1101 module, ordered and expected by 2026-05-27; frequency variant to be verified before use
- USB data cable and optional powered USB hub
- Antennas appropriate to receive-only experiments and legal-band transmit tests
- Optional second CC1101 module for debug receive
- Optional attenuators, dummy load, shielding box, and SMA adapters for bench tests

## Software Stack

- SDR++ or SDR# for first receive checks
- RTL-SDR tools and drivers
- GNU Radio for receiver-chain experiments
- Python for packet simulation, decode tooling, plots, and tests
- PlatformIO for ESP32-CAM/CC1101 firmware

## Learning Phases

| Phase | Focus | Proof point |
| --- | --- | --- |
| 0 | Project setup and learning map | Repo scaffold, safety notes, guided issues |
| 1 | SDR bring-up | Nooelec detected, FM receive, first IQ capture workflow |
| 2 | Receive-only RF literacy | Waterfall interpretation and safe observations |
| 3 | Python digital link simulation | Packet framing, CRC, BER/PER intuition |
| 4 | CC1101 standalone packet link | Known text packets at legal low power |
| 5 | ESP32-CAM image capture | JPEG size and frame budget measurements |
| 6 | Packet protocol and frame transport | Host/firmware-compatible packet format |
| 7 | SDR/GNU Radio FSK receiver | Known packet recovered from SDR capture |
| 8 | End-to-end image link | Small image reconstructed from RF packets |
| 9 | Measurement and failure analysis | Link budget, distance, payload-size tradeoffs |
| 10 | Portfolio polish | Final report, diagrams, demo script, resume bullets |

## Safety And Legal Boundary

Receive-only work comes first. Before any RF transmission, complete the checklist in [docs/04_rf_safety_and_legal_notes.md](docs/04_rf_safety_and_legal_notes.md), verify current ACMA/LIPD rules, confirm the module frequency variant, use low power, and avoid protected services. Never connect a transmitter directly to the SDR input without suitable attenuation.

Note: legacy NOAA POES/APT weather-satellite reception is no longer a reliable beginner task because the POES constellation has been decommissioned. See [docs/weather_satellite_receive_alternatives.md](docs/weather_satellite_receive_alternatives.md) for the updated receive-only planning note.

While the CC1101 is in transit, the active path is pre-transmit work: SDR receive-only setup, IQ capture workflow, Python packet simulation, image serialization, and serial/file loopback. See [docs/pre_transmit_work_plan.md](docs/pre_transmit_work_plan.md).

## Current Status

| Area | Status |
| --- | --- |
| Repository scaffold | Complete |
| Learning path | Complete |
| RF safety checklist | Drafted |
| SDR bring-up | Not started |
| Packet simulation | Ready before RF hardware |
| Firmware | Not started |
| GNU Radio receiver | Not started |
| End-to-end link | Not started |

## Final Portfolio Outcomes

- A public, readable engineering lab showing RF, DSP, embedded, and packet-communications growth.
- Screenshots and captures showing SDR bring-up, spectra, waterfall interpretation, and demodulation progress.
- Packet protocol documentation with tests and failure analysis.
- Link-budget and measurement notes comparing simulation against real RF behaviour.
- Final engineering report and concise resume bullets.
