
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Engineering Ops Tools", layout="centered")
st.title("📊 Engineering Toolbox (Operations Tools)")

tab1, tab2, tab3 = st.tabs([
    "Production Estimator",
    "G-code Viewer",
    "Takt Time"
])

with tab1:
    st.header("Production Rate Estimator")
    cycle_time_hr = st.number_input("Cycle Time per Part (hours)", min_value=0.01, step=0.01, format="%.2f")
    shift_hours = st.number_input("Shift Length (hours)", min_value=1.0, step=0.5)
    breaks_min = st.number_input("Break Time (minutes)", min_value=0.0, step=5.0)
    if st.button("Estimate Production"):
        available_hours = shift_hours - (breaks_min / 60)
        parts_per_day = available_hours / cycle_time_hr
        st.subheader("Estimated Output")
        st.write(f"Available Time: {available_hours:.2f} hours")
        st.write(f"Estimated Parts per Day: {parts_per_day:.0f}")

with tab2:
    st.header("G-code Viewer")
    uploaded_file = st.file_uploader("Upload G-code file (.nc or .txt)", type=["nc", "txt"])
    if uploaded_file:
        code_lines = uploaded_file.read().decode("utf-8").splitlines()
        st.text_area("G-code Preview", value="\n".join(code_lines[:50]), height=300)
        if st.checkbox("Show Tool Changes"):
            tool_lines = [line for line in code_lines if "T" in line and "M6" in line]
            st.write("Detected Tool Changes:")
            for tl in tool_lines:
                st.code(tl)

with tab3:
    st.header("Takt Time Calculator")
    demand = st.number_input("Customer Demand (units/day)", min_value=1)
    available_time = st.number_input("Available Work Time (minutes/day)", min_value=1.0)
    if st.button("Calculate Takt Time"):
        takt_time = available_time / demand
        st.subheader(f"Takt Time: {takt_time:.2f} min/unit")
        if takt_time < 1:
            st.warning("⚠️ Your takt time is less than 1 min/unit. Ensure machines can keep up.")
