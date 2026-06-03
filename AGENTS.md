# AGENTS.md

This repository is Aedan's guided communications-engineering lab for a
low-rate sub-GHz image/video telemetry learning link:

```text
ESP32-CAM -> packetised payload -> CC1101 FSK/GFSK -> legal low-power RF or
bench link -> RTL-SDR -> GNU Radio/Python demod -> packet decode -> image
reconstruction
```

This file is the repo-local operating manual for Codex and other AI agents.
It should be read before making changes. It is the closest equivalent to a
project-specific `CLAUDE.md`, but do not assume it is magical permanent
memory: if a future agent has not loaded this file, read it explicitly.

## First Files To Read

Read these before planning or editing:

1. `README.md`
2. `docs/01_learning_path.md`
3. `docs/04_rf_safety_and_legal_notes.md`
4. `docs/05_system_architecture.md`
5. `docs/06_packet_protocol.md`
6. `docs/07_gnuradio_receiver_design.md`
7. `docs/cc1101_bringup_plan.md`
8. `firmware/esp32cam_cc1101/README.md`
9. `firmware/esp32cam_cc1101/platformio.ini`
10. `receiver/python/README.md`

For active work, also inspect:

```powershell
git status --short --branch
git log --oneline -8
```

Never overwrite user edits. This project often contains local notebooks,
screenshots, and field-test notes that may not be committed yet.

## Collaboration Contract

This is a learning project, not an "AI writes everything while Aedan watches"
project.

Default mode for agents:

1. Explain the concept and the current system boundary.
2. Show the relevant file/function/command.
3. Ask before writing substantial implementation code unless Aedan clearly
   requested the edit.
4. Prefer small, inspectable changes.
5. After changing code, explain what changed in plain engineering language.

When Aedan asks "how do I..." or "why does...", answer as a teacher first.
Do not immediately replace the learning moment with a full implementation.

It is OK to proactively run safe inspection commands, builds, tests, and small
documentation edits. It is not OK to silently design or implement a complex
receiver, packet protocol, camera pipeline, or RF transmit behavior without
first giving Aedan the shape of the design and getting a clear go-ahead.

Use this decision rule:

- Explain only: conceptual RF/DSP questions, code-reading questions, command
  walkthroughs, "what does this function do?"
- Explain then ask: new demod algorithms, packet protocol changes, firmware
  architecture changes, GNU Radio flowgraph decisions.
- Implement directly: explicitly requested file edits, scaffolds, docs,
  small bug fixes, tests, build fixes, issue updates.

Good agent behavior:

- Make Aedan smarter about the stack every time.
- Prefer "here is the mental model, here is the command, here is what to
  expect" over dropping a wall of code.
- Keep the RF safety gate visible.
- Keep changes tied to issues, evidence, and portfolio outcomes.

Bad agent behavior:

- Jumping straight to full video transport.
- Hiding complexity behind generated code.
- Enabling transmit by default.
- Treating SDR screenshots as decoration rather than measurement evidence.
- Committing large raw captures.

## Current Validated State

As of 2026-06-01, the project has reached first RF/DSP proof-of-life:

- ESP32-CAM can be powered/flashed through the HW-409 USB-to-serial adapter.
- PlatformIO firmware builds for `esp32cam` and `esp32cam_tx_test`.
- CC1101 SPI/register bring-up works:
  - `PARTNUM=0x00`
  - `VERSION=0x14`
  - `RadioLib CC1101 init ... success`
  - `CC1101 SPI OK`
- Low-power CC1101 burst transmission has been observed on SDR#.
- RTL-SDR IQ capture has been recorded as `.cu8`.
- Python analysis has shown:
  - repeated burst power envelope at the firmware cadence,
  - clean burst duration around tens of milliseconds,
  - quadrature demod with two FSK frequency states around +/-5 kHz.

Treat this as a real milestone:

```text
ESP32-CAM -> CC1101 -> RF burst -> RTL-SDR IQ -> Python quadrature demod
```

Do not assume the exact RF center from memory. The firmware currently sets
`CC1101_FREQ_MHZ=433.92`, while field captures may be tuned around nearby
measured energy such as `433.875 MHz`. Always verify the current firmware
setting, SDR tuning, module variant, and local rules before transmit tests.

## Safety And Legal Rules

This repository must remain public-safe.

Hard rules:

- Receive-only work comes first.
- Any transmit work is optional, low-power, short-range, legal-band, and
  controlled.
- Never encourage transmitting outside legal bands.
- Never encourage high-power transmission.
- Never transmit near aviation, emergency, cellular, GPS, broadcast, Defence,
  or protected bands.
