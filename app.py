import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Function to load and clean data
@st.cache_data
def load_data():
    # Load datasets
    global_temp_country = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
    global_temp = pd.read_csv("GlobalTemperatures.csv")
    global_temp_city = pd.read_csv("GlobalLandTemperaturesByMajorCity.csv")  # Load the city temperature data

    # Convert date strings to datetime objects and extract year and month
    global_temp_country['dt'] = pd.to_datetime(global_temp_country['dt'])
    global_temp_country['year'] = global_temp_country['dt'].dt.year

    global_temp['dt'] = pd.to_datetime(global_temp['dt'])
    global_temp['year'] = global_temp['dt'].dt.year
    global_temp['month'] = global_temp['dt'].dt.month
    global_temp['decade'] = (global_temp['year'] // 10) * 10

    global_temp_city['dt'] = pd.to_datetime(global_temp_city['dt'])
    global_temp_city['year'] = global_temp_city['dt'].dt.year

    # Clean 'GlobalLandTemperaturesByCountry.csv'
    global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
        ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
         'United Kingdom', 'Africa', 'South America'])]
    global_temp_country_clear = global_temp_country_clear.replace(
        ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
        ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

    # Calculate average temperature for each country by year
    global_temp_country_avg = global_temp_country_clear.groupby(['Country', 'year'])['AverageTemperature'].mean().reset_index()

    # Preprocess the city temperature data
    global_temp_city = global_temp_city[global_temp_city['year'] >= 1850]  # Filter out records before 1850
    global_temp_city_avg = global_temp_city.groupby(['City', 'Country', 'year'])['AverageTemperature'].mean().reset_index()

    return global_temp_country_avg, global_temp, global_temp_city_avg

# Call the load_data function to load all datasets
global_temp_country_avg, global_temp, global_temp_city_avg = load_data()


# Function for Interactive Global Temperature Map
def global_temp_map():
    st.title("Interactive Global Temperature Map")

    # Filter the data to include only years from 1850 onwards and drop NaN values
    global_temp_country_filtered = global_temp_country_avg[global_temp_country_avg['year'] >= 1850].dropna(subset=['AverageTemperature'])

    # Ensure the data is sorted by year
    global_temp_country_sorted = global_temp_country_filtered.sort_values('year')

    # Define the color scale to use for the choropleth
    color_scale = px.colors.sequential.OrRd

    fig = px.choropleth(global_temp_country_sorted,
                        locations="Country",
                        locationmode='country names',
                        color="AverageTemperature",
                        hover_name="Country",
                        animation_frame="year",
                        color_continuous_scale=color_scale,
                        range_color=(global_temp_country_sorted['AverageTemperature'].min(),
                                     global_temp_country_sorted['AverageTemperature'].max()))

    # Update the layout to include country borders
    fig.update_geos(
        showcountries=True,
        countrycolor="Black"  # Set border color to black for visibility
    )

    # Update the layout to match your theme
    fig.update_layout(
        title_text='Global Land Average Temperature Over Time',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    st.plotly_chart(fig)

# Function for Home Page
def home():
    st.title("Climate Data Analysis Application")
    st.markdown("""
    This application provides an in-depth analysis of global temperature trends.
    Explore various aspects of global climate change over time.
    """)

# Function for Global Land Average Temperature Analysis
def global_land_avg_temp():
    st.title("Global Land Average Temperature Analysis")
    land_avg_temp_trend = global_temp.groupby('year')['LandAverageTemperature'].mean().reset_index()
    fig = px.line(land_avg_temp_trend, x='year', y='LandAverageTemperature', 
                  title='Global Land Average Temperature Over Time',
                  line_shape='linear', 
                  line_dash_sequence=['solid'],
                  color_discrete_sequence=['#FF5733'])
    st.plotly_chart(fig)

# Function for Decadal Trends
def decadal_seasonal_trends():
    st.title("Decadal and Seasonal Temperature Trends")

    # Decadal Analysis
    avg_temp_by_decade = global_temp.groupby('decade')['LandAverageTemperature'].mean().reset_index()
    st.write("Average Land Temperature by Decade")
    fig_decade = px.bar(avg_temp_by_decade, x='decade', y='LandAverageTemperature',
                        color='LandAverageTemperature', 
                        color_continuous_scale=px.colors.sequential.YlOrRd)
    st.plotly_chart(fig_decade)

#Function for When did global warming started?
def global_warming_start():
    st.title("When Did Global Warming Start?")
    st.markdown("""
    Explore the changes in temperature measures over the years.
    Select a temperature measure to see its trend.
    """)

    # Dropdown for selecting the plot
    option = st.selectbox(
        'Choose a Temperature Measure',
        ['Land Average Temperature', 'Land Min Temperature', 'Land Max Temperature', 'Land and Ocean Average Temperature']
    )

    # Filter the data to include only years from 1850 onwards
    filtered_data = global_temp[global_temp['year'] >= 1850]

    # Group by year
    yearly_data = filtered_data.groupby('year').mean().reset_index()

    # Initialize a figure object
    fig = go.Figure()

    # Choose the column to plot based on the dropdown selection
    if option == 'Land Average Temperature':
        column = 'LandAverageTemperature'
        title = 'Land Average Temperature Over Years'
    elif option == 'Land Min Temperature':
        column = 'LandMinTemperature'
        title = 'Land Min Temperature Over Years'
    elif option == 'Land Max Temperature':
        column = 'LandMaxTemperature'
        title = 'Land Max Temperature Over Years'
    else:
        column = 'LandAndOceanAverageTemperature'
        title = 'Land and Ocean Average Temperature Over Years'

    # Add the main trace to the figure
    fig.add_trace(go.Scatter(x=yearly_data['year'], y=yearly_data[column], mode='lines', name=option))

    # Add a vertical line for the year 1975 (or any other significant year)
    fig.add_trace(go.Scatter(x=[1975, 1975], y=[min(yearly_data[column]), max(yearly_data[column])], 
                             mode="lines", line=go.scatter.Line(color="gray", width=2), 
                             showlegend=False))

    # Update the layout
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Temperature (°C)',
        template='plotly_dark'
    )

    # Plot!
    st.plotly_chart(fig)

# Function for Comparing City Temperature Trends
def compare_city_temps():
    st.title("Compare City Temperature Trends")

    # Get the unique list of cities
    cities = city_yearly_avg_temp['City'].unique()
    
    # Dropdown for selecting cities
    city1 = st.selectbox('Select the first city to compare', cities)
    city2 = st.selectbox('Select the second city to compare', cities, index=1)  # Default to second item in the list

    # Filter the data for the selected cities
    city1_data = city_yearly_avg_temp[city_yearly_avg_temp['City'] == city1]
    city2_data = city_yearly_avg_temp[city_yearly_avg_temp['City'] == city2]

    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=city1_data['year'], y=city1_data['AverageTemperature'],
                             mode='lines', name=city1))
    fig.add_trace(go.Scatter(x=city2_data['year'], y=city2_data['AverageTemperature'],
                             mode='lines', name=city2))

    # Update the layout
    fig.update_layout(
        title=f'Temperature Trends: {city1} vs {city2}',
        xaxis_title='Year',
        yaxis_title='Average Temperature (°C)',
        template='plotly_dark'
    )

    st.plotly_chart(fig)
    
#Function for thanks page
def thanks_and_credits():
    st.title("Thanks and Credits")
    st.markdown("This application was developed by [Your Name]. Thanks to all the data providers and libraries used in this project.")

# Main Script to Run the App
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home", "Global Land Avg Temp", "Decadal and Seasonal Trends", "When Did Global Warming Start?", "Global Temp Map", "Thanks and Credits"))

if page == "Home":
    home()
elif page == "Global Land Avg Temp":
    global_land_avg_temp()
elif page == "Decadal and Seasonal Trends":
    decadal_seasonal_trends()
elif page == "When Did Global Warming Start?":
    global_warming_start()
elif page == "Global Temp Map":
    global_temp_map()
elif page == "Compare City Temps":
    compare_city_temps()
elif page == "Thanks and Credits":
    thanks_and_credits()


