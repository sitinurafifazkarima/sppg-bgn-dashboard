"""
Simple test dashboard untuk troubleshooting Streamlit Cloud errors
Jalankan: streamlit run dashboard_simple_test.py
"""

import streamlit as st
import pandas as pd
import sys
import os

st.set_page_config(page_title="SPPG Dashboard Test", layout="wide")

st.title("🔍 Dashboard Test - Troubleshooting")

# System info
st.subheader("📊 System Information")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
with col2:
    st.metric("Working Directory", "✅" if os.path.exists(os.getcwd()) else "❌")
with col3:
    st.metric("Streamlit Version", st.__version__)

# Check packages
st.subheader("📦 Package Versions")
try:
    import plotly
    st.success(f"✅ Plotly: {plotly.__version__}")
except Exception as e:
    st.error(f"❌ Plotly: {str(e)}")

try:
    import numpy as np
    st.success(f"✅ NumPy: {np.__version__}")
except Exception as e:
    st.error(f"❌ NumPy: {str(e)}")

try:
    st.success(f"✅ Pandas: {pd.__version__}")
except Exception as e:
    st.error(f"❌ Pandas: {str(e)}")

# Check file existence
st.subheader("📁 File Check")

files_to_check = [
    'sppg_data_complete_with_coordinates.csv',
    'dashboard_sppg.py',
    'requirements.txt'
]

for file in files_to_check:
    if os.path.exists(file):
        size = os.path.getsize(file) / 1024  # KB
        st.success(f"✅ {file} - {size:.1f} KB")
    else:
        st.error(f"❌ {file} - NOT FOUND")

# Try to load CSV
st.subheader("🔄 Data Loading Test")

try:
    with st.spinner("Loading CSV..."):
        df = pd.read_csv('sppg_data_complete_with_coordinates.csv')
    
    st.success(f"✅ CSV loaded successfully!")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", f"{len(df):,}")
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
    with col4:
        valid_coords = df.dropna(subset=['Latitude', 'Longitude'])
        st.metric("Valid Coordinates", f"{len(valid_coords):,}")
    
    st.subheader("📋 Column Names")
    st.write(df.columns.tolist())
    
    st.subheader("🔍 Sample Data (First 5 rows)")
    st.dataframe(df.head(), use_container_width=True)
    
    st.subheader("📊 Data Types")
    st.write(df.dtypes)
    
    st.subheader("❓ Missing Values")
    missing = df.isnull().sum()
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing': missing.values,
        'Percentage': (missing.values / len(df) * 100).round(2)
    })
    st.dataframe(missing_df[missing_df['Missing'] > 0], use_container_width=True)
    
except FileNotFoundError as e:
    st.error(f"❌ CSV file not found: {str(e)}")
    st.info("📁 Current working directory: " + os.getcwd())
    st.info("📂 Files in current directory:")
    try:
        files = os.listdir('.')
        for f in files[:20]:  # Show first 20 files
            st.text(f"  - {f}")
    except Exception as e:
        st.error(f"Cannot list directory: {str(e)}")
        
except Exception as e:
    st.error(f"❌ Error loading CSV: {str(e)}")
    st.exception(e)

# Test plotly
st.subheader("📈 Plotly Test")
try:
    import plotly.express as px
    
    # Simple test chart
    test_data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    })
    
    fig = px.line(test_data, x='x', y='y', title='Test Chart')
    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ Plotly working!")
    
except Exception as e:
    st.error(f"❌ Plotly error: {str(e)}")

# Environment info
st.subheader("🌍 Environment Variables")
with st.expander("Show environment (click to expand)"):
    env_vars = {
        'PATH': os.environ.get('PATH', 'N/A'),
        'HOME': os.environ.get('HOME', 'N/A'),
        'PWD': os.environ.get('PWD', 'N/A'),
    }
    for key, value in env_vars.items():
        st.text(f"{key}: {value[:100]}...")  # First 100 chars

st.markdown("---")
st.success("✅ If you see this, Streamlit is working!")
st.info("🔍 Check the results above to identify any issues.")
