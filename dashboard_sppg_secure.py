"""
Dashboard SPPG BGN - Versi dengan Authentication
Gunakan file ini jika Anda ingin menambahkan password protection
"""

from auth import require_authentication
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Import dashboard utama
import dashboard_sppg

# Wrap main function dengan authentication
@require_authentication
def main():
    dashboard_sppg.main()

if __name__ == "__main__":
    main()
