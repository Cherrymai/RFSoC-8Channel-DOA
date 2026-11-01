"""Floating-point MUSIC grid search for education; not FPGA hardware acceleration."""

import numpy as np

from .geometry import steering_vector


def covariance_matrix(snapshots: np.ndarray) -> np.ndarray:
    centered = snapshots - snapshots.mean(axis=1, keepdims=True)
    return centered @ centered.conj().T / centered.shape[1]


def music_spectrum_2d(
    snapshots: np.ndarray,
    positions_m: np.ndarray,
    carrier_hz: float,
    azimuths_deg: np.ndarray,
    elevations_deg: np.ndarray,
    source_count: int = 1,
) -> np.ndarray:
    """Compute a normalized MUSIC pseudospectrum in dB over an az/el grid."""
    channel_count = snapshots.shape[0]
    if not 1 <= source_count < channel_count:
        raise ValueError("source_count must be between 1 and channel_count-1")
    covariance = covariance_matrix(snapshots)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)
    noise_subspace = eigenvectors[:, order[: channel_count - source_count]]
    projector = noise_subspace @ noise_subspace.conj().T

    spectrum = np.empty((len(elevations_deg), len(azimuths_deg)), dtype=float)
    for el_index, elevation in enumerate(elevations_deg):
        for az_index, azimuth in enumerate(azimuths_deg):
            steering = steering_vector(positions_m, carrier_hz, azimuth, elevation)
            denominator = np.real(np.vdot(steering, projector @ steering))
            spectrum[el_index, az_index] = 1.0 / max(denominator, 1e-15)
    spectrum /= spectrum.max()
    return 10.0 * np.log10(np.maximum(spectrum, 1e-12))


def estimate_peak(
    spectrum_db: np.ndarray, azimuths_deg: np.ndarray, elevations_deg: np.ndarray
) -> tuple[float, float]:
    el_index, az_index = np.unravel_index(np.argmax(spectrum_db), spectrum_db.shape)
    return float(azimuths_deg[az_index]), float(elevations_deg[el_index])

