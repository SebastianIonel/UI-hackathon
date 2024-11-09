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

# Function to show the profit margins chart
def show_profit_margins_chart():
    # Load data from info.json
    with open('info.json', 'r') as file:
        data = json.load(file)

    # Extract relevant data for the chart
    years = ["2021", "2022", "2023"]
    gross_profit_margin = [data['companyIndicators']['Indicators'][year]['Gross Profit Margin'] for year in years]
    operating_margin = [data['companyIndicators']['Indicators'][year]['Operating Margin'] for year in years]
    net_profit_margin = [data['companyIndicators']['Indicators'][year]['Net Profit Margin'] for year in years]

    # Create a DataFrame for plotting
    df = pd.DataFrame({
        "Year": years,
        "Gross Profit Margin": gross_profit_margin,
        "Operating Margin": operating_margin,
        "Net Profit Margin": net_profit_margin
    })

    # Melt the DataFrame to have a long format suitable for plotly
    df_melted = df.melt(id_vars="Year", var_name="Margin Type", value_name="Percentage")

    # Create a stacked bar chart using Plotly
    fig = px.bar(df_melted, x="Year", y="Percentage", color="Margin Type", barmode="group",
                 title="Profit Margins Over Time", labels={"Percentage": "Percentage (%)", "Margin Type": "Profit Margin Type"})
    st.plotly_chart(fig)

def show_liquidity_leverage_chart():
    # Load data from info.json
    with open('info.json', 'r') as file:
        data = json.load(file)

    # Extract relevant data for the chart
    years = ["2021", "2022", "2023"]
    current_ratio = [data['companyIndicators']['Indicators'][year]['Current Ratio'] for year in years]
    debt_to_equity_ratio = [data['companyIndicators']['Indicators'][year]['Debt-to-Equity Ratio'] for year in years]

    # Create a DataFrame for plotting
    df = pd.DataFrame({
        "Year": years,
        "Current Ratio": current_ratio,
        "Debt-to-Equity Ratio": debt_to_equity_ratio
    })

    # Melt the DataFrame to have a long format suitable for plotly
    df_melted = df.melt(id_vars="Year", var_name="Ratio Type", value_name="Value")

    # Create a line chart using Plotly
    fig = px.line(df_melted, x="Year", y="Value", color="Ratio Type", 
                  title="Liquidity and Leverage Ratios Over Time", labels={"Value": "Ratio", "Ratio Type": "Ratio Type"})
    st.plotly_chart(fig)