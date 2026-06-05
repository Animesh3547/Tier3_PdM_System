# --- window-code-block: orchestrator.py ---
import numpy as np
import time
from sensor_health import SensorHealthGate
from anomaly_funnel import ScadaAnomalyFunnel
from kinematic_dsp import KinematicPhysicsEngine
from fault_injector import inject_bpfo_fault

def simulate_data_stream(batch_size=10000):
    """Generates continuous fake sensor data to simulate a live factory machine."""
    while True:
        # Simulating normal background noise with a slight unbalance
        yield np.random.normal(0, 1.0, batch_size)
        time.sleep(1) # Simulating a 1-second data ingestion interval

if __name__ == "__main__":
    print("=== TIER 3 EDGE PIPELINE INITIALIZED ===")
    
    # 1. Initialize Modules
    health_gate = SensorHealthGate()
    ml_funnel = ScadaAnomalyFunnel(model_path="models/iforest_baseline.pkl")
    
    # Bearing geometry: 8 rollers, 10mm roller, 40mm pitch, 0 deg contact angle
    physics_engine = KinematicPhysicsEngine(sample_rate=10000, rpm=1800, 
        bearing_geometry={'n_rollers': 8, 'roller_diameter': 10, 'pitch_diameter': 40, 'contact_angle': 0})
    
    # 2. Boot Sequence
    try:
        ml_funnel.load_baseline()
    except RuntimeError as e:
        print(f"\n[BOOT SEQUENCE FAILED] {e}")
        print("Please run train_baseline.py to establish a healthy baseline.")
        exit(1)
        
    print("[SYSTEM] All gates active. Beginning continuous monitoring...")
    
    # 3. Continuous Monitoring Loop
    try:
        for batch_id, raw_signal in enumerate(simulate_data_stream()):
            print(f"\n--- Processing Batch {batch_id + 1} ---")
            
            # GATE 1: Hardware Validation
            is_valid, health_status = health_gate.validate_signal(raw_signal)
            if not is_valid:
                print(f"[CRITICAL ABORT] Hardware failure detected: {health_status}")
                # Future: Send JSON alert to MERN backend here
                continue 
            
            # GATE 2: Statistical Anomaly Tripwire
            # SIMULATION: Inject fault after Batch 25
            if batch_id == 25:
                print("\n[SIMULATION] Injecting Bearing Outer Race Fracture...")
                raw_signal = inject_bpfo_fault(raw_signal, 10000, physics_engine.bpfo)
            
            is_anomalous, features = ml_funnel.monitor_stream(raw_signal)
            if not is_anomalous:
                print("[STATUS] Machine State: NOMINAL")
                continue
                
            print("[WARNING] Statistical Anomaly Detected! Handing off to Physics Engine...")
            
            # GATE 3: Kinematic Root Cause Verification
            fault_flags = physics_engine.analyze_faults(raw_signal)
            
            if any(fault_flags.values()):
                print(f"[ALARM] Mathematical Fault Verified: {fault_flags}")
                # Future: Send verified JSON alert to LLM / MERN backend here
            else:
                print("[STATUS] Anomaly dismissed. No kinematic fault frequencies matched (Transient Noise).")

    except KeyboardInterrupt:
        print("\n[SYSTEM] Edge pipeline safely terminated by user.")

# ONE-LINE SUMMARY: The Orchestrator manages the pipeline flow, running incoming data through the hardware, ML, and physics gates sequentially.