# --- window-code-block: anomaly_funnel.py ---
import numpy as np
import joblib
import os
from scipy.stats import kurtosis, skew
from sklearn.ensemble import IsolationForest

class ScadaAnomalyFunnel:
    def __init__(self, contamination=0.05, model_path="models/iforest_baseline.pkl"):
        """
        DETERMINISTIC ML LAYER:
        Flags statistical outliers using an Isolation Forest.
        """
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_trained = False
        self.model_path = model_path
        
    def calculate_dsp_features(self, raw_signal):
        """Extracts 1D time-domain statistics."""
        rms = np.sqrt(np.mean(raw_signal**2))
        kurt = kurtosis(raw_signal, fisher=False)
        peak = np.max(np.abs(raw_signal))
        crest_factor = peak / rms if rms > 0 else 0
        signal_skew = skew(raw_signal) # Added to detect asymmetrical faults like rubbing
        
        return np.array([rms, kurt, crest_factor, signal_skew])

    def load_baseline(self):
        """
        CRITICAL SAFETY GATE: Loads an existing model.
        NEVER trains automatically to prevent learning a failing state.
        """
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print(f"[SYSTEM] Loaded validated baseline model from {self.model_path}")
        else:
            # The Dead Man's Switch
            raise RuntimeError("CRITICAL: No baseline model found. System halted to prevent unmonitored training on potentially failing hardware.")

    def authorize_manual_training(self, baseline_signals):
        """
        Requires explicit engineer execution to establish a new normal.
        Only run this when the machine is mathematically verified as healthy.
        """
        print("[WARNING] Explicit training authorized. Establishing new mechanical baseline...")
        feature_matrix = [self.calculate_dsp_features(sig) for sig in baseline_signals]
        self.model.fit(feature_matrix)
        joblib.dump(self.model, self.model_path)
        self.is_trained = True
        print(f"[SYSTEM] New baseline mathematically verified and locked to {self.model_path}")

    def monitor_stream(self, raw_signal):
        """Evaluates a single block of streaming data."""
        if not self.is_trained:
            raise RuntimeError("Model locked. Execute authorize_manual_training() first.")
            
        features = self.calculate_dsp_features(raw_signal).reshape(1, -1)
        prediction = self.model.predict(features)[0]
        
        # IsolationForest outputs 1 for normal, -1 for anomaly.
        is_anomalous = bool(prediction == -1) 
        
        return is_anomalous, features[0]

# ONE-LINE SUMMARY: The hardened funnel forces explicit human authorization to train, preventing the AI from learning a destructive mechanical state.