- Never create malicious, surveillance, jamming, spoofing, interception, or
  disruption objectives.
- Never connect a transmitter directly to the RTL-SDR input without a designed
  attenuation path and power calculation.
- Always require the checklist in `docs/04_rf_safety_and_legal_notes.md`
  before any RF transmission.

If uncertain, do simulation, offline IQ analysis, dummy-load/attenuated bench
work, or receive-only experiments instead.

## Project Direction

The intended learning path is:

1. SDR setup and IQ capture.
2. Receive-only RF literacy.
3. Python packet and channel simulation.
4. ESP32-CAM/CC1101 bring-up.
5. Known packet bursts.
6. Offline Python demod from recorded IQ.
7. GNU Radio receiver chain once Python proves the DSP shape.
8. Packet sync/CRC/reconstruction.
9. Tiny still image.
10. Low-FPS image stream only after the earlier layers are understood.

Do not start with full video. The first useful receiver goal is:

```text
Recover a known test packet from a recorded IQ capture.
```

## Recommended Laptop Environment

Target platform for field tests: Windows laptop.

Minimum installs:

- Git
- GitHub CLI (`gh`), optional but useful for issue/project updates
- Visual Studio Code
- PlatformIO IDE VS Code extension, optional but recommended
- Python 3.11, recommended for the project virtual environment
- RTL-SDR command-line tools (`rtl_sdr.exe`, `rtl_test.exe`)
- Zadig/WinUSB driver for the RTL-SDR on Windows
- SDR# or SDR++ for visual RF checks
- GNU Radio, preferably after Python offline demod is underway

Python version guidance:

- Use Python 3.11 for the repo `.venv` unless there is a specific reason not
  to. It is a conservative choice for NumPy/Matplotlib/pytest/PlatformIO work.
- Python 3.12 is likely fine if packages install cleanly.
- Avoid relying on Python 3.13+ for this repo until the DSP and SDR package
  stack has been confirmed on the laptop.
- GNU Radio installed through Radioconda/conda will usually bring its own
  Python environment. Keep that separate from the repo `.venv`.

Official references worth checking when setting up a new machine:

- PlatformIO install docs: https://docs.platformio.org/en/latest/core/installation/
- PlatformIO Python note: https://docs.platformio.org/en/latest/faq/install-python.html
- GNU Radio Windows install: https://wiki.gnuradio.org/index.php/WindowsInstall
- GNU Radio conda install: https://wiki.gnuradio.org/index.php/CondaInstall
- RTL-SDR quick start: https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/

## Windows Bootstrap Checklist

From a fresh clone:

```powershell
cd C:\Users\Aedan\dev\subghz-sdr-video-telemetry-lab
git status --short --branch
python --version
```

Create and activate the Python environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r receiver\python\requirements.txt
python -m pip install -r simulation\python\requirements.txt
python -m pip install --upgrade platformio
```

If `py -3.11` is unavailable, install Python 3.11 from python.org or use the
available compatible Python after confirming package installs.

Check PlatformIO:

```powershell
cd firmware\esp32cam_cc1101
python -m platformio run -e esp32cam
python -m platformio run -e esp32cam_tx_test
```

Check the RTL-SDR command-line tools from the folder where they are installed:

```powershell
.\rtl_test.exe -t
```

Only one program can usually own the RTL-SDR at a time. Close/stop SDR# or
SDR++ before using `rtl_sdr.exe`.

Example IQ capture command:

```powershell
.\rtl_sdr.exe -d 0 -f 433875000 -s 2040000 -g 20 -n 40800000 C:\Users\Aedan\dev\subghz-sdr-video-telemetry-lab\captures\example_iq\cc1101_433875000_2040000sps_10s.cu8
```

For `.cu8`, `-n` is bytes. At 2.04 MS/s, a 10 second capture is:

```text
2 bytes per complex sample * 2,040,000 samples/s * 10 s = 40,800,000 bytes
```

Do not commit large IQ captures.

## Firmware Notes

Firmware source:

```text
firmware/esp32cam_cc1101/src/main.cpp
```

Build environments:

```text
esp32cam         safe default, CC1101_TRANSMIT_ENABLED=0
esp32cam_tx_test low-power TX test, CC1101_TRANSMIT_ENABLED=1
```

Common commands:

```powershell
cd firmware\esp32cam_cc1101
python -m platformio run -e esp32cam
python -m platformio run -e esp32cam --target upload
python -m platformio run -e esp32cam_tx_test
python -m platformio run -e esp32cam_tx_test --target upload
python -m platformio device monitor -e esp32cam_tx_test
```

Current hardware wiring:

```text
HW-409 5V  -> ESP32-CAM 5V
HW-409 GND -> ESP32-CAM GND
HW-409 TXD -> ESP32-CAM U0R/RX/GPIO3
HW-409 RXD -> ESP32-CAM U0T/TX/GPIO1

