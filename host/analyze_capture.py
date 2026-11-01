#!/usr/bin/env python3
"""Run MUSIC analysis on an eight-channel CSV capture."""

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rfsoc8_ref.csvio import read_complex_channels, write_music_grid
from rfsoc8_ref.geometry import uca_positions
from rfsoc8_ref.music import estimate_peak, music_spectrum_2d


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an 8-channel IQ CSV file")
    parser.add_argument("capture", type=Path)
    parser.add_argument("--carrier-hz", type=float, required=True)
    parser.add_argument("--radius-m", type=float, required=True)
    parser.add_argument("--output", type=Path, default=Path("music_from_capture.csv"))
    args = parser.parse_args()

    snapshots = read_complex_channels(args.capture, channel_count=8)
    positions = uca_positions(8, args.radius_m)
    azimuths = np.arange(-180.0, 181.0, 2.0)
    elevations = np.arange(0.0, 61.0, 2.0)
    spectrum = music_spectrum_2d(
        snapshots, positions, args.carrier_hz, azimuths, elevations, source_count=1
    )
    azimuth, elevation = estimate_peak(spectrum, azimuths, elevations)
    write_music_grid(args.output, spectrum, azimuths, elevations)
    print(f"Estimated direction: az={azimuth:.1f} deg, el={elevation:.1f} deg")


if __name__ == "__main__":
    main()

