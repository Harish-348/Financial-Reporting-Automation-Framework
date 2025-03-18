import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db_connection import fetch_table_data

# Streamlit Page Config
st.set_page_config(page_title="Financial Data Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("Dashboard Navigation")
section = st.sidebar.radio("Go to:", ["View Data Tables", "KPI Analysis", "Aggregate Functions", "Data Marts"])

# Tables available in the database
tables = {
    "dm_financial_performance": "Financial Performance Data Mart",
    "dm_market_stock_performance": "Market Stock Performance",
    "dm_dividend_investor_insights": "Dividend Investor Insights",
    "kpi_stock_performance": "Stock Performance KPIs",
    "kpi_financial_performance": "Financial Performance KPIs",
    "kpi_profitability": "Profitability KPIs",
    "kpi_price_volatility": "Price Volatility KPIs",
    "agg_financials_monthly": "Monthly Financial Aggregates",
    "agg_financials_quarterly": "Quarterly Financial Aggregates",
    "agg_financials_annual": "Annual Financial Aggregates"
}

# 🚀 View Data Tables
if section == "View Data Tables":
    st.title(" View Data Tables")
    selected_table = st.sidebar.selectbox("Select a Table", list(tables.keys()), format_func=lambda x: tables[x])
    df = fetch_table_data(selected_table)
    if not df.empty:
        st.subheader(f"{tables[selected_table]}")
        st.dataframe(df)
    else:
        st.error("No data available")

# KPI Analysis
elif section == "KPI Analysis":
    st.title(" KPI Analysis")
    kpi_table = st.sidebar.selectbox("Select KPI Table", ["kpi_stock_performance", "kpi_financial_performance", "kpi_profitability", "kpi_price_volatility"])
    df = fetch_table_data(kpi_table)
    if not df.empty:
        st.subheader(f" {tables[kpi_table]}")
        st.dataframe(df)
        time_col = "date"
        df[time_col] = pd.to_datetime(df[time_col])
        df = df.sort_values(time_col)
        
        # KPI Trends with Rolling Average
        st.subheader("KPI Trends Over Time")
        kpi_metric = st.selectbox("Select KPI Metric", df.select_dtypes(include=['number']).columns)
        df["rolling_avg"] = df[kpi_metric].rolling(window=5, min_periods=1).mean()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df, x=time_col, y="rolling_avg", ax=ax, label="5-period Rolling Avg")
        ax.set_title(f"Trend of {kpi_metric} Over Time")
        st.pyplot(fig)
    else:
        st.error("No KPI data found")

#  Aggregate Functions
elif section == "Aggregate Functions":
    st.title("Aggregate Functions")
    selected_table = st.sidebar.selectbox("Select Aggregate Table", ["agg_financials_monthly", "agg_financials_quarterly", "agg_financials_annual"])
    df = fetch_table_data(selected_table)
    if not df.empty:
        st.subheader(f"{tables[selected_table]}")
        st.dataframe(df.describe())
        
        # Aggregated Trends Visualization
        st.subheader("Aggregated Trends")
        time_col = df.columns[0]  # Assuming first column is time-related
        agg_metric = st.selectbox("Select Metric", df.select_dtypes(include=['number']).columns)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x=time_col, y=agg_metric, ax=ax, palette="coolwarm")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_title(f"{agg_metric} Trends ({tables[selected_table]})")
        st.pyplot(fig)
    else:
        st.error("No data found")

# Data Marts
elif section == "Data Marts":
    st.title(" Data Mart Insights")
    dm_table = st.sidebar.selectbox("Select Data Mart", ["dm_financial_performance", "dm_market_stock_performance", "dm_dividend_investor_insights"])
    df = fetch_table_data(dm_table)
    if not df.empty:
        st.subheader(f" {tables[dm_table]}")
        st.dataframe(df)
        
        # Time Series Trends
        st.subheader("Trends Over Time")
        time_col = "reporting_date"
        df[time_col] = pd.to_datetime(df[time_col])
        df = df.sort_values(time_col)
        metric = st.selectbox("Select Metric", df.select_dtypes(include=['number']).columns)
        df["rolling_avg"] = df[metric].rolling(window=5, min_periods=1).mean()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df, x=time_col, y="rolling_avg", ax=ax, label="5-period Rolling Avg")
        ax.set_title(f"Trend of {metric} Over Time")
        st.pyplot(fig)
    else:
        st.error("No data available")
