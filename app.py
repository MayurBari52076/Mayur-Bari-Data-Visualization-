# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Universal Insights Generator", page_icon=":bar_chart:", layout="wide")

# App title
st.title("📊 Universal Insights Generator")
st.markdown("Upload any CSV file to automatically generate high-value insights and visualizations!")

# Upload CSV file
uploaded_file = st.file_uploader("🔼 Upload your CSV file", type=["csv"])

st.markdown("---")

if uploaded_file is not None:
    # Read the CSV
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Data overview
    st.header("1. 📄 Data Preview")
    st.dataframe(df.head())

    # Dataset summary
    st.header("2. 📋 Dataset Summary")
    with st.expander("🔍 View Summary Statistics"):
        st.dataframe(df.describe(include='all'))

    # Missing Values
    st.header("3. ❗ Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        st.dataframe(missing)
    else:
        st.success("✅ No missing values found!")

    # Data types
    st.header("4. 🧬 Column Data Types")
    st.dataframe(df.dtypes)

    # Identify numerical and categorical columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    st.markdown("---")

    # Correlation Heatmap
    st.header("5. ♨️ Correlation Heatmap (Numerical Data)")
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", linewidths=0.5)
        st.pyplot(fig)
    else:
        st.info("Not enough numerical columns to generate a correlation heatmap.")

    st.markdown("---")

    # Visualizations Section
    st.header("6. 📊 Visualizations")

    if num_cols:
        with st.expander("📈 Histograms (Numerical Columns)"):
            for col in num_cols:
                fig = px.histogram(df, x=col, title=f"Histogram of {col}", color_discrete_sequence=["#1abc9c"])
                st.plotly_chart(fig, use_container_width=True)

        with st.expander("📉 Line Charts (Numerical Columns)"):
            for col in num_cols:
                fig = px.line(df, y=col, title=f"Line Chart of {col}", markers=True)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No numerical columns available for Histograms and Line Charts.")

    if cat_cols:
        with st.expander("🧩 Pie Charts (Categorical Columns)"):
            for col in cat_cols:
                if df[col].nunique() <= 10 and df[col].notnull().sum() > 0:
                    fig = px.pie(df, names=col, title=f"Pie Chart of {col}", hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)

        with st.expander("📊 Bar Charts (Categorical Columns)"):
            for col in cat_cols:
                if df[col].nunique() <= 20 and df[col].notnull().sum() > 0:
                    freq = df[col].value_counts().reset_index()
                    freq.columns = [col, 'Count']
                    fig = px.bar(freq, x=col, y='Count', title=f"Bar Chart of {col}",
                                 color_discrete_sequence=["#e74c3c"])
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No categorical columns available for Pie and Bar Charts.")

    st.success("✅ Visualizations generated successfully!")
else:
    st.info("Please upload a CSV file to start.")
