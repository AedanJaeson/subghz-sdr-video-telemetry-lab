# GNU Radio Receiver Design

Planned CC1101 FSK/GFSK receive chain:

```text
RTL-SDR source
  -> frequency translating filter
  -> low-pass filter
  -> quadrature demod
  -> clock recovery
  -> binary slicer
  -> file or socket sink
  -> Python packet synchroniser/decoder
```

The first receiver goal is to recover known text packets, not images.

## Offline Workflow

Record IQ first, then process the same capture repeatedly. This makes demodulation experiments reproducible and avoids changing RF conditions while debugging.

## First Offline Flowgraph: See The FSK

The first GNU Radio flowgraph should read a saved RTL-SDR `.cu8` capture and
reproduce what the Python notebook already showed: a burst envelope and a
two-level FSK demod waveform. Do not start with live SDR or packet decoding.

Target flow:

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

Useful variables:

```text
samp_rate = 2.04e6
decim = 16
channel_rate = samp_rate / decim
freq_dev = 5e3
quad_gain = channel_rate / (2 * 3.141592653589793 * freq_dev)
```

### File Source

Settings:

```text
Type: Byte
File: path to the .cu8 capture
Repeat: Yes, for GUI testing
```

Purpose: this reads the raw bytes captured by `rtl_sdr.exe`.

The `.cu8` format is interleaved unsigned 8-bit IQ:

```text
I0, Q0, I1, Q1, I2, Q2, ...
```

Each pair of bytes represents one complex SDR sample at one instant in time.
The file source does not understand any RF meaning yet. It just streams bytes.

### UChar To Float

Settings:

```text
Scale: 1
```

Purpose: convert each unsigned byte from integer form into a floating-point
number so later DSP blocks can do arithmetic.

At this point the values are still in the RTL-SDR byte range:

```text
0 ... 255
```

They are not yet normal centered IQ samples.

### Deinterleave

Settings:

```text
Item size: gr.sizeof_float
Num outputs: 2
Block size: 1
```

Purpose: split the alternating byte stream into separate I and Q streams.

Input:

```text
I0, Q0, I1, Q1, I2, Q2, ...
```

Outputs:

```text
out0: I0, I1, I2, ...
out1: Q0, Q1, Q2, ...
```

This is a generic GNU Radio stream block. Do not use LoRa-specific
deinterleavers here.

### Add Const

Settings on both I and Q paths:

```text
Constant: -127.5
```

Purpose: remove the unsigned-byte DC offset.

RTL-SDR `.cu8` samples are centered around `127.5`, not zero. DSP math expects
baseband IQ centered around zero. Subtracting `127.5` changes:

```text
0     -> -127.5
127.5 -> 0
255   -> +127.5
```

Without this step, the signal has a large artificial DC offset.

### Multiply Const

Settings on both I and Q paths:

```text
Constant: 0.0078431372549
```

That constant is:

```text
1 / 127.5
```

Purpose: normalize the centered byte samples into the usual DSP range:

```text
-1.0 ... +1.0
```

The full conversion is:

```text
normalized = (byte_value - 127.5) / 127.5
```

This is the GNU Radio version of the Python code:

```python
i = (iq[:, 0].astype(np.float32) - 127.5) / 127.5
q = (iq[:, 1].astype(np.float32) - 127.5) / 127.5
```

### Float To Complex

Purpose: rebuild the two real streams into one complex IQ stream:

```text
I + jQ
```

Connect the normalized I path to the real input and the normalized Q path to
the imaginary input.

After this block, GNU Radio finally has real SDR complex baseband samples.

### Throttle

Settings:

```text
Type: Complex
Sample Rate: samp_rate
```

Purpose: stop a file-based GUI flowgraph from running as fast as the computer
can read the file.

When using a hardware source such as an RTL-SDR Source, do not use Throttle;
the hardware controls the sample rate. For a File Source, Throttle makes the
time sinks and GUI behavior easier to understand.

### Low Pass Filter

Settings:

```text
Type: Complex -> Complex
Decimation: decim
Gain: 1
Sample Rate: samp_rate
Cutoff: 25000
Transition Width: 10000
Window: Hamming
```

Purpose: keep the narrow CC1101 signal and remove nearby noise/out-of-band
energy before demodulation.

The CC1101 test signal uses about `+/-5 kHz` deviation at `4.8 kbps`, so a
cutoff around `25 kHz` is deliberately wider than the data but much narrower
than the full `2.04 MHz` RTL-SDR capture.

The filter also decimates by `16`:

```text
2.04 MS/s / 16 = 127.5 kS/s
```

That lower sample rate is still plenty for a `4.8 kbps` signal and makes later
plots and DSP blocks easier to handle.

### Quadrature Demod

Settings:

```text
Gain: quad_gain
```

Purpose: convert frequency changes in the complex IQ signal into an amplitude
waveform.

FSK stores bits as frequency shifts:

```text
bit state A -> carrier slightly below center
bit state B -> carrier slightly above center
```

Quadrature demod measures the phase change from one complex sample to the next.
Phase change per sample is frequency. After this block, the two FSK tones should
appear as two amplitude levels.

The gain:

```text
quad_gain = channel_rate / (2 * pi * freq_dev)
```

roughly scales `+/-5 kHz` deviation into approximately `+/-1`.

If the output levels are inverted, that is not fatal. It may mean the tuned
frequency is on the other side, the frequency offset sign is reversed, or the
bit interpretation needs inversion later.

### Moving Average

Settings:

```text
Length: 16
Scale: 1.0 / 16
```

Purpose: smooth high-rate noise in the quadrature-demod output so the two FSK
levels are easier to see.

This is not final clock recovery. It is just a visual/debugging smoother for
the first flowgraph.

### QT GUI Time Sink

Settings:

```text
Type: Float
Sample Rate: channel_rate
```

Purpose: display the demodulated signal in time.

Expected first success:

```text
During noise: messy/random output
During burst: two visible FSK levels around approximately -1 and +1
```

If you see the two levels, the offline GNU Radio demod has reproduced the
Python quadrature-demod proof point.

## After The First Flowgraph Works

Do not jump straight to JPEG or live video. The next steps are:

1. Add burst gating or manual zooming.
2. Estimate symbol timing for `4.8 kbps`.
3. Add binary slicing.
4. Search for known packet structure or known ASCII test payloads.
5. Move packet synchronisation and CRC checks into Python.
6. Only then create a live RTL-SDR flowgraph.
