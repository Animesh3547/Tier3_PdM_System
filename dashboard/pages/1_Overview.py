import streamlit as st

st.title("Machine Overview")

machine_id = "PUMP_04"
rpm = 1800
sample_rate = 10000

health_score = 92.4
trend_status = "STABLE"
anomaly_status = "NO"
verified_fault = "NONE"

col1, col2, col3, col4 = st.columns(4)

col1.metric("Health Score", f"{health_score}%")
col2.metric("Trend", trend_status)
col3.metric("Anomaly", anomaly_status)
col4.metric("Verified Fault", verified_fault)

st.divider()

st.subheader("Machine Parameters")

st.write(f"Machine ID: {machine_id}")
st.write(f"RPM: {rpm}")
st.write(f"Sampling Rate: {sample_rate} Hz")