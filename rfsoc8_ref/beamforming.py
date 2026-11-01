"""Floating-point conventional beamforming reference; not synthesizable RTL."""

import numpy as np

from .geometry import steering_vector


def conventional_weights(
    positions_m: np.ndarray, carrier_hz: float, az_deg: float, el_deg: float
) -> np.ndarray:
    steering = steering_vector(positions_m, carrier_hz, az_deg, el_deg)
    return steering / len(steering)


def apply_beamformer(snapshots: np.ndarray, weights: np.ndarray) -> np.ndarray:
    if snapshots.shape[0] != weights.size:
        raise ValueError("snapshot channel count and weight count differ")
    return np.conjugate(weights) @ snapshots


def azimuth_pattern_db(
    positions_m: np.ndarray,
    carrier_hz: float,
    look_az_deg: float,
    look_el_deg: float,
    azimuths_deg: np.ndarray,
) -> np.ndarray:
    weights = conventional_weights(positions_m, carrier_hz, look_az_deg, look_el_deg)
    response = np.array(
        [
            abs(np.vdot(weights, steering_vector(positions_m, carrier_hz, az, look_el_deg)))
            for az in azimuths_deg
        ]
    )
    response /= max(response.max(), np.finfo(float).eps)
    return 20.0 * np.log10(np.maximum(response, 1e-6))

