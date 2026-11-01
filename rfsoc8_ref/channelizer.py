"""Software polyphase FIR + FFT demonstration; not vendor IP or production RTL."""

import numpy as np
from scipy.signal import firwin


def design_prototype(bin_count: int, taps_per_phase: int) -> np.ndarray:
    """Windowed low-pass prototype for a critically sampled teaching PFB."""
    tap_count = bin_count * taps_per_phase
    taps = firwin(tap_count, cutoff=1.0 / bin_count, window="hamming", fs=1.0)
    return taps / np.sum(taps)


def pfb_channelize(
    signal: np.ndarray, bin_count: int = 64, taps_per_phase: int = 8
) -> np.ndarray:
    """Return complex PFB spectra shaped [frame, bin] for a 1-D complex signal."""
    x = np.asarray(signal, dtype=np.complex128).ravel()
    taps = design_prototype(bin_count, taps_per_phase)
    window_size = taps.size
    if x.size < window_size:
        x = np.pad(x, (0, window_size - x.size))
    frame_count = 1 + (x.size - window_size) // bin_count
    spectra = np.empty((frame_count, bin_count), dtype=np.complex128)
    for frame_index in range(frame_count):
        start = frame_index * bin_count
        window = x[start : start + window_size] * taps
        polyphase_sum = window.reshape(taps_per_phase, bin_count).sum(axis=0)
        spectra[frame_index] = np.fft.fftshift(np.fft.fft(polyphase_sum))
    return spectra


def frequency_axis_hz(bin_count: int, sample_rate_hz: float) -> np.ndarray:
    return np.fft.fftshift(np.fft.fftfreq(bin_count, d=1.0 / sample_rate_hz))

