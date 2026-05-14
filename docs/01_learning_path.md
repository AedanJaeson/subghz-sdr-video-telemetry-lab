# Learning Path

This project is a guided communications engineering lab, not a rush to "video". Each phase proves one layer before adding the next.

## Before Touching Hardware

Learn and record the basics:

- What an SDR records: IQ samples, sample rate, center frequency, gain, and bandwidth.
- What a waterfall shows: time, frequency, amplitude, burst timing, and noise floor.
- What FSK/GFSK means: information carried by frequency deviation rather than amplitude.
- What packet framing does: preamble, sync word, headers, payload length, CRC, and sequence tracking.
- What the legal boundary is: receive-only first; transmit only after checking current local rules.

Do not start with full video. Start with receive-only SDR proof, then simulated packets, then known text packets, then still images.

## Phase 0 - Project Setup And Learning Map

Outcome: the repository is understandable to a future employer and safe for public viewing.

Learn:

- Project scoping
- Safety gating
- Evidence-driven engineering notes

Prove:

- README explains the purpose and non-goals.
- Docs define the architecture and legal checklist.
- GitHub issues break the work into guided learning tasks.

Evidence:

- Initial commit
- Issue list
- Milestones and labels

Difficulty: beginner project-management, intermediate technical framing.

## Phase 1 - SDR Bring-Up With Nooelec v5

Outcome: the RTL-SDR receive chain works on the host machine.

Learn:

- RTL-SDR drivers
- Device enumeration
- Center frequency, sample rate, gain
- Spectrum and waterfall basics
- FM broadcast demodulation as a known-good receive test

Prove:

- SDR++/SDR# sees the device.
- A local FM station can be received.
- A small IQ capture can be recorded and replayed or inspected.

Evidence:

- Screenshot of device detection
- Screenshot of FM waterfall
- Notes listing OS, driver, sample rate, gain, antenna, and frequency

Difficulty: beginner to intermediate, mostly tooling.

## Phase 2 - Receive-Only RF Literacy

Outcome: build intuition for real RF activity without transmitting.

Learn:

- Burst signals
- Band occupancy
- Antenna placement effects
- Overload and clipping
- Why decoding private content is out of scope

Prove:

- Observe ADS-B at 1090 MHz if conditions permit.
- Observe 433 MHz or 915 MHz activity receive-only.
- Record repeatable observation notes.
- Treat legacy NOAA POES/APT as retired. If a weather-satellite task is attempted, use it as a planning note for realistic alternatives rather than assuming NOAA APT capture is still available.

Evidence:

- Waterfall screenshots
- RF observation log entries
- Notes on bandwidth, burst duration, and likely modulation
- For weather-satellite planning: a current-status note and a decision to skip, defer, or choose an alternative receive-only experiment.

Difficulty: beginner to intermediate.

## Phase 3 - Python Digital Link Simulation

Outcome: understand packet reliability before using hardware.

Learn:

- Packet fields and byte ordering
- CRC
- BER and PER
- Packet-size tradeoffs
- Why JPEG is fragile under missing packets

Prove:

- Encode/decode tests pass.
- Corrupted packets fail CRC.
- BER/PER plots explain why payload size matters.
- JPEG chunking works only when all required packets arrive.

Evidence:

- Unit tests
- Simulation plots
- Short README explaining assumptions

Difficulty: intermediate DSP/comms.

## Phase 4 - CC1101 Standalone Packet Link

Outcome: generate a known legal low-power signal and verify the module settings.

Learn:

- CC1101 frequency variants
- SPI control
- Modulation settings
- Symbol rate and deviation
- Legal-band and power constraints

Prove:

- Module pinout and frequency variant are verified.
- Firmware sends known text packets.
- A second CC1101 or SDR can observe the signal.

Evidence:

- Pinout notes
- Firmware build result
- SDR screenshot or CC1101 receive log

Difficulty: intermediate embedded/RF.

## Phase 5 - ESP32-CAM Image Capture

Outcome: know what image payload sizes are realistic.

Learn:

- OV2640 frame sizes
- JPEG quality/size tradeoff
- Serial logging and ESP32-CAM flashing
- Why full-motion video is not an MVP

Prove:

- Capture a still frame.
- Log resolution, JPEG quality, and byte size.
- Create a frame-size budget table.

Evidence:

- Serial output
- Budget table
- Design decision choosing the MVP payload

Difficulty: intermediate embedded.

## Phase 6 - Packet Protocol And Frame Transport

Outcome: firmware and host tools share one packet definition.

Learn:

- Sequence numbers
- Missing-packet detection
- Incomplete-frame handling
- Preamble and sync strategies

Prove:

- ESP32 encoder emits packets with frame and packet IDs.
- Python decoder reconstructs a file from simulated packets.
- Missing packets are reported cleanly.

Evidence:

- Test vectors
- Python tests
- Protocol documentation

Difficulty: intermediate.

## Phase 7 - SDR/GNU Radio FSK Receiver

Outcome: recover known CC1101 packet bytes from SDR captures.

Learn:

- Frequency translation
- Low-pass filtering
- Quadrature demodulation
- Clock recovery
- Binary slicing
- Sync detection

Prove:

- GNU Radio flowgraph produces a bit or byte stream.
- Python sync detector finds known packets.
- Offline record-first-process-later workflow exists.

Evidence:

- Flowgraph file
- Decoded known payload
- Receiver settings log

Difficulty: intermediate to advanced.

## Phase 8 - End-To-End Image Link

Outcome: reconstruct a tiny image from the full chain.

Learn:

- Real packet loss
- Latency and goodput
- Frame discard policy
- Viewer/update loop basics

Prove:

- Static test image is reconstructed or failure is quantified.
- ESP32-CAM still frame is reconstructed.
- A primitive slow image stream works within honest limitations.

Evidence:

- Reconstructed image
- Packet success logs
- FPS and dropped-frame notes

Difficulty: advanced integration.

## Phase 9 - Measurement, Link Budget, And Failure Analysis

Outcome: turn the demo into engineering evidence.

Learn:

- Free-space path loss
- Link margin
- Antenna orientation
- Packet success vs distance
- Packet success vs payload size
- Simulation-vs-real gaps

Prove:

- Link budget assumptions are explicit.
- Measurements produce tables or plots.
- Final report explains failures, not just successes.

Evidence:

- Tables
- Plots
- Screenshots
- Failure notes

Difficulty: advanced analysis.

## Phase 10 - Portfolio Polish

Outcome: produce a clear public artifact.

Learn:

- Technical communication
- Architecture diagrams
- Demo scripts
- Resume translation

Prove:

- Final report is complete.
- README links to the final demo and report.
- Resume bullets are specific and quantified.

Evidence:

- Final report
- Architecture diagram
- Demo script
- Retrospective

Difficulty: intermediate communication.
