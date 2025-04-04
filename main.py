import streamlit as st
import plotly.express as px

st.title("WEATHER FORECAST")
place = st.text_input("PLACE")
days = st.slider("FORECAST DAYS", min_value=1, max_value=10, help="Select the number of days to forecast weather")
option = st.selectbox("VIEW PARAMETER", ("Temperature", "Sky Condition"))
st.subheader(f"{option} for the next {days} days in {place}")


def get_data(days):
    dates = ["2025-04-05", "2025-04-06", "2025-04-07"]
    temperatures = [32, 33, 28]
    temperatures = [days * i for i in temperatures]
    return dates, temperatures


d, t = get_data(days)
figure = px.line(x=d, y=t, labels={"x": "Date", "y": "Temperature (C)"})
st.plotly_chart(figure)
