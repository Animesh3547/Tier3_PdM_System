# --- window-code-block: health_tracker.py ---
import numpy as np
from collections import deque

class PrognosticHealthTracker:
    def __init__(self, history_capacity=50):
        """
        INDUSTRIAL TRENDING LAYER:
        Maintains historical context to calculate a 0-100% Health Score 
        and identify active degradation slopes.
        """
        self.history = deque(maxlen=history_capacity)
        self.baseline_norm = None

    def calibrate_baseline(self, baseline_features):
        """Locks in the '100% Healthy' 7D mathematical signature."""
        self.baseline_norm = np.linalg.norm(baseline_features)

    def update(self, current_features):
        """
        Updates the trend history and calculates the current machine health.
        Returns: tuple (health_score: float, trend_status: str)
        """
        self.history.append(current_features)
        
        # Failsafe if baseline isn't loaded
        if self.baseline_norm is None or self.baseline_norm == 0:
            return 100.0, "AWAITING_BASELINE"

        # 1. Calculate Current Deviation (Distance from baseline)
        current_norm = np.linalg.norm(current_features)
        deviation_ratio = (current_norm - self.baseline_norm) / self.baseline_norm
        
        # Map deviation to a 0-100 score (Tuning scalar: 100 multiplier for PoC visibility)
        health_score = max(0.0, min(100.0, 100.0 - (deviation_ratio * 100)))

        # 2. Calculate Trend Direction (Slope over time)
        if len(self.history) < 10:
            return round(health_score, 1), "STABLE (GATHERING DATA)"

        # Compare the newest data vs the oldest data in the buffer
        recent_avg = np.mean([np.linalg.norm(f) for f in list(self.history)[-5:]])
        older_avg = np.mean([np.linalg.norm(f) for f in list(self.history)[:5]])
        
        trend_slope = recent_avg - older_avg

        # Threshold for status change
        if trend_slope > (self.baseline_norm * 0.05): # 5% growth
            trend_status = "DEGRADING ⬇️"
        elif trend_slope < -(self.baseline_norm * 0.05):
            trend_status = "IMPROVING ⬆️"
        else:
            trend_status = "STABLE 🟢"

        return round(health_score, 1), trend_status

# ONE-LINE SUMMARY: The Health Tracker uses a rolling buffer to measure how far the machine's 7D features have drifted from perfect health, yielding a clear metric for the dashboard.