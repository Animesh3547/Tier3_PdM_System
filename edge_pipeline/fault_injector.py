# --- window-code-block: fault_injector.py ---
import numpy as np

def inject_bpfo_fault(signal, sample_rate, bpfo_hz):
    """
    Injects a transient impact signal at the BPFO frequency.
    Simulates a localized spall in the outer race of the bearing.
    """
    n = len(signal)
    t = np.arange(n) / sample_rate
    
    # Create impact pulses at the BPFO frequency
    # A fracture impacts once every 1/BPFO seconds
    impact_indices = (np.arange(0, n, sample_rate / bpfo_hz)).astype(int)
    
    # Inject high-energy spikes
    faulty_signal = signal.copy()
    faulty_signal[impact_indices] += 5.0 # Magnitude of the fault
    
    return faulty_signal