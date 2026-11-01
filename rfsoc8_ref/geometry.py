"""Ideal 8-element UCA geometry. No measured antenna calibration is included."""

import numpy as np

SPEED_OF_LIGHT_M_S = 299_792_458.0


def uca_positions(element_count: int = 8, radius_m: float = 0.04) -> np.ndarray:
    """Return ideal element XYZ coordinates with element 0 on the +X axis."""
    angles = 2.0 * np.pi * np.arange(element_count) / element_count
    return np.column_stack(
        (radius_m * np.cos(angles), radius_m * np.sin(angles), np.zeros(element_count))
    )


def unit_direction(az_deg: float, el_deg: float) -> np.ndarray:
    """Direction vector; azimuth is from +X to +Y, elevation is above XY."""
    az = np.deg2rad(az_deg)
    el = np.deg2rad(el_deg)
    return np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])


def steering_vector(
    positions_m: np.ndarray, carrier_hz: float, az_deg: float, el_deg: float
) -> np.ndarray:
    """Ideal narrowband receive steering vector with unit-magnitude elements."""
    wavelength_m = SPEED_OF_LIGHT_M_S / carrier_hz
    phase = -2.0 * np.pi / wavelength_m * (positions_m @ unit_direction(az_deg, el_deg))
    return np.exp(1j * phase)

