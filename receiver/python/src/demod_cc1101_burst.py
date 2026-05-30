"""Offline CC1101 2-FSK burst demod exploration from RTL-SDR .cu8 captures.

This is intentionally a learning/debug script, not a polished packet decoder.
It loads unsigned 8-bit IQ samples, finds high-power bursts, quadrature-demods
one burst into instantaneous frequency, slices it into candidate bits, then
tries simple byte packings to look for the known ASCII test payload.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class Burst:
    start_sample: int
    end_sample: int
    peak_db: float


def load_cu8(path: Path) -> np.ndarray:
    raw = np.fromfile(path, dtype=np.uint8)
    raw = raw[: len(raw) // 2 * 2]
    iq = raw.reshape(-1, 2).astype(np.float32)
    i = (iq[:, 0] - 127.5) / 127.5
    q = (iq[:, 1] - 127.5) / 127.5
    return i + 1j * q


def moving_average(values: np.ndarray, width: int) -> np.ndarray:
    if width <= 1:
        return values
    kernel = np.ones(width, dtype=np.float32) / width
    return np.convolve(values, kernel, mode="valid")


def find_bursts(samples: np.ndarray, sample_rate: int, threshold_db: float) -> list[Burst]:
    power = np.abs(samples) ** 2
    window = sample_rate // 1000
    trimmed = power[: len(power) // window * window]
    power_ms = trimmed.reshape(-1, window).mean(axis=1)
    power_ms_db = 10 * np.log10(power_ms + 1e-12)

    active = power_ms_db > threshold_db
    bursts: list[Burst] = []
    idx = 0
    while idx < len(active):
        if not active[idx]:
            idx += 1
            continue
        start_ms = idx
        while idx < len(active) and active[idx]:
            idx += 1
        end_ms = idx
        peak_db = float(power_ms_db[start_ms:end_ms].max())
        bursts.append(Burst(start_ms * window, end_ms * window, peak_db))
    return bursts


def quadrature_demod(samples: np.ndarray, sample_rate: int, smooth: int) -> np.ndarray:
    phase = np.unwrap(np.angle(samples))
    freq_hz = np.diff(phase) * sample_rate / (2 * np.pi)
    return moving_average(freq_hz, smooth)


def slice_bits(freq_hz: np.ndarray, samples_per_symbol: float, offset: int, invert: bool) -> np.ndarray:
    sample_points = np.arange(offset, len(freq_hz), samples_per_symbol).astype(np.int64)
    sample_points = sample_points[sample_points < len(freq_hz)]
    bits = freq_hz[sample_points] > np.median(freq_hz)
    if invert:
        bits = ~bits
    return bits.astype(np.uint8)


def pack_bits(bits: np.ndarray, msb_first: bool) -> bytes:
    usable = bits[: len(bits) // 8 * 8].reshape(-1, 8)
    if msb_first:
        weights = np.array([128, 64, 32, 16, 8, 4, 2, 1], dtype=np.uint8)
    else:
        weights = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)
    return bytes((usable * weights).sum(axis=1).astype(np.uint8))


def printable_preview(data: bytes, limit: int = 120) -> str:
    text = "".join(chr(b) if 32 <= b <= 126 else "." for b in data[:limit])
    return text


def search_candidates(freq_hz: np.ndarray, sample_rate: int, bit_rate: float) -> None:
    samples_per_symbol = sample_rate / bit_rate
    print(f"samples/symbol: {samples_per_symbol:.2f}")
    print("candidate byte streams containing SUBGHZ or LAB:")

    hits = 0
    max_offset = int(samples_per_symbol)
    for offset in range(max_offset):
        for invert in (False, True):
            bits = slice_bits(freq_hz, samples_per_symbol, offset, invert)
            for msb_first in (True, False):
                data = pack_bits(bits, msb_first)
                if b"SUBGHZ" in data or b"LAB" in data:
                    hits += 1
                    print(
                        f"- offset={offset} invert={invert} "
                        f"bit_order={'msb' if msb_first else 'lsb'}"
                    )
                    print(f"  hex: {data[:80].hex(' ')}")
                    print(f"  txt: {printable_preview(data)}")
                    if hits >= 8:
                        return
    if hits == 0:
        print("- no ASCII hit yet; inspect plots and try symbol timing/sync handling next")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("capture", type=Path, help="RTL-SDR .cu8 capture")
    parser.add_argument("--sample-rate", type=int, default=2_040_000)
    parser.add_argument("--bit-rate", type=float, default=4_800.0)
    parser.add_argument("--threshold-db", type=float, default=-25.0)
    parser.add_argument("--burst", type=int, default=0)
    parser.add_argument("--smooth", type=int, default=64)
    parser.add_argument("--plots", action="store_true")
    args = parser.parse_args()

    samples = load_cu8(args.capture)
    duration_s = len(samples) / args.sample_rate
    print(f"loaded {len(samples):,} complex samples ({duration_s:.2f} s)")

    bursts = find_bursts(samples, args.sample_rate, args.threshold_db)
    print(f"found {len(bursts)} burst(s) above {args.threshold_db:.1f} dB")
    for idx, burst in enumerate(bursts[:10]):
        start_ms = burst.start_sample / args.sample_rate * 1000
        end_ms = burst.end_sample / args.sample_rate * 1000
        print(f"- #{idx}: {start_ms:.1f}-{end_ms:.1f} ms peak={burst.peak_db:.1f} dB")

    if not bursts:
        raise SystemExit("no bursts found; lower --threshold-db or check the capture")
    if args.burst >= len(bursts):
        raise SystemExit(f"burst index {args.burst} out of range")

    burst = bursts[args.burst]
    pad = int(0.002 * args.sample_rate)
    start = max(0, burst.start_sample - pad)
    end = min(len(samples), burst.end_sample + pad)
    burst_samples = samples[start:end]
    freq_hz = quadrature_demod(burst_samples, args.sample_rate, args.smooth)

    print(
        "demod frequency levels approx: "
        f"p10={np.percentile(freq_hz, 10):.0f} Hz, "
        f"median={np.median(freq_hz):.0f} Hz, "
        f"p90={np.percentile(freq_hz, 90):.0f} Hz"
    )
    search_candidates(freq_hz, args.sample_rate, args.bit_rate)

    if args.plots:
        t_ms = np.arange(len(freq_hz)) / args.sample_rate * 1000
        plt.figure(figsize=(12, 4))
        plt.plot(t_ms, freq_hz)
        plt.xlabel("Time within selected burst (ms)")
        plt.ylabel("Instantaneous frequency offset (Hz)")
        plt.title("CC1101 Quadrature Demod")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()
