"""CSV exchange helpers for normalized simulated IQ, not raw ADC codes."""

import csv
from pathlib import Path
import numpy as np


def write_complex_channels(path: Path, snapshots: np.ndarray) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    channel_count, sample_count = snapshots.shape
    header = ["sample"]
    for channel in range(channel_count):
        header.extend([f"ch{channel}_real", f"ch{channel}_imag"])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for sample in range(sample_count):
            row = [sample]
            for channel in range(channel_count):
                value = snapshots[channel, sample]
                row.extend([f"{value.real:.10g}", f"{value.imag:.10g}"])
            writer.writerow(row)


def read_complex_channels(path: Path, channel_count: int = 8) -> np.ndarray:
    data = np.genfromtxt(path, delimiter=",", names=True)
    channels = [data[f"ch{i}_real"] + 1j * data[f"ch{i}_imag"] for i in range(channel_count)]
    return np.asarray(channels)


def write_music_grid(
    path: Path, spectrum_db: np.ndarray, azimuths_deg: np.ndarray, elevations_deg: np.ndarray
) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["azimuth_deg", "elevation_deg", "spectrum_db"])
        for el_index, elevation in enumerate(elevations_deg):
            for az_index, azimuth in enumerate(azimuths_deg):
                writer.writerow([azimuth, elevation, spectrum_db[el_index, az_index]])

