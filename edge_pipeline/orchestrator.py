# --- window-code-block: orchestrator.py ---
import numpy as np
import time
import json
import sys
from sensor_health import SensorHealthGate
from anomaly_funnel import ScadaAnomalyFunnel
from kinematic_dsp import KinematicPhysicsEngine
from temporal_persistence_gate import AlarmPersistenceGate
from fault_injector import inject_bpfo_fault
from health_tracker import PrognosticHealthTracker

def simulate_data_stream(sample_rate):
    while True:
        yield np.random.normal(0, 1.0, sample_rate)
        time.sleep(1)

if __name__ == "__main__":
    print("=== TIER 3 EDGE PIPELINE INITIALIZED ===")
    
    # 1. Load Config
    try:
        with open('config.json') as f: config = json.load(f)
    except FileNotFoundError:
        print("[CRITICAL] config.json not found. Halting.")
        sys.exit(1)
        
    # 2. Initialize Modules using Config
    health_gate = SensorHealthGate()
    persistence = AlarmPersistenceGate(window_size=5, trigger_threshold=config['persistence_threshold'])
    health_tracker = PrognosticHealthTracker(history_capacity=50)

    ml_funnel = ScadaAnomalyFunnel(
        sample_rate=config['sample_rate'], 
        rpm=config['rpm'], 
        model_path="models/iforest_baseline.pkl"
    )

    simulated_healthy_norm = ml_funnel.calculate_dsp_features(np.random.normal(0, 1.0, config['sample_rate']))
    health_tracker.calibrate_baseline(simulated_healthy_norm)
    
    physics_engine = KinematicPhysicsEngine(
        sample_rate=config['sample_rate'], 
        rpm=config['rpm'], 
        resonance_band=config['resonance_band'],
        bearing_geometry=config['bearing_geom']
    )
    
    # 3. Boot Sequence
    try:
        ml_funnel.load_baseline()
    except RuntimeError as e:
        print(f"\n[BOOT SEQUENCE FAILED] {e}")
        sys.exit(1)
        
    print(f"[SYSTEM] Monitoring Machine: {config['machine_id']} at {config['rpm']} RPM")
    
    # 4. Continuous Monitoring Loop
    try:
        for batch_id, raw_signal in enumerate(simulate_data_stream(config['sample_rate'])):
            print(f"\n--- Processing Batch {batch_id + 1} ---")
            
            is_valid, health_status = health_gate.validate_signal(raw_signal)
            if not is_valid:
                print(f"[CRITICAL ABORT] Hardware failure: {health_status}")
                continue 
            
            # SIMULATION: Inject fault after Batch 25
            if batch_id >= 10:
                if batch_id == 10: print("\n[SIMULATION] Injecting Bearing Outer Race Fracture...")
                raw_signal = inject_bpfo_fault(raw_signal, config['sample_rate'], physics_engine.bpfo)
            
            is_anomalous, features = ml_funnel.monitor_stream(raw_signal)
            
            # --- THE TRENDING LAYER ---
            health_score, trend_status = health_tracker.update(features)
            print(f"[HEALTH SCORE: {health_score}% | TREND: {trend_status}]")

            is_confirmed = persistence.update_state(is_anomalous)
            
            # WATERFALL LOGIC
            if not is_anomalous:
                print("[STATUS] Machine State: NOMINAL")
                continue
                
            if is_anomalous and not is_confirmed:
                print(f"[WARNING] Transient spike detected (Window {sum(persistence.state_queue)}/{persistence.trigger_threshold}). Awaiting persistence...")
                continue
                
            if is_confirmed:
                print("[CRITICAL] Persistent Anomaly Confirmed! Handing off to Physics Engine...")
                fault_flags = physics_engine.analyze_faults(raw_signal)
                
                if any(fault_flags.values()):
                    print(f"[ALARM] Mathematical Fault Verified: {fault_flags}")
                    # Future: Send JSON alert to MERN Backend
                else:
                    print("[STATUS] Persistent Anomaly lacks kinematic match (Unknown Fault / Severe Noise).")

    except KeyboardInterrupt:
        print("\n[SYSTEM] Edge pipeline safely terminated by user.")