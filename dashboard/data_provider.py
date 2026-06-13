import os
import sys
import json
import numpy as np

# Go from dashboard -> Tier3_PdM_System
PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

# Add edge_pipeline to imports
EDGE_PIPELINE = os.path.join(
    os.path.dirname(PROJECT_ROOT),
    "edge_pipeline"
)

sys.path.append(EDGE_PIPELINE)

from anomaly_funnel import ScadaAnomalyFunnel
from kinematic_dsp import KinematicPhysicsEngine


def load_config():
    with open(
        os.path.join(
            EDGE_PIPELINE,
            "config.json"
        ),
        "r"
    ) as f:
        return json.load(f)


def generate_signal():
    config = load_config()

    fs = config["sample_rate"]

    t = np.arange(fs) / fs

    signal = (
        2*np.sin(2*np.pi*30*t)
        + np.sin(2*np.pi*60*t)
        + 0.3*np.random.randn(fs)
    )

    return signal


def get_fft_data():

    config = load_config()

    signal = generate_signal()

    window = np.hanning(len(signal))
    signal = signal * window

    xf = np.fft.rfftfreq(
        len(signal),
        d=1/config["sample_rate"]
    )

    yf = np.abs(np.fft.rfft(signal))

    return xf, yf


def get_features():

    config = load_config()

    signal = generate_signal()

    funnel = ScadaAnomalyFunnel(
        sample_rate=config["sample_rate"],
        rpm=config["rpm"]
    )

    return funnel.calculate_dsp_features(signal)

def get_envelope_data():

    config = load_config()

    signal = generate_signal()

    physics_engine = KinematicPhysicsEngine(
        sample_rate=config["sample_rate"],
        rpm=config["rpm"],
        bearing_geometry=config["bearing_geom"],
        resonance_band=config["resonance_band"]
    )

    xf, yf = physics_engine._envelope_spectrum(signal)

    return xf, yf

def get_feature_vector():

    config = load_config()

    signal = generate_signal()

    funnel = ScadaAnomalyFunnel(
        sample_rate=config["sample_rate"],
        rpm=config["rpm"]
    )

    return funnel.calculate_dsp_features(signal)