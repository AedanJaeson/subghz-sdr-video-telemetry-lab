# Pre-Transmit Work Plan

Updated: 2026-05-15

The CC1101 module has been ordered and is expected by 2026-05-27. Until it arrives, RF transmit work is blocked. The project should keep momentum by proving everything that can be proven before the radio module exists.

## Current Rule

No CC1101 RF transmission work is expected until the module arrives, the frequency variant is verified, and the RF safety checklist is complete.

## Work That Can Continue Now

### 1. SDR Receive-Only Proof

Goal: prove the receive chain and capture workflow.

- Detect the Nooelec NESDR SMArt v5.
- Receive a local FM broadcast signal.
- Record a short IQ capture using SDR++/SDR# first.
- Add metadata for every capture.
- Keep large IQ files out of Git.

### 2. Packet Protocol In Python

Goal: make the packet format real before firmware.

- Implement packet encode/decode.
- Include preamble, sync word, protocol version, frame ID, packet ID, total packets, payload length, payload, and CRC.
- Add tests for clean packets, corrupted CRC, missing packets, duplicate packets, and out-of-order packets.

### 3. Image Serialization Simulation

Goal: prove that image bytes can become packets and become an image again.

- Use a tiny fixture image or generated test payload.
- Split bytes into packets.
- Reconstruct perfectly when all packets arrive.
- Drop or corrupt packets and confirm the decoder reports failure cleanly.
- Record packet count, payload size, total overhead, and reconstructed file hash.

### 4. Serial/File Loopback

Goal: simulate the firmware-to-host transport without RF.

Recommended first loopback:

```text
image file -> packet encoder -> packet stream file -> Python decoder -> reconstructed image
```

If the ESP32-CAM is available, add:

```text
ESP32-CAM capture -> firmware packet encoder -> serial byte dump -> Python decoder -> reconstructed image
```

This proves the image serialization and packet format before the CC1101 is involved.

### 5. ESP32-CAM Frame Budget

Goal: know whether the planned image sizes are plausible.

- Capture still frames at small resolutions.
- Log JPEG quality, resolution, and byte count.
- Estimate packet count and transmit time for several payload sizes.
- Decide the MVP payload: tiny JPEG or raw/grayscale thumbnail.

## Blocked Until CC1101 Arrives

- CC1101 module variant and pinout verification.
- CC1101 transmit sketch.
- CC1101-to-CC1101 packet link.
- Capturing the CC1101 signal with SDR.
- GNU Radio demod of real CC1101 packets.
- End-to-end RF image link.

## Recommended Active Issues

Work these before returning to RF transmit:

- Issue 005: Install SDR drivers and verify device enumeration.
- Issue 006: First FM broadcast receive.
- Issue 007: Record and replay first IQ capture.
- Issue 013: Build simple packet framing model in Python.
- Issue 016: Add JPEG frame chunking simulation.
- Issue 027: Implement Python packet decoder.
- Issue 028: Add sequence tracking and missing-packet report.
- Issue 029: Define sync word and preamble strategy.

