import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load data (use Streamlit's cache mechanism for efficiency)
@st.cache
def load_data():
    global_temp_country = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
    global_temp = pd.read_csv("GlobalTemperatures.csv")

    # Handling missing values
    global_temp_country.dropna(subset=['AverageTemperature'], inplace=True)
    global_temp.dropna(subset=['LandAverageTemperature'], inplace=True)

    # Convert date strings to datetime objects
    global_temp_country['dt'] = pd.to_datetime(global_temp_country['dt'])
    global_temp['dt'] = pd.to_datetime(global_temp['dt'])

    # Extract year and month for further analysis
    global_temp_country['year'] = global_temp_country['dt'].dt.year
    global_temp['year'] = global_temp['dt'].dt.year
    global_temp['month'] = global_temp['dt'].dt.month

    # Grouping data by decade
    global_temp['decade'] = (global_temp['year'] // 10) * 10

    return global_temp_country, global_temp

global_temp_country, global_temp = load_data()

# Function for Home Page
def home():
    st.title("Climate Data Analysis Application")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("backgroundimage.jpg");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.write("This application provides an in-depth analysis of global temperature trends.")
    st.write("Explore various aspects of global climate change over time.")

# Function for Global Land Average Temperature Analysis
def global_land_avg_temp():
    st.title("Global Land Average Temperature Analysis")
    land_avg_temp_trend = global_temp.groupby('year')['LandAverageTemperature'].mean().reset_index()
    fig = px.line(land_avg_temp_trend, x='year', y='LandAverageTemperature', title='Global Land Average Temperature Over Time')
    st.plotly_chart(fig)

# Function for Decadal and Seasonal Temperature Trends
def decadal_seasonal_trends():
    st.title("Decadal and Seasonal Temperature Trends")
    # Decadal Analysis
    avg_temp_by_decade = global_temp.groupby('decade')['LandAverageTemperature'].mean().reset_index()
    st.write("Average Land Temperature by Decade")
    fig_decade = px.bar(avg_temp_by_decade, x='decade', y='LandAverageTemperature')
    st.plotly_chart(fig_decade)

    # Seasonal Analysis
    st.write("Seasonal Patterns in Global Temperatures")
    avg_temp_by_month = global_temp.groupby('month')['LandAverageTemperature']. mean().reset_index()
    fig_month = px.line(avg_temp_by_month, x='month', y='LandAverageTemperature')
    st.plotly_chart(fig_month)

# Function for Interactive Global Temperature Map
def global_temp_map():
    st.title("Interactive Global Temperature Map")
    fig = px.choropleth(global_temp_country, 
                        locations="Country", 
                        locationmode='country names',
                        color="AverageTemperature",
                        hover_name="Country", 
                        animation_frame="year")
    st.plotly_chart(fig)

# Main Script to Run the App
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home", "Global Land Avg Temp", "Decadal and Seasonal Trends", "Global Temp Map"))

if page == "Home":
    home()
elif page == "Global Land Avg Temp":
    global_land_avg_temp()
elif page == "Decadal and Seasonal Trends":
    decadal_seasonal_trends()
elif page == "Global Temp Map":
    global_temp_map()
