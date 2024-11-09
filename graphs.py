import plotly.express as px
import streamlit as st
import pandas as pd
import json

def show_revenue_net_income_chart():
    # Load data from info.json
    with open('info.json', 'r') as file:
        data = json.load(file)

    # Extract relevant data for the chart
    years = ["2021", "2022", "2023"]
    revenue = [data['companyInfo']['Financials'][year]['Revenue'] for year in years]
    net_income = [data['companyInfo']['Financials'][year]['Net_Income'] for year in years]

    # Create a DataFrame for plotting
    df = pd.DataFrame({
        "Year": years,
        "Revenue": revenue,
        "Net Income": net_income
    })

    # Create a line chart using Plotly
    fig = px.line(df, x="Year", y=["Revenue", "Net Income"], title="Revenue and Net Income Over Time", labels={"value": "Amount", "variable": "Metric"})
    st.plotly_chart(fig)
