# --- window-code-block: train_baseline.py ---
import numpy as np
import os
import sys
from anomaly_funnel import ScadaAnomalyFunnel

def capture_healthy_baseline():
    """
    Simulates capturing live data from the DAQ system.
    Currently uses synthetic normal data for local testing.
    """
    print("[SYSTEM] Simulating DAQ ingestion of 50 healthy data blocks...")
    healthy_signals = [np.random.normal(0, 1.0, 10000) for _ in range(50)]
    return healthy_signals

if __name__ == "__main__":
    print("=== TIER 3 HITL BASELINE CALIBRATION ===")
    print("WARNING: Executing this will overwrite the machine's statistical baseline.")
    
    # The True Human-In-The-Loop Lock
    confirmation = input("Are you physically present at the machine and verifying it is healthy? (Type YES to proceed): ")
    
    if confirmation.strip() != "YES":
        print("[ABORT] Calibration cancelled. System state unchanged.")
        sys.exit(0)
        
    print("[SYSTEM] Engineer authorization confirmed via terminal.")
    
    os.makedirs("models", exist_ok=True)
    funnel = ScadaAnomalyFunnel(model_path="models/iforest_baseline.pkl")
    
    verified_data = capture_healthy_baseline()
    funnel.authorize_manual_training(verified_data)
    
    print("[SUCCESS] Machine baseline locked. Safe to begin continuous monitoring.")

# ONE-LINE SUMMARY: The script now strictly pauses execution until an engineer types an explicit confirmation, locking the training gate.