"""Plots for software simulation outputs. Every figure is visibly labeled."""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


WATERMARK = "Simulation result (not measured data)"


def _finish(fig, path: Path) -> None:
    # Reserve a dedicated footer so the simulation warning never covers an axis label.
    fig.subplots_adjust(bottom=0.20)
    fig.text(0.5, 0.025, WATERMARK, ha="center", color="crimson", fontsize=9, weight="bold")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_geometry(positions_m: np.ndarray, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(positions_m[:, 0], positions_m[:, 1], s=80)
    for index, (x, y, _) in enumerate(positions_m):
        ax.annotate(f"CH{index}", (x, y), xytext=(5, 5), textcoords="offset points")
    ax.set_aspect("equal")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("Ideal 8-element UCA geometry (simulation reference)")
    ax.grid(True, alpha=0.3)
    _finish(fig, path)


def plot_beam_pattern(azimuths_deg: np.ndarray, pattern_db: np.ndarray, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(azimuths_deg, pattern_db)
    ax.set_ylim(-60, 3)
    ax.set_xlabel("Azimuth (deg)")
    ax.set_ylabel("Normalized response (dB)")
    ax.set_title("Conventional beamformer pattern (software reference)")
    ax.grid(True, alpha=0.3)
    _finish(fig, path)


def plot_channelizer(freq_hz: np.ndarray, spectra: np.ndarray, path: Path) -> None:
    power = 20.0 * np.log10(np.maximum(np.mean(np.abs(spectra), axis=0), 1e-12))
    power -= power.max()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(freq_hz / 1e3, power, marker=".")
    ax.set_xlabel("Baseband frequency (kHz)")
    ax.set_ylabel("Normalized magnitude (dB)")
    ax.set_title("Polyphase FIR + FFT channelizer demo")
    ax.grid(True, alpha=0.3)
    _finish(fig, path)


def plot_music(
    azimuths_deg: np.ndarray,
    elevations_deg: np.ndarray,
    spectrum_db: np.ndarray,
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    image = ax.imshow(
        spectrum_db,
        origin="lower",
        aspect="auto",
        extent=[azimuths_deg[0], azimuths_deg[-1], elevations_deg[0], elevations_deg[-1]],
        vmin=-30,
        vmax=0,
        cmap="viridis",
    )
    fig.colorbar(image, ax=ax, label="Normalized MUSIC spectrum (dB)")
    ax.set_xlabel("Azimuth (deg)")
    ax.set_ylabel("Elevation (deg)")
    ax.set_title("2-D MUSIC grid search (ideal planar UCA simulation)")
    _finish(fig, path)

