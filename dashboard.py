import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="COVID-19 Global Tracker",
    page_icon="🦠",
    layout="wide"
)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('owid-covid-data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar controls
st.sidebar.header("Dashboard Controls")
selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=sorted(df['location'].unique()),
    default=["Kenya", "United States", "India"]
)

date_range = st.sidebar.date_input(
    "Select date range",
    value=[datetime(2021,1,1), datetime(2023,1,1)],
    min_value=datetime(2020,1,1),
    max_value=datetime.today()
)

# Main content
st.title("🌍 COVID-19 Global Data Tracker")
st.markdown("Interactive dashboard for analyzing pandemic trends")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Cases & Deaths", "Vaccinations", "Comparative Analysis"])

with tab1:
    st.header("Case and Death Trends")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("New Cases")
        fig_cases = px.line(
            df[(df['location'].isin(selected_countries)) & 
               (df['date'].between(*date_range))],
            x='date', y='new_cases_smoothed_per_million',
            color='location',
            labels={'new_cases_smoothed_per_million': 'Cases per million'},
            height=500
        )
        st.plotly_chart(fig_cases, use_container_width=True)
    
    with col2:
        st.subheader("New Deaths")
        fig_deaths = px.line(
            df[(df['location'].isin(selected_countries)) & 
               (df['date'].between(*date_range))],
            x='date', y='new_deaths_smoothed_per_million',
            color='location',
            labels={'new_deaths_smoothed_per_million': 'Deaths per million'},
            height=500
        )
        st.plotly_chart(fig_deaths, use_container_width=True)

with tab2:
    st.header("Vaccination Progress")
    
    # Vaccination metrics
    vacc_metric = st.radio(
        "Select vaccination metric",
        options=['total_vaccinations_per_hundred', 'people_fully_vaccinated_per_hundred'],
        index=0,
        horizontal=True
    )
    
    fig_vacc = px.line(
        df[(df['location'].isin(selected_countries)) & 
           (df['date'].between(*date_range))],
        x='date', y=vacc_metric,
        color='location',
        labels={vacc_metric: 'Vaccination coverage'},
        height=600
    )
    st.plotly_chart(fig_vacc, use_container_width=True)

with tab3:
    st.header("Country Comparison")
    
    # Latest data comparison
    latest = df[df['date'] == df['date'].max()]
    latest_filtered = latest[latest['location'].isin(selected_countries)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Total Cases per Million")
        fig_bar_cases = px.bar(
            latest_filtered.sort_values('total_cases_per_million', ascending=False),
            x='location', y='total_cases_per_million',
            color='location',
            labels={'total_cases_per_million': 'Cases per million'},
            height=500
        )
        st.plotly_chart(fig_bar_cases, use_container_width=True)
    
    with col2:
        st.subheader("Vaccination Coverage")
        fig_bar_vacc = px.bar(
            latest_filtered.sort_values('people_fully_vaccinated_per_hundred', ascending=False),
            x='location', y='people_fully_vaccinated_per_hundred',
            color='location',
            labels={'people_fully_vaccinated_per_hundred': 'Fully vaccinated (%)'},
            height=500
        )
        st.plotly_chart(fig_bar_vacc, use_container_width=True)

# Add download button for filtered data
csv = df[(df['location'].isin(selected_countries)) & 
         (df['date'].between(*date_range))].to_csv(index=False)
st.sidebar.download_button(
    label="Download filtered data",
    data=csv,
    file_name='filtered_covid_data.csv',
    mime='text/csv'
)
