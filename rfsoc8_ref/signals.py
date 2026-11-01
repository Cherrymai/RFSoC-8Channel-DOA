"""Synthetic CW/FMCW generators. These functions emulate data, not RF hardware."""

import numpy as np

from .geometry import steering_vector


def generate_cw(sample_count: int, sample_rate_hz: float, tone_hz: float) -> np.ndarray:
    time_s = np.arange(sample_count) / sample_rate_hz
    return np.exp(1j * 2.0 * np.pi * tone_hz * time_s)


def generate_fmcw(
    sample_count: int,
    sample_rate_hz: float,
    start_hz: float = -200e3,
    stop_hz: float = 200e3,
) -> np.ndarray:
    """Generate one complex baseband linear chirp; no range/velocity scene is modeled."""
    duration_s = sample_count / sample_rate_hz
    time_s = np.arange(sample_count) / sample_rate_hz
    slope_hz_s = (stop_hz - start_hz) / duration_s
    phase = 2.0 * np.pi * (start_hz * time_s + 0.5 * slope_hz_s * time_s**2)
    return np.exp(1j * phase)


def synthesize_array_data(
    waveform: np.ndarray,
    positions_m: np.ndarray,
    carrier_hz: float,
    az_deg: float,
    el_deg: float,
    snr_db: float,
    seed: int = 48396,
) -> np.ndarray:
    """Create ideal complex snapshots shaped [element, time], plus white noise."""
    steering = steering_vector(positions_m, carrier_hz, az_deg, el_deg)
    clean = steering[:, None] * np.asarray(waveform)[None, :]
    signal_power = float(np.mean(np.abs(clean) ** 2))
    noise_power = signal_power / (10.0 ** (snr_db / 10.0))
    rng = np.random.default_rng(seed)
    noise = np.sqrt(noise_power / 2.0) * (
        rng.standard_normal(clean.shape) + 1j * rng.standard_normal(clean.shape)
    )
    return clean + noise

