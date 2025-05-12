import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
import bcrypt
import json
from pathlib import Path
import os
from datetime import datetime
import base64
from PIL import Image
import requests
from io import BytesIO
from utils import (
    clean_data,
    compare_datasets,
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_heatmap,
    get_download_link,
    apply_filters
)

# Page configuration
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the data
    df = pd.read_csv(uploaded_file)
    
    # Clean the data
    df = clean_data(df)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    filters = {}
    
    for column in df.columns:
        if df[column].dtype == 'object':
            unique_values = df[column].unique()
            selected_values = st.sidebar.multiselect(
                f"Select {column}",
                options=unique_values,
                default=unique_values
            )
            if selected_values:
                filters[column] = selected_values
    
    # Apply filters
    filtered_df = apply_filters(df, filters)
    
    # Display basic information
    st.header("Dataset Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Dataset Shape:", filtered_df.shape)
        st.write("Columns:", list(filtered_df.columns))
    
    with col2:
        st.write("Missing Values:")
        st.write(filtered_df.isnull().sum())
    
    # Data visualization
    st.header("Data Visualization")
    
    # Select visualization type
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap"]
    )
    
    if viz_type == "Line Chart":
        x_col = st.selectbox("Select X-axis", filtered_df.columns)
        y_col = st.selectbox("Select Y-axis", filtered_df.select_dtypes(include=['number']).columns)
        fig = create_line_chart(filtered_df, x_col, y_col, f"{y_col} vs {x_col}")
        st.plotly_chart(fig)
    
    elif viz_type == "Bar Chart":
        x_col = st.selectbox("Select X-axis", filtered_df.columns)
        y_col = st.selectbox("Select Y-axis", filtered_df.select_dtypes(include=['number']).columns)
        fig = create_bar_chart(filtered_df, x_col, y_col, f"{y_col} by {x_col}")
        st.plotly_chart(fig)
    
    elif viz_type == "Pie Chart":
        values_col = st.selectbox("Select Values", filtered_df.select_dtypes(include=['number']).columns)
        names_col = st.selectbox("Select Categories", filtered_df.columns)
        fig = create_pie_chart(filtered_df, values_col, names_col, f"{values_col} by {names_col}")
        st.plotly_chart(fig)
    
    elif viz_type == "Heatmap":
        fig = create_heatmap(filtered_df, "Correlation Heatmap")
        st.plotly_chart(fig)
    
    # Download options
    st.header("Download Data")
    file_type = st.radio("Select file type", ["csv", "excel"])
    download_link = get_download_link(filtered_df, "filtered_data", file_type)
    st.markdown(download_link, unsafe_allow_html=True)
    
    # Display raw data
    st.header("Raw Data")
    st.dataframe(filtered_df)

# Custom CSS
def load_css():
    st.markdown("""
        <style>
        /* Dark theme colors */
        :root {
            --primary-color: #1E3A8A;
            --secondary-color: #2563EB;
            --background-dark: #0F172A;
            --card-bg: #1E293B;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --accent-color: #3B82F6;
            --success-color: #059669;
            --error-color: #DC2626;
        }

        /* Main container styling */
        .main {
            background: var(--background-dark);
            color: var(--text-primary);
            padding: 2rem;
        }
        
        /* Header styling */
        .stApp header {
            background-color: var(--primary-color);
            color: var(--text-primary);
        }
        
        /* Title styling */
        h1, h2, h3 {
            color: var(--text-primary);
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: var(--text-primary);
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        
        .stButton>button:hover {
            background: linear-gradient(45deg, var(--secondary-color), var(--primary-color));
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 2rem 1rem;
        }
        
        .sidebar .sidebar-content {
            background: transparent;
        }
        
        /* Card styling */
        .card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Form styling */
        .stForm {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Input field styling */
        .stTextInput>div>div>input {
            background-color: var(--background-dark);
            color: var(--text-primary);
            border-radius: 8px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            padding: 0.5rem;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }
        
        /* Selectbox styling */
        .stSelectbox>div>div>select {
            background-color: var(--background-dark);
            color: var(--text-primary);
            border-radius: 8px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            padding: 0.5rem;
        }
        
        /* File uploader styling */
        .stFileUploader>div>div>button {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: var(--text-primary);
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        
        /* Success message styling */
        .stSuccess {
            background-color: rgba(5, 150, 105, 0.2);
            color: #34D399;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--success-color);
        }
        
        /* Error message styling */
        .stError {
            background-color: rgba(220, 38, 38, 0.2);
            color: #F87171;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--error-color);
        }
        
        /* Chart container styling */
        .chart-container {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background-color: var(--card-bg);
            border-radius: 8px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: var(--background-dark);
            border-radius: 8px;
            gap: 1rem;
            padding-top: 10px;
            padding-bottom: 10px;
            color: var(--text-secondary);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color);
            color: var(--text-primary);
        }

        /* Logo styling */
        .logo-container {
            text-align: center;
            margin-bottom: 2rem;
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .logo-container img {
            max-width: 200px;
            height: auto;
            margin-bottom: 1rem;
            filter: brightness(1.2);
        }

        /* Brand name styling */
        .brand-name {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            text-align: center;
            margin-bottom: 0.5rem;
            font-family: 'Segoe UI', sans-serif;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .brand-tagline {
            font-size: 1.2rem;
            color: var(--text-secondary);
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Metric styling */
        .stMetric {
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Dataframe styling */
        .stDataFrame {
            background: var(--card-bg);
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Plot styling */
        .js-plotly-plot {
            background: var(--card-bg) !important;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--background-dark);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-color);
        }
        </style>
    """, unsafe_allow_html=True)

