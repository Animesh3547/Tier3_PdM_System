import streamlit as st
import numpy as np
import pandas as pd

st.title("Trend Monitoring")

n_points = 50

time_axis = np.arange(n_points)

rms = np.linspace(1.0, 2.5, n_points) + 0.05*np.random.randn(n_points)

kurtosis = np.linspace(3.0, 8.0, n_points) + 0.2*np.random.randn(n_points)

crest_factor = np.linspace(2.5, 5.5, n_points) + 0.1*np.random.randn(n_points)

hf_energy = np.linspace(100, 500, n_points) + 20*np.random.randn(n_points)

trend_df = pd.DataFrame({
    "Sample": time_axis,
    "RMS": rms,
    "Kurtosis": kurtosis,
    "Crest Factor": crest_factor,
    "HF Energy": hf_energy
})

st.subheader("RMS Trend")
st.line_chart(
    trend_df,
    x="Sample",
    y="RMS"
)

st.subheader("Kurtosis Trend")
st.line_chart(
    trend_df,
    x="Sample",
    y="Kurtosis"
)

st.subheader("Crest Factor Trend")
st.line_chart(
    trend_df,
    x="Sample",
    y="Crest Factor"
)

st.subheader("High Frequency Energy Trend")
st.line_chart(
    trend_df,
    x="Sample",
    y="HF Energy"
)