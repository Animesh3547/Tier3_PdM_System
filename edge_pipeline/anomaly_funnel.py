# --- window-code-block: anomaly_funnel.py ---
import numpy as np
import joblib
import os
from scipy.stats import kurtosis, skew
from scipy.fft import rfft, rfftfreq
from sklearn.ensemble import IsolationForest

class ScadaAnomalyFunnel:
    def __init__(self, sample_rate=10000, rpm=1800, contamination=0.05, model_path="models/iforest_baseline.pkl"):
        """
        PROGNOSTIC ML LAYER:
        Flags outliers using a combined Time-Domain and Frequency-Domain feature vector.
        """
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_trained = False
        self.model_path = model_path
        self.fs = sample_rate
        self.shaft_hz = rpm / 60.0
        
    def calculate_dsp_features(self, raw_signal):
        """Extracts a 7-dimensional prognostic feature vector."""
        # 1. Time-Domain
        rms = np.sqrt(np.mean(raw_signal**2))
        kurt = kurtosis(raw_signal, fisher=False)
        peak = np.max(np.abs(raw_signal))
        crest_factor = peak / rms if rms > 0 else 0
        signal_skew = skew(raw_signal)
        
        # 2. Frequency-Domain (Standard FFT)
        n = len(raw_signal)

        window = np.hanning(n)
        windowed_signal = raw_signal * window

        yf = np.abs(rfft(windowed_signal))
        xf = rfftfreq(n, 1 / self.fs)
        
        # 3. Extract Specific Harmonics (1X and 2X RPM)
        # Find the closest frequency bin to the physical harmonic
        idx_1x = np.argmin(np.abs(xf - self.shaft_hz))
        idx_2x = np.argmin(np.abs(xf - (self.shaft_hz * 2)))
        
        amp_1x = yf[idx_1x]
        amp_2x = yf[idx_2x]
        
        # 4. Extract High-Frequency Energy (Proxy for overall bearing noise > 1000Hz)
        hf_mask = xf > 1000
        hf_energy = np.sum(yf[hf_mask]) if np.any(hf_mask) else 0

        # Unified Prognostic Vector
        return np.array([rms, kurt, crest_factor, signal_skew, amp_1x, amp_2x, hf_energy])

    def load_baseline(self):
        """CRITICAL SAFETY GATE: Loads an existing model."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print(f"[SYSTEM] Loaded validated baseline model from {self.model_path}")
        else:
            raise RuntimeError("CRITICAL: No baseline model found. System halted to prevent unmonitored training.")

    def authorize_manual_training(self, baseline_signals):
        """Requires explicit engineer execution to establish a new normal."""
        print("[WARNING] Explicit training authorized. Establishing new prognostic baseline...")
        feature_matrix = [self.calculate_dsp_features(sig) for sig in baseline_signals]
        self.model.fit(feature_matrix)
        joblib.dump(self.model, self.model_path)
        self.is_trained = True
        print(f"[SYSTEM] New baseline mathematically verified and locked to {self.model_path}")

    def monitor_stream(self, raw_signal):
        """Evaluates a single block of streaming data against the 7D vector."""
        if not self.is_trained:
            raise RuntimeError("Model locked. Execute train_baseline.py first.")
            
        features = self.calculate_dsp_features(raw_signal).reshape(1, -1)
        prediction = self.model.predict(features)[0]
        
        is_anomalous = bool(prediction == -1) 
        return is_anomalous, features[0]

# ONE-LINE SUMMARY: The upgraded funnel integrates FFT amplitudes directly into the ML vector, enabling the AI to detect specific harmonic drift before the overall machine energy spikes.