For flashing only:
ESP32-CAM GPIO0 -> GND

CC1101 GND  -> ESP32-CAM GND
CC1101 VCC  -> ESP32-CAM 3V3
CC1101 SCK  -> ESP32-CAM GPIO14
CC1101 MISO -> ESP32-CAM GPIO12
CC1101 MOSI -> ESP32-CAM GPIO13
CC1101 CSN  -> ESP32-CAM GPIO15
CC1101 GDO0 -> ESP32-CAM GPIO2
CC1101 GDO2 -> ESP32-CAM GPIO16
```

CC1101 VCC is 3.3 V only. Do not connect it to 5 V.

`main.cpp` currently transmits simple ASCII test packets in the TX test env:

```text
SUBGHZ_LAB_TEST_0
SUBGHZ_LAB_TEST_1
...
```

The text is passed to RadioLib as bytes using `packet.c_str()` and
`reinterpret_cast<const uint8_t *>`. For teaching moments, explain this as
"view the existing ASCII characters as a byte array"; do not overcomplicate it.

## Receiver/Demod Direction

Preferred order:

1. Python offline analysis of recorded `.cu8`.
2. Python burst detection and quadrature demod plots.
3. Python bit recovery experiments.
4. Packet sync/CRC decoder.
5. GNU Radio flowgraph once the DSP shape is understood.
6. Live receiver.

Use Python for:

- reading `.cu8`,
- unsigned IQ normalization,
- power vs time,
- burst detection,
- quadrature demod,
- plotting,
- packet parser tests.

Use GNU Radio for:

- interactive receiver-chain experiments,
- live RTL-SDR source,
- frequency translating filter,
- low-pass filter,
- quadrature demod,
- symbol timing/clock recovery,
- binary slicing,
- file/socket sink to Python.

When helping with GNU Radio, explain every new block in terms of:

- what data type it expects,
- what data type it outputs,
- what physical/DSP idea it represents,
- why it belongs at that point in the chain,
- what the user should expect to see if it is working.

Do not give Aedan a block list without the theory. GNU Radio is part of the
learning objective, not just a tool for producing bits.

Do not use C++ for the receiver MVP unless Aedan explicitly asks. C++ is useful
later for a polished high-performance receiver, but it slows learning during
early DSP exploration.

## Capture And Evidence Policy

Useful evidence to commit:

- Markdown notes explaining setup, frequency, sample rate, gain, and result.
- Small scripts used to generate plots.
- Screenshots/figures in `reports/figures/` when they support a documented
  experiment.
- Tables/CSV summaries of measurements.
- Test output summaries.

Do not commit:

- large `.cu8`, `.iq`, `.cf32`, `.wav`, `.raw`, or `.cfile` captures,
- secrets, tokens, or environment dumps,
- unreviewed generated clutter,
- private or sensitive decoded content.

Raw captures should remain local or move to external storage. The repo should
contain instructions and reproducible analysis code, not bulky RF recordings.

## Git And GitHub Workflow

Before editing:

```powershell
git status --short --branch
```

Keep commits small and descriptive. Good commit examples:

```text
Add CC1101 burst demod notebook notes
Document Windows laptop setup
Add packet CRC tests
Record SDR capture workflow
```

Do not commit unrelated user changes. If the worktree contains unrelated
notebooks, screenshots, or firmware edits, leave them alone unless Aedan asks.

If pushing:

```powershell
git add <specific files>
git commit -m "<message>"
git push
```

Use GitHub issues as the backlog source. Every substantial change should map
to an issue or create/update one.

## Agent Response Style

Use concise, plain engineering language. Aedan likes to understand the system
deeply, so include the mental model before or alongside commands.

When explaining code, point to the exact file/function. When explaining RF/DSP,
connect the concept to the measured plots or current firmware settings.

When giving commands, include:

- working directory,
- command,
- expected output,
- what failure usually means.

When the user is in the middle of hardware work, prefer immediate practical
steps over broad lectures.

## Hard Stop Conditions

Stop and ask before proceeding if:

- a change would enable RF transmission by default,
- a test would transmit outside verified legal conditions,
- a command may overwrite local captures/notebooks/user edits,
- the next step needs hardware state that cannot be inferred,
- a design choice affects the packet protocol, receiver architecture, or
  portfolio narrative.

If blocked, explain the smallest useful next observation or command.
