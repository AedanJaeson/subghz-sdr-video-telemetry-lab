# Project Overview

This lab builds a guided path from basic SDR operation to an end-to-end low-rate digital image telemetry link:

```text
ESP32-CAM -> packetised image bytes -> CC1101 FSK/GFSK -> RF/bench link
          -> RTL-SDR IQ capture -> GNU Radio/Python demod -> packet decode
          -> frame reconstruction
```

The project is intentionally staged. Receive-only skills come first, then simulation, then controlled low-power transmit work only after legal and hardware checks are complete.

## Design Constraints

- Public-safe documentation.
- No high-power transmit tasks.
- No protected-band transmit tasks.
- No malicious, surveillance, jamming, spoofing, or interception objectives.
- Small, evidence-oriented milestones that produce screenshots, logs, plots, or written notes.

## MVP Outcome

The first meaningful end-to-end outcome is not live video. The MVP is a single tiny image or JPEG-like payload split into packets, transmitted at low power on a legal band, received by SDR, decoded, and reconstructed with measured packet loss.

