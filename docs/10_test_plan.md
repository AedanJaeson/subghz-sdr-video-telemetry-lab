# Test Plan

## Test Philosophy

Every phase should leave evidence: screenshots, logs, plots, tests, or written observations.

## Early Tests

- SDR device enumeration.
- FM broadcast receive.
- IQ capture/replay workflow.
- Packet encode/decode unit tests.
- CRC rejection tests.

## Integration Tests

- Known CC1101 text packet captured by SDR.
- Offline demod recovers the same known payload.
- Simulated packet stream reconstructs a file.
- Full RF path reconstructs a small image or quantifies failure.

