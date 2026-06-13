# --- window-code-block: kinematic_dsp.py ---
import numpy as np
from scipy.signal import butter, filtfilt, hilbert, find_peaks
from scipy.fft import rfft, rfftfreq

class KinematicPhysicsEngine: 
    def __init__(self, sample_rate, rpm, bearing_geometry, resonance_band):
        self.fs = sample_rate
        self.shaft_hz = rpm / 60.0
        self.geom = bearing_geometry
        self.resonance_band = resonance_band # Injected from config.json
        self._calculate_theoretical_frequencies()

    def _calculate_theoretical_frequencies(self):
        n = self.geom['n_rollers']
        d = self.geom['roller_diameter']
        D = self.geom['pitch_diameter']
        cos_phi = np.cos(np.radians(self.geom['contact_angle']))
        
        self.bpfo = (n / 2) * self.shaft_hz * (1 - (d / D) * cos_phi)
        self.bpfi = (n / 2) * self.shaft_hz * (1 + (d / D) * cos_phi)
        self.ftf = 0.5 * self.shaft_hz * (1 - (d / D) * cos_phi)
        self.bsf = (D / (2 * d)) * self.shaft_hz * (1 - ((d / D) * cos_phi)**2)
        
        self.harmonic_1x = self.shaft_hz
        self.harmonic_2x = self.shaft_hz * 2
        self.harmonic_3x = self.shaft_hz * 3

    def _raw_spectrum(self, raw_signal):
        n = len(raw_signal)

        window = np.hanning(n)
        windowed_signal = raw_signal * window

        yf = np.abs(rfft(windowed_signal))
        xf = rfftfreq(n, 1 / self.fs)
        return xf, yf

    def _envelope_spectrum(self, raw_signal):
        nyq = 0.5 * self.fs
        lowcut = self.resonance_band[0]
        highcut = self.resonance_band[1]
        
        # Dynamic filter based on config variables
        b, a = butter(4, [lowcut / nyq, highcut / nyq], btype='band')
        filtered_sig = filtfilt(b, a, raw_signal)
        analytic_signal = hilbert(filtered_sig)
        amplitude_envelope = np.abs(analytic_signal)

        n = len(amplitude_envelope)

        window = np.hanning(n)
        windowed_envelope = amplitude_envelope * window

        yf = np.abs(rfft(windowed_envelope))
        xf = rfftfreq(n, 1 / self.fs)
        return xf, yf

# Current FFT resolution:
# Fs = 10000 Hz
# N = 10000 samples
# Δf = 1 Hz
# Therefore ±2 Hz matching tolerance is acceptable.

    def analyze_faults(self, raw_signal, tolerance_hz=2.0):
        env_xf, env_yf = self._envelope_spectrum(raw_signal)
        env_peaks, _ = find_peaks(env_yf, height=np.mean(env_yf) + 2*np.std(env_yf))
        env_peak_freqs = env_xf[env_peaks]
        
        raw_xf, raw_yf = self._raw_spectrum(raw_signal)
        raw_peaks, _ = find_peaks(raw_yf, height=np.mean(raw_yf) + 2*np.std(raw_yf))
        raw_peak_freqs = raw_xf[raw_peaks]
        
        fault_flags = {
            "Outer_Race_BPFO": any(abs(f - self.bpfo) < tolerance_hz for f in env_peak_freqs),
            "Inner_Race_BPFI": any(abs(f - self.bpfi) < tolerance_hz for f in env_peak_freqs),
            "Cage_Defect_FTF": any(abs(f - self.ftf) < tolerance_hz for f in env_peak_freqs),
            "Rolling_Element_BSF": any(abs(f - self.bsf) < tolerance_hz for f in env_peak_freqs),
            "Unbalance_1X_RPM": any(abs(f - self.harmonic_1x) < tolerance_hz for f in raw_peak_freqs),
            "Misalignment_2X_RPM": any(abs(f - self.harmonic_2x) < tolerance_hz for f in raw_peak_freqs)
        }
        return fault_flags

# ONE-LINE SUMMARY: The physics engine now dynamically constructs its envelope filter using the machine-specific resonance band defined in the JSON configuration.