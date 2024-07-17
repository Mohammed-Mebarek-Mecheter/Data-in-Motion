import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

# Load your cleaned and processed crime data
df = pd.read_csv('data/cleaned_MD_Crime_Data.csv')

# Define functions for each section of the analysis
def introduction():
    st.title("Maryland Crime Data Analysis (1975-2020)")
    st.write("""
    This app provides an analysis of historical crime data in Maryland to identify trends, patterns, and potential areas for intervention.
    The goal is to inform strategic planning for reducing crime rates by 10% in the next five years.
    """)

def trend_analysis():
    st.header("Trend Analysis")
    st.write("The overall crime rates in Maryland changed from 1975 to 2020?")
    crime_rates = df.groupby('Year')['OverallCrimeRatePer100k'].mean()
    trend_chart = alt.Chart(crime_rates.reset_index()).mark_line().encode(
        x='Year',
        y='OverallCrimeRatePer100k',
        tooltip=['Year', 'OverallCrimeRatePer100k']
    ).interactive()
    st.altair_chart(trend_chart, use_container_width=True)

def crime_distribution():
    st.header("Crime Distribution")
    st.write("The most common types of crimes committed in Maryland over the years.")
    # Define the crime types
    crime_types = ['Murder', 'Rape', 'Robbery', 'AggAssault', 'BreakAndEnter', 'LarcenyTheft', 'MotorVehicleTheft']
    # Group by 'Year' and sum the crime counts
    crime_data = df[crime_types + ['Year']].groupby('Year').sum().reset_index()
    # Melt the data for Altair
    crime_data_melted = crime_data.melt('Year', var_name='Crime Type', value_name='Count')
    # Create the Altair area chart
    distribution_chart = alt.Chart(crime_data_melted).mark_area().encode(
        x='Year:O',
        y='Count:Q',
        color='Crime Type:N',
        tooltip=['Year', 'Crime Type', 'Count']
    ).interactive()
    st.altair_chart(distribution_chart, use_container_width=True)

def geographical_analysis():
    st.header("Geographical Analysis")
    st.write("The jurisdictions have the highest and lowest crime rates in Maryland.")
    crime_types = ['Murder', 'Rape', 'Robbery', 'AggAssault', 'BreakAndEnter', 'LarcenyTheft', 'MotorVehicleTheft']
    crime_data = df[crime_types + ['Jurisdiction', 'Population']].copy()
    for crime_type in crime_types:
        crime_data[f'{crime_type}RatePer100k'] = crime_data[crime_type] / crime_data['Population'] * 100000
    average_crime_rates = crime_data.groupby('Jurisdiction')[[f'{crime_type}RatePer100k' for crime_type in crime_types]].mean().reset_index()
    fig = px.bar(average_crime_rates, x='Jurisdiction', y=[f'{crime_type}RatePer100k' for crime_type in crime_types], title="Average Crime Rates by Jurisdiction")
    st.plotly_chart(fig, use_container_width=True)

def population_correlation():
    st.header("Population Correlation")
    st.write("The correlation between population size and crime rates in different jurisdictions.")
    columns_of_interest = ['Population', 'MurderPer100k', 'RapePer100k', 'RobberyPer100k', 'AggAssaultPer100k', 'BreakAndEnterPer100k', 'LarcenyTheftPer100k', 'MotorVehicleTheftPer100k']
    crime_population_data = df[columns_of_interest]
    correlation_matrix = crime_population_data.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='rocket_r', ax=ax)
    st.pyplot(fig)

def crime_hotspots():
    st.header("Crime Hotspots")
    st.write("Identify crime hotspots in Maryland.")

    # Define the crime types to be analyzed
    crime_types = ['Murder', 'Rape', 'Robbery', 'AggAssault', 'BreakAndEnter', 'LarcenyTheft', 'MotorVehicleTheft']

    # Calculate the total crime rate per jurisdiction over the entire period
    df['TotalCrime'] = df[crime_types].sum(axis=1)
    total_crime_per_jurisdiction = df.groupby('Jurisdiction')['TotalCrime'].sum().reset_index()

    # Sort the jurisdictions by total crime in descending order to identify hotspots
    total_crime_per_jurisdiction = total_crime_per_jurisdiction.sort_values(by='TotalCrime', ascending=False)

    # Create a bar chart to visualize the total crime per jurisdiction
    fig = px.bar(total_crime_per_jurisdiction, x='Jurisdiction', y='TotalCrime', title="Total Crime by Jurisdiction",
                 labels={'TotalCrime': 'Total Crime Count', 'Jurisdiction': 'Jurisdiction'},
                 color='TotalCrime', color_continuous_scale='Reds')

    st.plotly_chart(fig, use_container_width=True)

    # Highlight the top hotspots
    st.write("Top Crime Hotspots:")
    top_hotspots = total_crime_per_jurisdiction.head(10)
    st.table(top_hotspots)

# Add the crime_hotspots function to the main navigation
def main():
    st.sidebar.title("Navigation")
    options = ["Introduction", "Trend Analysis", "Crime Distribution", "Geographical Analysis", "Population Correlation", "Crime Hotspots"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Introduction":
        introduction()
    elif choice == "Trend Analysis":
        trend_analysis()
    elif choice == "Crime Distribution":
        crime_distribution()
    elif choice == "Geographical Analysis":
        geographical_analysis()
    elif choice == "Population Correlation":
        population_correlation()
    elif choice == "Crime Hotspots":
        crime_hotspots()

if __name__ == "__main__":
    main()
