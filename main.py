import streamlit as st
import plotly.express as px
from backend import get_data
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 800;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem !important;
        font-weight: 600;
        color: #0277BD;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .stTextInput {
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1rem;
        color: #424242;
    }
    .weather-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
    }
    .metric-label {
        font-size: 1rem;
        text-align: center;
        color: #616161;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 class='main-header'>🌤️ Weather Forecast</h1>", unsafe_allow_html=True)

# Create sidebar for inputs
with st.sidebar:
    st.markdown("<h2>Location Settings</h2>", unsafe_allow_html=True)
    place = st.text_input("Enter Location", placeholder="e.g., London, New York, Tokyo")
    days = st.slider("Forecast Days", min_value=1, max_value=5, value=3,
                     help="Select the number of days to forecast weather")

    st.markdown("<h2>Display Options</h2>", unsafe_allow_html=True)
    option = st.selectbox("Select View Parameter", ("Temperature", "Sky Condition", "Detailed View"))

    temp_unit = st.radio("Temperature Unit", ["Celsius", "Fahrenheit"])

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p class='info-text'>Data provided by Weather API</p>", unsafe_allow_html=True)


# Function to convert temperature if needed
def convert_temp(temp, unit):
    if unit == "Celsius":
        return temp
    else:  # Fahrenheit
        return (temp * 9 / 5) + 32


# Main content area
if place:
    try:
        # Get weather data
        filtered_data = get_data(place, days)

        # Display current weather summary
        if filtered_data:
            # Get current weather (first item in the list)
            current = filtered_data[0]

            # Create columns for current weather display
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
                current_temp = convert_temp(current["main"]["temp"] / 10, temp_unit)
                st.markdown(f"<div class='metric-value'>{current_temp:.1f}°</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-label'>Current Temperature ({temp_unit})</div>",
                            unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{current['weather'][0]['main']}</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Weather Condition</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col3:
                st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{current['main'].get('humidity', 'N/A')}%</div>",
                            unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Humidity</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # Display forecasted data based on selected option
        st.markdown(f"<h2 class='subheader'>{option} for the next {days} days in {place}</h2>", unsafe_allow_html=True)

        dates = [d["dt_txt"] for d in filtered_data]
        formatted_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%a %d %b, %H:%M") for date in dates]

        if option == "Temperature":
            # Create temperature dataframe
            temperatures = [convert_temp(d["main"]["temp"] / 10, temp_unit) for d in filtered_data]
            temp_min = [convert_temp(d["main"].get("temp_min", d["main"]["temp"] - 10) / 10, temp_unit) for d in
                        filtered_data]
            temp_max = [convert_temp(d["main"].get("temp_max", d["main"]["temp"] + 10) / 10, temp_unit) for d in
                        filtered_data]

            temp_df = pd.DataFrame({
                "Date": formatted_dates,
                f"Temperature ({temp_unit})": temperatures,
                "Min": temp_min,
                "Max": temp_max
            })

            # Create temperature chart
            fig = px.line(temp_df, x="Date", y=f"Temperature ({temp_unit})",
                          title=f"Temperature Forecast for {place}",
                          labels={"Date": "Date & Time", f"Temperature ({temp_unit})": f"Temperature ({temp_unit})"},
                          markers=True)

            fig.add_scatter(x=temp_df["Date"], y=temp_df["Min"], mode="lines", name="Min Temp", line=dict(dash="dash"))
            fig.add_scatter(x=temp_df["Date"], y=temp_df["Max"], mode="lines", name="Max Temp", line=dict(dash="dash"))

            fig.update_layout(
                plot_bgcolor='rgba(240,240,240,0.8)',
                height=500,
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Show temperature table
            st.markdown("<h3 class='subheader'>Temperature Details</h3>", unsafe_allow_html=True)
            st.dataframe(temp_df.set_index("Date"), use_container_width=True)

        elif option == "Sky Condition":
            # Show sky condition images with improved layout
            st.markdown("<h3 class='subheader'>Sky Conditions</h3>", unsafe_allow_html=True)

            images = {
                "Clear": "images/clear.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png"
            }

            # Get the conditions and create display columns (5 per row)
            sky_conditions = [d["weather"][0]["main"] for d in filtered_data]


            # Create chunks of 5 for display
            def chunks(lst, n):
                for i in range(0, len(lst), n):
                    yield lst[i:i + n], formatted_dates[i:i + n], sky_conditions[i:i + n]


            for i, (condition_chunk, date_chunk, sky_chunk) in enumerate(chunks(sky_conditions, 5)):
                cols = st.columns(len(condition_chunk))

                for j, (col, date, condition) in enumerate(zip(cols, date_chunk, sky_chunk)):
                    with col:
                        if condition in images:
                            st.image(images[condition], width=100)
                            st.markdown(f"<p style='text-align:center'>{condition}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align:center; font-size:0.8rem'>{date}</p>",
                                        unsafe_allow_html=True)
                        else:
                            st.write(f"No image for {condition}")
                            st.markdown(f"<p style='text-align:center'>{date}</p>", unsafe_allow_html=True)

        elif option == "Detailed View":
            # Show comprehensive data
            st.markdown("<h3 class='subheader'>Detailed Weather Information</h3>", unsafe_allow_html=True)

            # Create a more detailed dataframe
            detailed_data = []
            for item in filtered_data:
                entry = {
                    "Date & Time": datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%a %d %b, %H:%M"),
                    "Temperature": f"{convert_temp(item['main']['temp'] / 10, temp_unit):.1f}°{temp_unit[0]}",
                    "Condition": item["weather"][0]["main"],
                    "Description": item["weather"][0]["description"].title(),
                    "Humidity": f"{item['main'].get('humidity', 'N/A')}%",
                    "Pressure": f"{item['main'].get('pressure', 'N/A')} hPa",
                    "Wind Speed": f"{item.get('wind', {}).get('speed', 'N/A')} m/s"
                }
                detailed_data.append(entry)

            # Display as a table
            detailed_df = pd.DataFrame(detailed_data)
            st.dataframe(detailed_df.set_index("Date & Time"), use_container_width=True)

            # Additional charts
            st.markdown("<h3 class='subheader'>Humidity Trend</h3>", unsafe_allow_html=True)
            humidity_values = [d["main"].get("humidity", 0) for d in filtered_data]

            humidity_df = pd.DataFrame({
                "Date": formatted_dates,
                "Humidity (%)": humidity_values
            })

            humidity_fig = px.line(humidity_df, x="Date", y="Humidity (%)",
                                   title=f"Humidity Forecast for {place}",
                                   labels={"Date": "Date & Time", "Humidity (%)": "Humidity (%)"},
                                   markers=True)

            humidity_fig.update_layout(
                plot_bgcolor='rgba(240,240,240,0.8)',
                height=400,
                hovermode="x unified"
            )

            st.plotly_chart(humidity_fig, use_container_width=True)

    except KeyError as e:
        st.error(f"Place does not exist or there was an error with the data: {e}")
        st.info("Please check the location name and try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.info("Please try again later or contact support if the issue persists.")
else:
    # Display welcome message when no location is entered
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <img src="https://img.icons8.com/fluency/96/000000/partly-cloudy-day.png" width="96">
        <h2>Welcome to the Weather Forecast App!</h2>
        <p>Enter a location in the sidebar to get started.</p>
    </div>
    """, unsafe_allow_html=True)

    # Display example locations
    st.markdown("""
    <div style="background-color: #f0f7ff; padding: 1rem; border-radius: 10px; margin-top: 2rem;">
        <h3>Try these example locations:</h3>
        <ul>
            <li>New York</li>
            <li>London</li>
            <li>Tokyo</li>
            <li>Sydney</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)