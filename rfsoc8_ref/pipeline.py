"""End-to-end software-only reference pipeline. No hardware access occurs here."""

import json
from pathlib import Path
import numpy as np

from .beamforming import apply_beamformer, azimuth_pattern_db, conventional_weights
from .channelizer import frequency_axis_hz, pfb_channelize
from .config import SimulationConfig
from .csvio import write_complex_channels, write_music_grid
from .geometry import uca_positions
from .music import estimate_peak, music_spectrum_2d
from .signals import generate_cw, generate_fmcw, synthesize_array_data
from .visualization import plot_beam_pattern, plot_channelizer, plot_geometry, plot_music


def run_reference_pipeline(cfg: SimulationConfig, output_dir: Path) -> dict:
    """Run deterministic synthetic data through all educational modules."""
    cfg.validate()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    positions = uca_positions(cfg.element_count, cfg.radius_m)
    cw = generate_cw(cfg.snapshot_count, cfg.sample_rate_hz, cfg.tone_hz)
    # Generated as a second demonstrator, then mixed weakly with CW to exercise PFB bins.
    fmcw = generate_fmcw(cfg.snapshot_count, cfg.sample_rate_hz)
    waveform = cw + 0.25 * fmcw
    snapshots = synthesize_array_data(
        waveform,
        positions,
        cfg.carrier_hz,
        cfg.source_az_deg,
        cfg.source_el_deg,
        cfg.snr_db,
        cfg.random_seed,
    )

    weights = conventional_weights(
        positions, cfg.carrier_hz, cfg.source_az_deg, cfg.source_el_deg
    )
    beamformed = apply_beamformer(snapshots, weights)
    channel_spectra = pfb_channelize(
        beamformed, cfg.channelizer_bins, cfg.channelizer_taps_per_phase
    )
    channel_freq_hz = frequency_axis_hz(cfg.channelizer_bins, cfg.sample_rate_hz)

    azimuths = np.arange(
        cfg.scan_az_min_deg, cfg.scan_az_max_deg + cfg.scan_az_step_deg / 2, cfg.scan_az_step_deg
    )
    elevations = np.arange(
        cfg.scan_el_min_deg, cfg.scan_el_max_deg + cfg.scan_el_step_deg / 2, cfg.scan_el_step_deg
    )
    spectrum_db = music_spectrum_2d(
        snapshots, positions, cfg.carrier_hz, azimuths, elevations, cfg.source_count
    )
    estimated_az, estimated_el = estimate_peak(spectrum_db, azimuths, elevations)

    write_complex_channels(output_dir / "synthetic_snapshots.csv", snapshots)
    write_music_grid(output_dir / "music_spectrum.csv", spectrum_db, azimuths, elevations)
    plot_geometry(positions, output_dir / "array_geometry.png")
    pattern_az = np.linspace(-180.0, 180.0, 721)
    pattern_db = azimuth_pattern_db(
        positions, cfg.carrier_hz, cfg.source_az_deg, cfg.source_el_deg, pattern_az
    )
    plot_beam_pattern(pattern_az, pattern_db, output_dir / "beam_pattern.png")
    plot_channelizer(channel_freq_hz, channel_spectra, output_dir / "channelizer.png")
    plot_music(azimuths, elevations, spectrum_db, output_dir / "music_spectrum.png")

    summary = {
        "notice": "软件仿真结果，未接入 ANTSDR T510 实板",
        "original_team_code": False,
        "hardware_verified": False,
        "synthetic_truth_az_deg": cfg.source_az_deg,
        "synthetic_truth_el_deg": cfg.source_el_deg,
        "estimated_az_deg": estimated_az,
        "estimated_el_deg": estimated_el,
        "config": cfg.to_dict(),
    }
    with (output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
    return summary

