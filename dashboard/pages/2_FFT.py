import streamlit as st
import pandas as pd

from data_provider import get_fft_data

st.title("FFT Analysis")

# Get FFT from project pipeline
xf, yf = get_fft_data()

# Create dataframe for plotting
fft_df = pd.DataFrame({
    "Frequency (Hz)": xf,
    "Magnitude": yf
})

st.subheader("Frequency Spectrum")

st.line_chart(
    fft_df,
    x="Frequency (Hz)",
    y="Magnitude"
)

st.markdown("""
### Reference Frequencies

- 1X RPM = 30 Hz
- 2X RPM = 60 Hz
- 3X RPM = 90 Hz

### Notes

- Hann Window applied before FFT
- FFT Resolution depends on Fs/N
- Peaks near 1X and 2X RPM indicate rotational faults
- Used for imbalance and misalignment analysis
""")