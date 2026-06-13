import streamlit as st
import pandas as pd

from data_provider import get_envelope_data

st.title("Envelope Spectrum Analysis")

xf, yf = get_envelope_data()

env_df = pd.DataFrame({
    "Frequency (Hz)": xf,
    "Magnitude": yf
})

st.subheader("Envelope Spectrum")

st.line_chart(
    env_df,
    x="Frequency (Hz)",
    y="Magnitude"
)

st.markdown("""
### Bearing Diagnostics

- BPFO : Outer Race Fault
- BPFI : Inner Race Fault
- BSF  : Rolling Element Fault
- FTF  : Cage Fault

Envelope analysis extracts impact repetition frequencies from resonance-band vibration signals.
""")