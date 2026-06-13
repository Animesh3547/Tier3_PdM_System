import streamlit as st

st.set_page_config(
    page_title="Machine Condition Monitoring",
    page_icon="⚙️",
    layout="wide"
)

st.title("Machine Condition Monitoring System")

st.markdown("""
### Physics-Guided Vibration Diagnostics

This dashboard visualizes:

- Machine Health Status
- Time-Domain Features
- FFT Analysis
- Envelope Spectrum Analysis
- Bearing Fault Indicators
- Degradation Trends
""")

st.info(
    "Use the navigation panel on the left to explore Overview, FFT, Envelope Analysis, and Trend Monitoring."
)