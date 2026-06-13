# --- window-code-block: temporal_persistence_gate.py ---
from collections import deque

class AlarmPersistenceGate:
    def __init__(self, window_size=5, trigger_threshold=4):
        """
        DETERMINISTIC TEMPORAL LAYER:
        Prevents transient mechanical shocks from causing false alarms.
        Requires 'trigger_threshold' anomalies within 'window_size' frames to fire.
        """
        self.window_size = window_size
        self.trigger_threshold = trigger_threshold
        # deque automatically pushes old data out when maxlen is reached
        self.state_queue = deque(maxlen=window_size)
        
    def update_state(self, is_anomalous: bool):
        """
        Takes the boolean output from the DSP/Isolation Forest.
        Returns True ONLY if the anomaly is mathematically persistent.
        """
        # Append 1 for an anomaly, 0 for normal
        self.state_queue.append(1 if is_anomalous else 0)
        
        # Only trigger if the queue is full and threshold is met
        if len(self.state_queue) == self.window_size:
            if sum(self.state_queue) >= self.trigger_threshold:
                return True # Persistent fault confirmed.
                
        return False # Transient noise or baseline state. Do nothing.

# ONE-LINE SUMMARY: State persistence mathematically eliminates transient false alarms by demanding continuous proof of failure across multiple time windows.