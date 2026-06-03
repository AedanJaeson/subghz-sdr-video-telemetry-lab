# GNU Radio Receiver

This folder holds receiver flowgraphs and notes.

## First Target

Recreate the Python offline demod result from a saved `.cu8` capture:

```text
File Source byte
  -> UChar To Float
  -> Deinterleave
      I path -> Add Const -127.5 -> Multiply Const 1/127.5
      Q path -> Add Const -127.5 -> Multiply Const 1/127.5
  -> Float To Complex
  -> Throttle
  -> Low Pass Filter complex
  -> Quadrature Demod
  -> Moving Average
  -> QT GUI Time Sink
```

The goal is to see the CC1101 packet burst turn into a two-level FSK waveform.
Do not start with image decode or a live receiver.

## Why This Chain Exists

The RTL-SDR `.cu8` file stores interleaved unsigned IQ bytes:

```text
I0, Q0, I1, Q1, ...
```

GNU Radio needs those converted into normalized complex samples:

```text
I + jQ, centered around 0, scaled roughly -1.0 ... +1.0
```

Then the low-pass filter isolates the narrow CC1101 signal, and quadrature
demod converts FSK frequency shifts into a normal float waveform.

Detailed block-by-block theory is in:

```text
docs/07_gnuradio_receiver_design.md
```

## First Success Criteria

- The flowgraph opens in GNU Radio Companion.
- The file source reads a known CC1101 `.cu8` capture.
- The QT GUI Time Sink shows quiet/noisy regions between bursts.
- During each burst, the quadrature-demod output has two visible levels.
- Settings used are recorded in an experiment note or commit message.

## Later Targets

- Add symbol timing and binary slicing.
- Produce a bit or byte stream.
- Decode packet boundaries and CRC in Python.
- Build a live RTL-SDR version after the offline chain is understood.
