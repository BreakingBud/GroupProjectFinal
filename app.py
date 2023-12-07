import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load and preprocess data
@st.cache_data
def load_data():
    global_temp_country = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
    global_temp = pd.read_csv("GlobalTemperatures.csv")

    # Handling missing values and data conversion
    global_temp_country.dropna(subset=['AverageTemperature'], inplace=True)
    global_temp.dropna(subset=['LandAverageTemperature'], inplace=True)

    global_temp_country['dt'] = pd.to_datetime(global_temp_country['dt'])
    global_temp['dt'] = pd.to_datetime(global_temp['dt'])

    global_temp_country['year'] = global_temp_country['dt'].dt.year
    global_temp['year'] = global_temp['dt'].dt.year
    global_temp['month'] = global_temp['dt'].dt.month

    global_temp['decade'] = (global_temp['year'] // 10) * 10

    return global_temp_country, global_temp

global_temp_country, global_temp = load_data()

# Function for Home Page
def home():
    st.title("Climate Data Analysis Application")
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("backgroundimage.jpg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
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
    fig_decade = px.bar(avg_temp_by_decade, x='decade', y='LandAverageTemperature')
    st.plotly_chart(fig_decade)

    # Seasonal Analysis
    avg_temp_by_month = global_temp.groupby('month')['LandAverageTemperature'].mean().reset_index()
    fig_month = px.line(avg_temp_by_month, x='month', y='LandAverageTemperature')
    st.plotly_chart(fig_month)

    # Interactive Country-specific Analysis
    st.title("Country-Specific Temperature Analysis")
    country_list = global_temp_country['Country'].unique()
    selected_country = st.selectbox('Select a Country', country_list)
    selected_year_range = st.slider('Select Year Range', min_value=int(global_temp_country['year'].min()), max_value=int(global_temp_country['year'].max()), value=(2000, 2010))

    country_data = global_temp_country[(global_temp_country['Country'] == selected_country) & (global_temp_country['year'].between(selected_year_range[0], selected_year_range[1]))]
    fig_country = px.line(country_data, x='year', y='AverageTemperature', title=f'Temperature Trend in {selected_country}')
    st.plotly_chart(fig_country)

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

# Function for Credits and Thank You Page
def credits():
    st.title("Credits and Acknowledgements")
    st.write("Thank you to everyone who contributed to this project.")

# Main script to run the app
if st.sidebar.button('Menu'):
    page = st.sidebar.radio("Navigate to", ("Home", "Global Land Avg Temp", "Decadal and Seasonal Trends", "Global Temp Map", "Credits"))

    if page == "Home":
        home()
    elif page == "Global Land Avg Temp":
        global_land_avg_temp()
    elif page == "Decadal and Seasonal Trends":
        decadal_seasonal_trends()
    elif page == "Global Temp Map":
        global_temp_map()
    elif page == "Credits":
        credits()
