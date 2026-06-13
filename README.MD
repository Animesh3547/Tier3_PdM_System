# Machine Condition Monitoring System

Domain:
Machine Condition Monitoring

Focus:
Physics-Guided Predictive Maintenance

Tech Stack:
Python, NumPy, SciPy, Scikit-Learn, Streamlit

Techniques:
FFT, Envelope Analysis, Hilbert Transform,
Bearing Kinematics, Isolation Forest

Status:
Architecture Complete | Dashboard Complete |
Validation Pending | Cloud Integration pending

## Overview

Machine condition monitoring plays a critical role in improving reliability, reducing unplanned downtime, and enabling predictive maintenance of rotating machinery. This project presents a physics-guided vibration monitoring framework that combines signal processing, anomaly detection, and engineering fault diagnostics to identify abnormal machine behavior.

The system extracts time-domain and frequency-domain condition indicators from vibration signals, monitors deviations from healthy operating conditions using Isolation Forest, and verifies potential faults through bearing kinematics and rotational frequency analysis. A temporal persistence layer is used to reduce false alarms, while a health tracking module monitors degradation trends over time.

The objective of the project is to develop an interpretable condition monitoring architecture that bridges vibration physics, statistical monitoring, and maintenance decision support.


## Problem Statement

Rotating machinery such as motors, pumps, compressors, and gear-driven systems are critical assets in industrial environments. Unexpected failures in these machines can result in production downtime, maintenance costs, equipment damage, and safety risks.

Traditional maintenance strategies often rely on fixed inspection schedules or simple alarm thresholds, which may fail to detect early-stage degradation and provide limited insight into the underlying fault mechanism. As machine operating conditions change, purely threshold-based approaches can also generate false alarms or miss developing faults.

This project was developed to explore a more structured condition monitoring approach by combining vibration signal analysis, statistical anomaly detection, and physics-guided fault verification. The goal is to provide interpretable machine health information, support early fault detection, and establish a foundation for predictive maintenance applications.


## System Architecture

The system follows a layered condition-monitoring architecture that combines signal validation, statistical anomaly detection, physics-guided fault verification, and health trend monitoring.

```text
Vibration Signal
        ↓
Sensor Health Gate
        ↓
Feature Extraction
(RMS, Kurtosis, Crest Factor, Skewness,
FFT Harmonics, HF Energy)
        ↓
Isolation Forest
Anomaly Detection
        ↓
Temporal Persistence Gate
        ↓
Physics-Guided Fault Analysis
(BPFO, BPFI, BSF, FTF,
1X RPM, 2X RPM)
        ↓
Health Tracking
& Trend Monitoring
        ↓
Streamlit Dashboard
```

### Layer Description

**Sensor Health Gate**

* Detects dead sensors
* Detects flatline signals
* Detects clipping conditions

**Feature Extraction Layer**

* Computes time-domain and frequency-domain condition indicators

**Anomaly Detection Layer**

* Uses Isolation Forest to identify deviations from the healthy baseline

**Persistence Verification Layer**

* Suppresses transient false alarms by requiring repeated anomaly confirmation

**Physics-Guided Diagnostic Layer**

* Verifies anomalies using bearing kinematics and rotational fault frequencies

**Health Tracking Layer**

* Tracks degradation trends and machine health indicators over time

**Visualization Layer**

* Provides interactive monitoring and diagnostic visualization through Streamlit




## Core Features

### Sensor Health Validation

* Dead sensor detection
* Flatline detection
* Clipping detection

### Time-Domain Monitoring

* RMS
* Kurtosis
* Crest Factor
* Skewness

### Frequency-Domain Analysis

* Hann-windowed FFT
* 1X RPM tracking
* 2X RPM tracking
* High-frequency energy monitoring

### Bearing Fault Diagnostics

* BPFO monitoring
* BPFI monitoring
* BSF monitoring
* FTF monitoring
* Envelope analysis
* Hilbert transform demodulation

### Anomaly Detection

* Isolation Forest based anomaly detection
* Human-approved baseline training

### Alarm Verification

* Temporal persistence gating
* False alarm suppression

### Health Assessment

* Health score estimation
* Degradation trend tracking

### Visualization

