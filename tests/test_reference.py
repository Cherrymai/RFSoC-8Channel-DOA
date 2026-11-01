"""Tests for the software reference only; passing does not imply hardware readiness."""

import tempfile
import unittest
from pathlib import Path
import numpy as np

from rfsoc8_ref.beamforming import apply_beamformer, conventional_weights
from rfsoc8_ref.channelizer import pfb_channelize
from rfsoc8_ref.csvio import read_complex_channels, write_complex_channels
from rfsoc8_ref.geometry import steering_vector, uca_positions
from rfsoc8_ref.music import estimate_peak, music_spectrum_2d
from rfsoc8_ref.signals import generate_cw, synthesize_array_data


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.positions = uca_positions(8, 0.04)
        self.carrier = 2.4e9

    def test_geometry_and_steering(self):
        self.assertEqual(self.positions.shape, (8, 3))
        vector = steering_vector(self.positions, self.carrier, 20, 10)
        np.testing.assert_allclose(np.abs(vector), 1.0)

    def test_beamformer_preserves_look_signal(self):
        waveform = generate_cw(1024, 1e6, 100e3)
        data = synthesize_array_data(waveform, self.positions, self.carrier, 30, 10, 80)
        weights = conventional_weights(self.positions, self.carrier, 30, 10)
        output = apply_beamformer(data, weights)
        self.assertGreater(np.mean(np.abs(output)), 0.9)

    def test_channelizer_shape(self):
        waveform = generate_cw(2048, 1e6, 100e3)
        spectra = pfb_channelize(waveform, 32, 4)
        self.assertEqual(spectra.shape[1], 32)
        self.assertGreater(spectra.shape[0], 1)

    def test_music_finds_synthetic_direction(self):
        waveform = generate_cw(2048, 1e6, 70e3)
        data = synthesize_array_data(waveform, self.positions, self.carrier, 40, 20, 30)
        az = np.arange(-90, 91, 2)
        el = np.arange(0, 41, 2)
        spectrum = music_spectrum_2d(data, self.positions, self.carrier, az, el)
        estimate = estimate_peak(spectrum, az, el)
        self.assertLessEqual(abs(estimate[0] - 40), 2)
        self.assertLessEqual(abs(estimate[1] - 20), 4)

    def test_csv_round_trip(self):
        original = np.arange(80).reshape(8, 10) + 1j * np.arange(80, 160).reshape(8, 10)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "iq.csv"
            write_complex_channels(path, original)
            restored = read_complex_channels(path)
        np.testing.assert_allclose(restored, original)


if __name__ == "__main__":
    unittest.main()

