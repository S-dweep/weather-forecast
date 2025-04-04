import streamlit as st

st.title("WEATHER FORECAST")
place=st.text_input("PLACE")
days=st.slider("FORECAST DAYS", min_value=1, max_value=10, help="Select the number of days to forecast weather")
option=st.selectbox("VIEW PARAMETER", ("Temperature", "Sky Condition"))
st.subheader(f"{option} for the next {days} days in {place}")