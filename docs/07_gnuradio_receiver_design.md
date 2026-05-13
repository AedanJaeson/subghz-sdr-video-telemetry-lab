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

