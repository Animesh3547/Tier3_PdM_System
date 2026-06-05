# --- window-code-block: sensor_health.py ---
import numpy as np

class SensorHealthGate:
    def __init__(self, min_rms=0.01, max_clip_limit=4.95):
        """
        DETERMINISTIC HARDWARE LAYER:
        Validates the physical integrity of the sensor connection.
        """
        self.min_rms = min_rms
        self.max_clip_limit = max_clip_limit

    def validate_signal(self, raw_signal):
        """
        Checks for dead signals, disconnected sensors, or short-circuit clipping.
        Returns: tuple (is_valid: bool, error_reason: str)
        """
        # Check 1: Dead Sensor or Unglued (Zero Energy)
        rms = np.sqrt(np.mean(raw_signal**2))
        if rms < self.min_rms:
            return False, "SENSOR_DEAD_OR_UNGLUED"

        # Check 2: Short Circuit or Overload (Clipping)
        clip_count = np.sum(np.abs(raw_signal) >= self.max_clip_limit)
        if (clip_count / len(raw_signal)) > 0.05:
            return False, "SENSOR_CLIPPING"

        # Check 3: Flatline (Frozen ADC or communication freeze)
        if np.all(raw_signal == raw_signal[0]):
            return False, "SENSOR_FLATLINE"

        return True, "SENSOR_HEALTHY"

# ONE-LINE SUMMARY: The SensorHealthGate mathematically prevents dead hardware data from triggering false AI diagnostics.