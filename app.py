import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load and clean data (use Streamlit's cache mechanism for efficiency)
@st.cache_data
def load_data():
    # Load datasets
    global_temp_country = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
    global_temp = pd.read_csv("GlobalTemperatures.csv")

    # Convert date strings to datetime objects
    global_temp_country['dt'] = pd.to_datetime(global_temp_country['dt'])
    global_temp['dt'] = pd.to_datetime(global_temp['dt'])

    # Extract year for further analysis
    global_temp_country['year'] = global_temp_country['dt'].dt.year

    # Clean 'GlobalLandTemperaturesByCountry.csv'
    global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
        ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
         'United Kingdom', 'Africa', 'South America'])]
    global_temp_country_clear = global_temp_country_clear.replace(
        ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
        ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

    # Calculate average temperature for each country by year
    global_temp_country_avg = global_temp_country_clear.groupby(['Country', 'year'])['AverageTemperature'].mean().reset_index()

    return global_temp_country_avg, global_temp

global_temp_country_avg, global_temp = load_data()

# Function for Home Page with Background Image
def home():
    st.title("Climate Data Analysis Application")
    st.write("This application provides an in-depth analysis of global temperature trends.")
    st.write("Explore various aspects of global climate change over time.")

# Function for Global Land Average Temperature Analysis
def global_land_avg_temp():
    st.title("Global Land Average Temperature Analysis")
    land_avg_temp_trend = global_temp.groupby('year')['LandAverageTemperature'].mean().reset_index()
    fig = px.line(land_avg_temp_trend, x='year', y='LandAverageTemperature', 
                  title='Global Land Average Temperature Over Time',
                  line_shape='linear', 
                  line_dash_sequence=['solid'],
                  color_discrete_sequence=['#FF5733'])  # Warm color for the line
    st.plotly_chart(fig)

# Function for Decadal Trends with Warm Colors
def decadal_seasonal_trends():
    st.title("Decadal and Seasonal Temperature Trends")

    # Decadal Analysis
    avg_temp_by_decade = global_temp.groupby('decade')['LandAverageTemperature'].mean().reset_index()
    st.write("Average Land Temperature by Decade")
    fig_decade = px.bar(avg_temp_by_decade, x='decade', y='LandAverageTemperature',
                        color='LandAverageTemperature',  # Coloring based on temperature
                        color_continuous_scale=px.colors.sequential.YlOrRd)  # Warm color scale
    st.plotly_chart(fig_decade)

# Function for Interactive Global Temperature Map with Warm Colors
def global_temp_map():
    st.title("Interactive Global Temperature Map")
    fig = px.choropleth(global_temp_country, 
                        locations="Country", 
                        locationmode='country names',
                        color="AverageTemperature",
                        hover_name="Country", 
                        animation_frame="year",
                        color_continuous_scale=px.colors.sequential.OrRd)
    st.plotly_chart(fig)

# Function for Thanks and Credits Page
def thanks_and_credits():
    st.title("Thanks and Credits")
    st.write("Thank you for exploring our Climate Data Analysis Application.")
    st.write("## Credits:")
    st.write("Data Source: Kaggle's Global Land and Ocean-and-Land Temperatures dataset.")
    st.write("Developed by: [Your Name/Team Name]")
    st.write("Special thanks to all contributors and data scientists working towards understanding climate change.")

# Main Script to Run the App
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home", "Global Land Avg Temp", "Decadal and Seasonal Trends", "Global Temp Map", "Thanks and Credits"))

if page == "Home":
    home()
elif page == "Global Land Avg Temp":
    global_land_avg_temp()
elif page == "Decadal and Seasonal Trends":
    decadal_seasonal_trends()
elif page == "Global Temp Map":
    global_temp_map()
elif page == "Thanks and Credits":
    thanks_and_credits()