def load_logo():
    # Load Kuber Industry logo
    logo_url = "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100066162236707"
    try:
        response = requests.get(logo_url)
        logo = Image.open(BytesIO(response.content))
        return logo
    except:
        return None

# Authentication
def init_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # Display logo and brand name
        logo = load_logo()
        if logo:
            st.image(logo, use_column_width=True)
        
        st.markdown("""
            <div class='brand-name'>KUBER INDUSTRY</div>
            <div class='brand-tagline'>Advanced Analytics Dashboard</div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "admin"
                    st.success("Login successful! Redirecting to dashboard...")
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials! Please try again.")

def signup():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # Display logo and brand name
        logo = load_logo()
        if logo:
            st.image(logo, use_column_width=True)
        
        st.markdown("""
            <div class='brand-name'>KUBER INDUSTRY</div>
            <div class='brand-tagline'>Create Your Account</div>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username", placeholder="Enter desired username")
            new_password = st.text_input("Choose Password", type="password", placeholder="Enter password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    # Auto-login after successful signup
                    st.session_state.authenticated = True
                    st.session_state.user_role = "user"  # Default role
                    st.success("Registration successful! Logging you in...")
                    st.experimental_rerun()

# Main Dashboard
def main_dashboard():
    # Display logo in sidebar
    with st.sidebar:
        logo = load_logo()
        if logo:
            st.image(logo, use_column_width=True)
        
        st.markdown("""
            <div class='brand-name' style='font-size: 1.5rem;'>KUBER INDUSTRY</div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio("Navigation", ["Home", "Static Data", "Dynamic Comparison", "Settings"])
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; margin-top: 2rem;'>
                <p style='color: #6B7280;'>Logged in as: {}</p>
            </div>
        """.format(st.session_state.user_role), unsafe_allow_html=True)
    
    if page == "Home":
        show_home()
    elif page == "Static Data":
        show_static_data()
    elif page == "Dynamic Comparison":
        show_dynamic_comparison()
    elif page == "Settings":
        show_settings()

def show_home():
    st.markdown("""
        <div class='card' style='margin-bottom: 2rem;'>
            <h2 style='margin-bottom: 0.5rem;'>Welcome to <span style="color: var(--accent-color);">Kuber Industry Analytics</span></h2>
            <p style='color: var(--text-secondary); font-size: 1.1rem;'>Your default data visualization dashboard</p>
        </div>
    """, unsafe_allow_html=True)

    try:
        df = pd.read_csv(r"C:\Users\HIMANSHU\OneDrive\Desktop\New folder (5)\Test.csv")

        st.markdown("""
            <div class='card' style='margin-bottom: 2rem;'>
                <h3 style='margin-bottom: 0.5rem;'>Data Overview</h3>
                <div style='display: flex; gap: 2rem;'>
                    <div style='flex:1;'>
                        <div class='stMetric'>
                            <span style='font-size: 1.2rem; color: var(--text-secondary);'>Total Rows</span><br>
                            <span style='font-size: 2rem; font-weight: bold; color: var(--accent-color);'>{}</span>
                        </div>
                    </div>
                    <div style='flex:1;'>
                        <div class='stMetric'>
                            <span style='font-size: 1.2rem; color: var(--text-secondary);'>Total Columns</span><br>
                            <span style='font-size: 2rem; font-weight: bold; color: var(--accent-color);'>{}</span>
                        </div>
                    </div>
                    <div style='flex:1;'>
                        <div class='stMetric'>
                            <span style='font-size: 1.2rem; color: var(--text-secondary);'>Memory Usage</span><br>
                            <span style='font-size: 2rem; font-weight: bold; color: var(--accent-color);'>{}</span>
                        </div>
                    </div>
                </div>
            </div>
        """.format(len(df), len(df.columns), f"{df.memory_usage().sum() / 1024:.2f} KB"), unsafe_allow_html=True)

        st.markdown("""
            <div class='card' style='margin-bottom: 2rem;'>
                <h3 style='margin-bottom: 0.5rem;'>Data Visualizations</h3>
                <p style='color: var(--text-secondary); margin-bottom: 1rem;'>Select one or more chart types to visualize your data. Each chart will appear in its own card below.</p>
            </div>
        """, unsafe_allow_html=True)

        chart_types = ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap", "Scatter Plot", "Box Plot"]
        selected_charts = st.multiselect(
            "Select Chart Types",
            chart_types,
            default=["Line Chart", "Bar Chart"],
            help="Choose multiple chart types to display below."
        )

        for idx, chart_type in enumerate(selected_charts):
            st.markdown(f"""
                <div class='card' style='margin-bottom: 2rem; border-left: 6px solid var(--accent-color);'>
                    <h4 style='margin-bottom: 1rem;'>{chart_type}</h4>
            """, unsafe_allow_html=True)

            if chart_type == "Line Chart":
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("Select X-axis", df.columns, key=f"line_x_{idx}")
                with col2:
                    y_col = st.selectbox("Select Y-axis", df.columns, key=f"line_y_{idx}")
                fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
                fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Bar Chart":
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("Select X-axis", df.columns, key=f"bar_x_{idx}")
                with col2:
                    y_col = st.selectbox("Select Y-axis", df.columns, key=f"bar_y_{idx}")
                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Pie Chart":
                col1, col2 = st.columns(2)
                with col1:
                    value_col = st.selectbox("Select Values", df.columns, key=f"pie_value_{idx}")
                with col2:
                    name_col = st.selectbox("Select Categories", df.columns, key=f"pie_name_{idx}")
                fig = px.pie(df, values=value_col, names=name_col, title=f"Distribution of {value_col}")
                fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Heatmap":
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                corr = df[numeric_cols].corr()
                fig = px.imshow(corr, title="Correlation Heatmap")
                fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Scatter Plot":
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("Select X-axis", df.columns, key=f"scatter_x_{idx}")
                with col2:
                    y_col = st.selectbox("Select Y-axis", df.columns, key=f"scatter_y_{idx}")
                with col3:
                    color_col = st.selectbox("Select Color", df.columns, key=f"scatter_color_{idx}")
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
                fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Box Plot":
                col1, col2 = st.columns(2)
                with col1:
                    y_col = st.selectbox("Select Y-axis", df.columns, key=f"box_y_{idx}")
                with col2:
                    x_col = st.selectbox("Select X-axis (optional)", ["None"] + list(df.columns), key=f"box_x_{idx}")
                if x_col == "None":
                    fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
                else:
                    fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot of {y_col} by {x_col}")
                fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading default data: {str(e)}")

def show_static_data():
    st.markdown("""
        <div class='card'>
            <h2>Static Data Analysis</h2>
            <p style='color: var(--text-secondary);'>Upload and analyze your static datasets</p>
        </div>
    """, unsafe_allow_html=True)
    
    # File uploader for static data
    uploaded_file = st.file_uploader("Upload your static data file", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # Data preview
        st.markdown("""
            <div class='card'>
                <h3>Data Preview</h3>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)
        
        # Visualization options
        st.markdown("""
            <div class='card'>
                <h3>Visualization Options</h3>
            </div>
        """, unsafe_allow_html=True)
        
        viz_type = st.selectbox("Select Visualization Type", 
                              ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap"])
        
        if viz_type == "Line Chart":
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Select X-axis", df.columns)
            with col2:
                y_col = st.selectbox("Select Y-axis", df.columns)
            
            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Bar Chart":
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Select X-axis", df.columns)
            with col2:
                y_col = st.selectbox("Select Y-axis", df.columns)
            
            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Pie Chart":
            col1, col2 = st.columns(2)
            with col1:
                value_col = st.selectbox("Select Values", df.columns)
            with col2:
                name_col = st.selectbox("Select Categories", df.columns)
            
            fig = px.pie(df, values=value_col, names=name_col, title=f"Distribution of {value_col}")
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Heatmap":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr, title="Correlation Heatmap")
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            st.plotly_chart(fig, use_container_width=True)

def show_dynamic_comparison():
    st.markdown("""
        <div class='card'>
            <h2>Dynamic Data Comparison</h2>
            <p style='color: var(--text-secondary);'>Compare and analyze multiple datasets</p>
        </div>
    """, unsafe_allow_html=True)
    
    # File uploaders for two datasets
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='card'>
                <h3>First Dataset</h3>
            </div>
        """, unsafe_allow_html=True)
        file1 = st.file_uploader("Upload first dataset", type=['csv', 'xlsx'])
    
    with col2:
        st.markdown("""
            <div class='card'>
                <h3>Second Dataset</h3>
            </div>
        """, unsafe_allow_html=True)
        file2 = st.file_uploader("Upload second dataset", type=['csv', 'xlsx'])
    
    if file1 is not None and file2 is not None:
        df1 = pd.read_csv(file1) if file1.name.endswith('.csv') else pd.read_excel(file1)
        df2 = pd.read_csv(file2) if file2.name.endswith('.csv') else pd.read_excel(file2)
        
        # Compare datasets
        st.markdown("""
            <div class='card'>
                <h3>Dataset Comparison</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Basic comparison metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Dataset 1 Shape", str(df1.shape))
        with col2:
            st.metric("Dataset 2 Shape", str(df2.shape))
        
        # Multiple Chart Options for Comparison
        chart_types = ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap", "Scatter Plot", "Box Plot"]
        selected_charts = st.multiselect("Select Chart Types for Comparison", chart_types, default=["Line Chart", "Bar Chart"])

        # Generate selected charts for both datasets
        for chart_type in selected_charts:
            st.markdown(f"""
                <div class='card'>
                    <h4>{chart_type} Comparison</h4>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Dataset 1")
                if chart_type == "Line Chart":
                    x_col = st.selectbox("Select X-axis", df1.columns, key=f"line_x1")
                    y_col = st.selectbox("Select Y-axis", df1.columns, key=f"line_y1")
                    fig = px.line(df1, x=x_col, y=y_col, title=f"Dataset 1: {y_col} over {x_col}")
                    fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### Dataset 2")
                if chart_type == "Line Chart":
                    x_col = st.selectbox("Select X-axis", df2.columns, key=f"line_x2")
                    y_col = st.selectbox("Select Y-axis", df2.columns, key=f"line_y2")
                    fig = px.line(df2, x=x_col, y=y_col, title=f"Dataset 2: {y_col} over {x_col}")
                    fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig, use_container_width=True)

            # Add similar chart generation for other chart types...
            # (Bar Chart, Pie Chart, Heatmap, Scatter Plot, Box Plot)

def show_settings():
    st.markdown("""
        <div class='card'>
            <h2>Settings</h2>
            <p>Customize your dashboard experience</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Theme selection
    st.markdown("""
        <div class='card'>
            <h3>Appearance</h3>
        </div>
    """, unsafe_allow_html=True)
    theme = st.selectbox("Select Theme", ["Light", "Dark"])
    
    # Download options
    st.markdown("""
        <div class='card'>
            <h3>Export Settings</h3>
        </div>
    """, unsafe_allow_html=True)
    download_format = st.multiselect("Select download formats", 
                                   ["PDF", "CSV", "PNG"])
    
    # Save settings
    if st.button("Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")

# Main app flow
def main():
    load_css()
    init_auth()
    
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            login()
        with tab2:
            signup()
    else:
        main_dashboard()

if __name__ == "__main__":
    main() 