* Streamlit dashboard
* FFT visualization
* Envelope spectrum visualization
* Trend monitoring


## Dashboard

An interactive Streamlit dashboard was developed to visualize machine condition monitoring outputs and diagnostic results.

The dashboard currently includes:

* Machine Overview
* FFT Analysis
* Envelope Spectrum Analysis
* Trend Monitoring

The dashboard is designed to provide engineers with a consolidated view of machine health, vibration behavior, anomaly status, and fault indicators.

### Dashboard Pages

#### Overview

Displays machine status, health metrics, and monitoring summary.

![Dashboard Overview](images/dashboard_overview.jpg)

#### FFT Analysis

Visualizes the frequency spectrum of vibration signals using Hann-windowed FFT processing.

![FFT Analysis](images/fft_analysis.jpg)

#### Envelope Spectrum Analysis

Visualizes envelope-demodulated vibration spectra for bearing fault investigation.

![Envelope Analysis](images/envelope_analysis.jpg)

#### Trend Monitoring

Displays the evolution of condition indicators and health metrics over time.

![Trend Monitoring](images/trend_monitoring.jpg)

## Results

Current implementation successfully demonstrates:

* End-to-end vibration monitoring pipeline architecture
* Time-domain feature extraction (RMS, Kurtosis, Crest Factor, Skewness)
* Hann-windowed FFT analysis for harmonic monitoring
* Envelope spectrum analysis using Hilbert Transform
* Bearing fault frequency calculation (BPFO, BPFI, BSF, FTF)
* Isolation Forest based anomaly detection
* Temporal persistence verification for alarm suppression
* Health score and degradation trend estimation
* Interactive Streamlit dashboard visualization

### Example Outputs

[Insert FFT Screenshot]

[Insert Envelope Spectrum Screenshot]

[Insert Trend Monitoring Screenshot]

[Insert Dashboard Overview Screenshot]

### Current Validation Status

The current implementation has been verified using simulated vibration signals for pipeline validation and algorithm testing.

Validation using publicly available bearing datasets (CWRU, IMS) and real DAQ-acquired vibration data is planned as future work.

## Repository Structure

```text
Machine-Condition-Monitoring-System/
│
├── dashboard/
│   ├── app.py
│   ├── data_provider.py
│   └── pages/
│
├── edge_pipeline/
│   ├── anomaly_funnel.py
│   ├── health_tracker.py
│   ├── kinematic_dsp.py
│   ├── orchestrator.py
│   ├── sensor_health.py
│   ├── temporal_persistence_gate.py
│   ├── train_baseline.py
│   └── config.json
│
├── README.md
├── requirements.txt
└── LICENSE
```

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Machine-Condition-Monitoring-System.git

cd Machine-Condition-Monitoring-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Dashboard

```bash
cd dashboard

py -m streamlit run app.py
```


## Current Limitations

* Current validation has primarily been performed using simulated vibration signals rather than long-duration industrial datasets.

* The monitoring pipeline currently assumes constant-speed rotating machinery and does not include variable-speed order tracking.

* Bearing geometry and machine operating parameters must be provided manually.

* The resonance band used for envelope analysis is currently configured manually and is not automatically identified from machine data.

* The implemented fault library focuses on common rotating machinery faults and does not cover all possible mechanical failure modes.

* The current Streamlit dashboard is intended for demonstration and visualization purposes rather than industrial deployment.

* Real-time DAQ integration, edge deployment optimization, and field validation have not yet been completed.

* Health score calculations currently provide relative condition assessment and are not calibrated against actual remaining useful life (RUL) measurements.


## Future Work

* Validate the monitoring pipeline using publicly available bearing datasets such as CWRU and IMS.

* Integrate real DAQ-acquired vibration signals for testing under realistic operating conditions.

* Extend support to variable-speed machinery through order tracking and speed-synchronized analysis.

* Expand the fault library to include additional rotating machinery faults such as looseness, rubbing, and gear-related defects.

* Investigate automatic resonance-band identification for improved envelope analysis configuration.

* Improve health tracking by incorporating degradation-rate estimation and condition trend forecasting.

* Optimize the system for edge deployment and continuous machine monitoring applications.

* Explore hybrid approaches combining physics-guided diagnostics with machine learning-based prognostics.
