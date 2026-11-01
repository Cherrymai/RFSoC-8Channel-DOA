"""Configuration for the software-only educational simulation."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass
class SimulationConfig:
    element_count: int = 8
    carrier_hz: float = 2.4e9
    sample_rate_hz: float = 1.0e6
    radius_m: float = 0.04
    snapshot_count: int = 4096
    tone_hz: float = 100e3
    source_az_deg: float = 35.0
    source_el_deg: float = 15.0
    snr_db: float = 15.0
    scan_az_min_deg: float = -180.0
    scan_az_max_deg: float = 180.0
    scan_az_step_deg: float = 2.0
    scan_el_min_deg: float = 0.0
    scan_el_max_deg: float = 60.0
    scan_el_step_deg: float = 2.0
    source_count: int = 1
    channelizer_bins: int = 64
    channelizer_taps_per_phase: int = 8
    random_seed: int = 48396

    def validate(self) -> None:
        if self.element_count != 8:
            raise ValueError("This reference package intentionally models exactly 8 elements")
        if self.snapshot_count < 256:
            raise ValueError("snapshot_count must be at least 256")
        if self.carrier_hz <= 0 or self.sample_rate_hz <= 0 or self.radius_m <= 0:
            raise ValueError("carrier, sample rate, and radius must be positive")
        if not (-180 <= self.source_az_deg <= 180):
            raise ValueError("source azimuth must be in [-180, 180] degrees")
        if not (0 <= self.source_el_deg <= 90):
            raise ValueError("this planar-UCA demo scans nonnegative elevation only")
        if self.source_count < 1 or self.source_count >= self.element_count:
            raise ValueError("source_count must be between 1 and 7")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_json(cls, path: Path) -> "SimulationConfig":
        with Path(path).open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        cfg = cls(**data)
        cfg.validate()
        return cfg

