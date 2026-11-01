#!/usr/bin/env python3
"""SIMULATION/REFERENCE ONLY. Command-line entry for the educational model."""

import argparse
from pathlib import Path

from rfsoc8_ref.config import SimulationConfig
from rfsoc8_ref.pipeline import run_reference_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RFSoC 8-channel educational software simulation (NOT hardware verified)"
    )
    parser.add_argument("--config", type=Path, help="optional JSON configuration")
    parser.add_argument("--output", type=Path, default=Path("generated_demo"))
    args = parser.parse_args()

    cfg = SimulationConfig.from_json(args.config) if args.config else SimulationConfig()
    result = run_reference_pipeline(cfg, args.output)
    print("Data source: software simulation (ANTSDR T510 not connected)")
    print(f"Synthetic truth: az={cfg.source_az_deg:.1f} deg, el={cfg.source_el_deg:.1f} deg")
    print(
        f"MUSIC grid estimate: az={result['estimated_az_deg']:.1f} deg, "
        f"el={result['estimated_el_deg']:.1f} deg"
    )
    print(f"Reference artifacts written to: {args.output.resolve()}")


if __name__ == "__main__":
    main()

