# --- window-code-block: train_baseline.py ---
import numpy as np
import os
import sys
import json
from anomaly_funnel import ScadaAnomalyFunnel

def capture_healthy_baseline(sample_rate):
    print(f"[SYSTEM] Simulating DAQ ingestion of 50 blocks at {sample_rate} Hz...")
    return [np.random.normal(0, 1.0, sample_rate) for _ in range(50)]

if __name__ == "__main__":
    print("=== TIER 3 HITL BASELINE CALIBRATION ===")
    
    # 1. Load Configuration
    try:
        with open('config.json') as f: config = json.load(f)
    except FileNotFoundError:
        print("[ERROR] config.json missing. Cannot establish machine parameters.")
        sys.exit(1)

    confirmation = input("Are you physically present at the machine and verifying it is healthy? (Type YES to proceed): ")
    if confirmation.strip() != "YES":
        print("[ABORT] Calibration cancelled.")
        sys.exit(0)
        
    os.makedirs("models", exist_ok=True)
    
    # 2. Initialize Funnel with Config Parameters
    funnel = ScadaAnomalyFunnel(
        sample_rate=config['sample_rate'],
        rpm=config['rpm'],
        model_path="models/iforest_baseline.pkl"
    )
    
    verified_data = capture_healthy_baseline(config['sample_rate'])
    funnel.authorize_manual_training(verified_data)
    print("[SUCCESS] Machine baseline locked.")