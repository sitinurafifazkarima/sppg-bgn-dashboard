import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Dashboard SPPG BGN - Analisis EOS",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('sppg_data_complete_with_coordinates.csv')
    # Clean data
    df = df.dropna(subset=['Latitude', 'Longitude'])
    return df

# Function to create hierarchical zones
def create_zones(df):
    """
    Membuat hierarki wilayah: Zona (Pulau/Regional) -> Wilayah (Provinsi)
    """
    # Mapping provinsi ke zona berdasarkan pulau/regional
    zona_mapping = {
        # Sumatera
        'ACEH': 'Zona Sumatera',
        'SUMATERA UTARA': 'Zona Sumatera',
        'SUMATERA BARAT': 'Zona Sumatera',
        'RIAU': 'Zona Sumatera',
        'KEPULAUAN RIAU': 'Zona Sumatera',
        'JAMBI': 'Zona Sumatera',
        'SUMATERA SELATAN': 'Zona Sumatera',
        'KEPULAUAN BANGKA BELITUNG': 'Zona Sumatera',
        'BENGKULU': 'Zona Sumatera',
        'LAMPUNG': 'Zona Sumatera',
        
        # Jawa
        'BANTEN': 'Zona Jawa',
        'DKI JAKARTA': 'Zona Jawa',
        'JAWA BARAT': 'Zona Jawa',
        'JAWA TENGAH': 'Zona Jawa',
        'DAERAH ISTIMEWA YOGYAKARTA': 'Zona Jawa',
        'JAWA TIMUR': 'Zona Jawa',
        
        # Kalimantan
        'KALIMANTAN BARAT': 'Zona Kalimantan',
        'KALIMANTAN TENGAH': 'Zona Kalimantan',
        'KALIMANTAN SELATAN': 'Zona Kalimantan',
        'KALIMANTAN TIMUR': 'Zona Kalimantan',
        'KALIMANTAN UTARA': 'Zona Kalimantan',
        
        # Sulawesi
        'SULAWESI UTARA': 'Zona Sulawesi',
        'SULAWESI TENGAH': 'Zona Sulawesi',
        'SULAWESI SELATAN': 'Zona Sulawesi',
        'SULAWESI TENGGARA': 'Zona Sulawesi',
        'GORONTALO': 'Zona Sulawesi',
        'SULAWESI BARAT': 'Zona Sulawesi',
        
        # Bali & Nusa Tenggara
        'BALI': 'Zona Bali & Nusa Tenggara',
        'NUSA TENGGARA BARAT': 'Zona Bali & Nusa Tenggara',
        'NUSA TENGGARA TIMUR': 'Zona Bali & Nusa Tenggara',
        
        # Maluku & Papua
        'MALUKU': 'Zona Maluku & Papua',
        'MALUKU UTARA': 'Zona Maluku & Papua',
        'PAPUA': 'Zona Maluku & Papua',
        'PAPUA BARAT': 'Zona Maluku & Papua',
        'PAPUA TENGAH': 'Zona Maluku & Papua',
        'PAPUA PEGUNUNGAN': 'Zona Maluku & Papua',
        'PAPUA SELATAN': 'Zona Maluku & Papua',
        'PAPUA BARAT DAYA': 'Zona Maluku & Papua',
    }
    
    df['Zona'] = df['Provinsi'].map(zona_mapping)
    df['Wilayah'] = df['Provinsi']
    
    return df

# Function to calculate EOS requirements
def calculate_eos_requirements(df, sppg_per_eos=25, avg_mttr_hours=24, working_days_per_month=22):
    """
    Menghitung kebutuhan EOS berdasarkan:
    - Ratio SPPG to EOS (default: 1 EOS untuk 25 SPPG)
    - MTTR (Mean Time to Repair) - waktu rata-rata perbaikan
    - Distribusi geografis
    - Status operasional
    """
    
    # Group by Zona and Wilayah
    summary = df.groupby(['Zona', 'Wilayah']).agg({
        'ID_SPPG': 'count',
        'Status_Operasional': lambda x: (x == 'Beroperasi').sum(),
        'Latitude': ['mean', 'std'],
        'Longitude': ['mean', 'std']
    }).reset_index()
    
    summary.columns = ['Zona', 'Wilayah', 'Total_SPPG', 'SPPG_Beroperasi', 
                       'Lat_Mean', 'Lat_Std', 'Lon_Mean', 'Lon_Std']
    
    # Calculate EOS requirements
    summary['EOS_Dasar'] = np.ceil(summary['Total_SPPG'] / sppg_per_eos)
    
    # Adjustment factor based on geographical spread (higher std = more spread = need more EOS)
    summary['Spread_Factor'] = 1 + (summary['Lat_Std'].fillna(0) + summary['Lon_Std'].fillna(0)) / 10
    summary['Spread_Factor'] = summary['Spread_Factor'].clip(1, 2)  # Max 2x multiplier
    
    # Adjustment based on operational status (operational sites need more immediate support)
    summary['Operational_Factor'] = 1 + (summary['SPPG_Beroperasi'] / summary['Total_SPPG']) * 0.3
    
    # Final EOS calculation
    summary['EOS_Required'] = np.ceil(summary['EOS_Dasar'] * summary['Spread_Factor'] * summary['Operational_Factor'])
    
    # Calculate workload metrics
    summary['SPPG_per_EOS'] = summary['Total_SPPG'] / summary['EOS_Required']
    
    # Estimate monthly repair calls (assume 5% failure rate per month)
    failure_rate = 0.05
    summary['Est_Monthly_Repairs'] = (summary['SPPG_Beroperasi'] * failure_rate).round(1)
    
    # Calculate if EOS can handle workload based on MTTR
    hours_per_month = working_days_per_month * 8
    summary['Hours_Available_per_EOS'] = hours_per_month
    summary['Hours_Needed_per_Month'] = summary['Est_Monthly_Repairs'] * avg_mttr_hours
    summary['Utilization_Rate'] = (summary['Hours_Needed_per_Month'] / 
                                    (summary['EOS_Required'] * summary['Hours_Available_per_EOS']) * 100).round(1)
    
    return summary

# Main app
def main():
    st.markdown('<h1 class="main-header">🗺️ Dashboard SPPG BGN - Analisis Kebutuhan EOS</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    try:
        df = load_data()
        df = create_zones(df)
        
        # Sidebar filters
        st.sidebar.header("🔍 Filter Data")
        
        # Zona filter
        zona_options = ['Semua Zona'] + sorted(df['Zona'].dropna().unique().tolist())
        selected_zona = st.sidebar.selectbox("Pilih Zona", zona_options)
        
        # Wilayah filter
        if selected_zona != 'Semua Zona':
            wilayah_options = ['Semua Wilayah'] + sorted(df[df['Zona'] == selected_zona]['Wilayah'].unique().tolist())
        else:
            wilayah_options = ['Semua Wilayah'] + sorted(df['Wilayah'].dropna().unique().tolist())
        selected_wilayah = st.sidebar.selectbox("Pilih Wilayah (Provinsi)", wilayah_options)
        
        # Status filter
        status_options = ['Semua Status'] + df['Status_Operasional'].unique().tolist()
        selected_status = st.sidebar.selectbox("Status Operasional", status_options)
        
        # Apply filters
        df_filtered = df.copy()
        if selected_zona != 'Semua Zona':
            df_filtered = df_filtered[df_filtered['Zona'] == selected_zona]
        if selected_wilayah != 'Semua Wilayah':
            df_filtered = df_filtered[df_filtered['Wilayah'] == selected_wilayah]
        if selected_status != 'Semua Status':
            df_filtered = df_filtered[df_filtered['Status_Operasional'] == selected_status]
        
        # Sidebar - EOS Parameters
        st.sidebar.header("⚙️ Parameter EOS")
        sppg_per_eos = st.sidebar.slider("Ratio SPPG per EOS", 10, 50, 25, 5,
                                          help="Jumlah SPPG yang dapat dihandle oleh 1 EOS")
        avg_mttr = st.sidebar.slider("MTTR (jam)", 4, 72, 24, 4,
                                      help="Mean Time to Repair - rata-rata waktu perbaikan")
        working_days = st.sidebar.slider("Hari Kerja per Bulan", 15, 30, 22, 1)
        
        # Calculate EOS requirements
        eos_summary = calculate_eos_requirements(df_filtered, sppg_per_eos, avg_mttr, working_days)
        
        # Main metrics
        st.markdown("## 📊 Ringkasan Utama")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total SPPG", f"{len(df_filtered):,}")
        with col2:
            beroperasi = (df_filtered['Status_Operasional'] == 'Beroperasi').sum()
            st.metric("SPPG Beroperasi", f"{beroperasi:,}")
        with col3:
            st.metric("Total Zona", df_filtered['Zona'].nunique())
        with col4:
            st.metric("Total Wilayah", df_filtered['Wilayah'].nunique())
        with col5:
            total_eos = int(eos_summary['EOS_Required'].sum())
            st.metric("EOS Dibutuhkan", f"{total_eos:,}")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs([
            "🗺️ Peta Sebaran", 
            "👨‍🔧 Analisis EOS",
            "📈 Metrik & KPI",
            "📋 Data Detail"
        ])
        
        # TAB 1: Map View
        with tab1:
            st.markdown("### Peta Sebaran SPPG BGN")
            
            # Color mapping for status
            color_map = {
                'Beroperasi': '#2ecc71',
                'Belum Beroperasi': '#e74c3c',
                'Dalam Pembangunan': '#f39c12'
            }
            
            df_filtered['color'] = df_filtered['Status_Operasional'].map(color_map)
            
            # Create map
            fig_map = px.scatter_mapbox(
                df_filtered,
                lat='Latitude',
                lon='Longitude',
                color='Status_Operasional',
                hover_name='ID_SPPG',
                hover_data={
                    'Zona': True,
                    'Wilayah': True,
                    'Kota_Kabupaten': True,
                    'Status_Operasional': True,
                    'Alamat': True,
                    'Latitude': ':.4f',
                    'Longitude': ':.4f'
                },
                color_discrete_map=color_map,
                zoom=4,
                height=600,
                title='Distribusi SPPG di Indonesia'
            )
            
            fig_map.update_layout(
                mapbox_style="open-street-map",
                margin={"r":0,"t":40,"l":0,"b":0}
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Distribution by Zona and Wilayah
            col1, col2 = st.columns(2)
            
            with col1:
                zona_dist = df_filtered.groupby('Zona').size().reset_index(name='Count')
                fig_zona = px.bar(
                    zona_dist,
                    x='Zona',
                    y='Count',
                    title='Distribusi SPPG per Zona',
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig_zona.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_zona, use_container_width=True)
            
            with col2:
                wilayah_dist = df_filtered.groupby('Wilayah').size().reset_index(name='Count').nlargest(15, 'Count')
                fig_wilayah = px.bar(
                    wilayah_dist,
                    x='Wilayah',
                    y='Count',
                    title='Top 15 Wilayah dengan SPPG Terbanyak',
                    color='Count',
                    color_continuous_scale='Greens'
                )
                fig_wilayah.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_wilayah, use_container_width=True)
        
        # TAB 2: EOS Analysis
        with tab2:
            st.markdown("### Analisis Kebutuhan EOS per Wilayah")
            
            st.markdown("""
            <div class="info-box">
            <strong>📌 Metodologi Perhitungan EOS:</strong>
            <ul>
                <li><strong>Ratio SPPG to EOS:</strong> Jumlah SPPG yang dapat dihandle oleh 1 EOS</li>
                <li><strong>Spread Factor:</strong> Penyesuaian berdasarkan sebaran geografis (semakin tersebar = butuh lebih banyak EOS)</li>
                <li><strong>Operational Factor:</strong> Penyesuaian berdasarkan % SPPG yang beroperasi</li>
                <li><strong>MTTR:</strong> Mean Time to Repair - waktu rata-rata untuk perbaikan</li>
                <li><strong>Utilization Rate:</strong> % kapasitas EOS yang terpakai (target: 60-80%)</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Summary by Zona
            zona_summary = eos_summary.groupby('Zona').agg({
                'Total_SPPG': 'sum',
                'SPPG_Beroperasi': 'sum',
                'EOS_Required': 'sum',
                'Est_Monthly_Repairs': 'sum',
                'Utilization_Rate': 'mean'
            }).reset_index()
            
            zona_summary['SPPG_per_EOS'] = (zona_summary['Total_SPPG'] / zona_summary['EOS_Required']).round(1)
            zona_summary = zona_summary.sort_values('EOS_Required', ascending=False)
            
            st.markdown("#### 📊 Kebutuhan EOS per Zona")
            
            # Display table
            st.dataframe(
                zona_summary.style.format({
                    'Total_SPPG': '{:,.0f}',
                    'SPPG_Beroperasi': '{:,.0f}',
                    'EOS_Required': '{:,.0f}',
                    'SPPG_per_EOS': '{:.1f}',
                    'Est_Monthly_Repairs': '{:.1f}',
                    'Utilization_Rate': '{:.1f}%'
                }).background_gradient(subset=['EOS_Required'], cmap='YlOrRd'),
                use_container_width=True,
                height=300
            )
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                fig_eos = px.bar(
                    zona_summary,
                    x='Zona',
                    y='EOS_Required',
                    title='Kebutuhan EOS per Zona',
                    color='EOS_Required',
                    color_continuous_scale='Reds',
                    text='EOS_Required'
                )
                fig_eos.update_traces(textposition='outside')
                fig_eos.update_layout(xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig_eos, use_container_width=True)
            
            with col2:
                fig_util = px.bar(
                    zona_summary,
                    x='Zona',
                    y='Utilization_Rate',
                    title='Tingkat Utilisasi EOS per Zona (%)',
                    color='Utilization_Rate',
                    color_continuous_scale='RdYlGn_r',
                    text='Utilization_Rate'
                )
                fig_util.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_util.update_layout(xaxis_tickangle=-45, showlegend=False)
                fig_util.add_hline(y=80, line_dash="dash", line_color="red", 
                                   annotation_text="Target Max: 80%")
                fig_util.add_hline(y=60, line_dash="dash", line_color="green",
                                   annotation_text="Target Min: 60%")
                st.plotly_chart(fig_util, use_container_width=True)
            
            # Detailed breakdown by Wilayah
            st.markdown("#### 🔍 Detail Kebutuhan EOS per Wilayah")
            
            eos_display = eos_summary[[
                'Zona', 'Wilayah', 'Total_SPPG', 'SPPG_Beroperasi', 
                'EOS_Required', 'SPPG_per_EOS', 'Est_Monthly_Repairs', 
                'Utilization_Rate'
            ]].sort_values(['Zona', 'EOS_Required'], ascending=[True, False])
            
            st.dataframe(
                eos_display.style.format({
                    'Total_SPPG': '{:,.0f}',
                    'SPPG_Beroperasi': '{:,.0f}',
                    'EOS_Required': '{:,.0f}',
                    'SPPG_per_EOS': '{:.1f}',
                    'Est_Monthly_Repairs': '{:.1f}',
                    'Utilization_Rate': '{:.1f}%'
                }).background_gradient(subset=['Utilization_Rate'], cmap='RdYlGn_r'),
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = eos_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data EOS (CSV)",
                data=csv,
                file_name='eos_requirements.csv',
                mime='text/csv'
            )
        
        # TAB 3: Metrics & KPI
        with tab3:
            st.markdown("### 📈 Metrik & KPI Operasional")
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_eos = int(eos_summary['EOS_Required'].sum())
                avg_sppg_per_eos = (eos_summary['Total_SPPG'].sum() / total_eos)
                st.metric(
                    "Rata-rata SPPG per EOS",
                    f"{avg_sppg_per_eos:.1f}",
                    delta=f"Target: {sppg_per_eos}",
                    delta_color="normal"
                )
            
            with col2:
                avg_util = eos_summary['Utilization_Rate'].mean()
                util_status = "optimal" if 60 <= avg_util <= 80 else "perlu disesuaikan"
                st.metric(
                    "Rata-rata Utilisasi EOS",
                    f"{avg_util:.1f}%",
                    delta=util_status,
                    delta_color="normal" if 60 <= avg_util <= 80 else "inverse"
                )
            
            with col3:
                total_repairs = eos_summary['Est_Monthly_Repairs'].sum()
                st.metric(
                    "Estimasi Perbaikan/Bulan",
                    f"{total_repairs:.0f}",
                    delta=f"MTTR: {avg_mttr}h"
                )
            
            # Status operational breakdown
            st.markdown("#### Status Operasional SPPG")
            
            status_counts = df_filtered['Status_Operasional'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Jumlah']
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                fig_pie = px.pie(
                    status_counts,
                    values='Jumlah',
                    names='Status',
                    title='Distribusi Status Operasional',
                    color='Status',
                    color_discrete_map=color_map,
                    hole=0.4
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_bar_status = px.bar(
                    status_counts,
                    x='Status',
                    y='Jumlah',
                    title='Jumlah SPPG per Status',
                    color='Status',
                    color_discrete_map=color_map,
                    text='Jumlah'
                )
                fig_bar_status.update_traces(textposition='outside')
                st.plotly_chart(fig_bar_status, use_container_width=True)
            
            # MTTR Simulation
            st.markdown("#### 🔧 Simulasi MTTR & Kapasitas EOS")
            
            mttr_range = list(range(4, 73, 4))
            sim_data = []
            
            for mttr in mttr_range:
                temp_summary = calculate_eos_requirements(df_filtered, sppg_per_eos, mttr, working_days)
                sim_data.append({
                    'MTTR (jam)': mttr,
                    'Total EOS': temp_summary['EOS_Required'].sum(),
                    'Avg Utilisasi (%)': temp_summary['Utilization_Rate'].mean()
                })
            
            sim_df = pd.DataFrame(sim_data)
            
            fig_sim = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig_sim.add_trace(
                go.Scatter(x=sim_df['MTTR (jam)'], y=sim_df['Total EOS'], 
                          name='Total EOS', mode='lines+markers', line=dict(color='blue', width=3)),
                secondary_y=False
            )
            
            fig_sim.add_trace(
                go.Scatter(x=sim_df['MTTR (jam)'], y=sim_df['Avg Utilisasi (%)'],
                          name='Avg Utilisasi (%)', mode='lines+markers', line=dict(color='red', width=3)),
                secondary_y=True
            )
            
            fig_sim.update_xaxes(title_text="MTTR (jam)")
            fig_sim.update_yaxes(title_text="Total EOS Dibutuhkan", secondary_y=False)
            fig_sim.update_yaxes(title_text="Utilisasi Rata-rata (%)", secondary_y=True)
            fig_sim.update_layout(title='Dampak MTTR terhadap Kebutuhan EOS & Utilisasi', height=400)
            
            st.plotly_chart(fig_sim, use_container_width=True)
            
            st.info("""
            💡 **Insight:** 
            - MTTR yang lebih tinggi membutuhkan lebih banyak EOS untuk maintain utilisasi yang sehat
            - Target utilisasi optimal: 60-80%
            - Utilisasi > 80% = EOS overworked, risiko burnout
            - Utilisasi < 60% = Kapasitas berlebih, inefisiensi biaya
            """)
        
        # TAB 4: Detailed Data
        with tab4:
            st.markdown("### 📋 Data Detail SPPG")
            
            # Search
            search_term = st.text_input("🔍 Cari SPPG (ID, Alamat, Kota)", "")
            
            if search_term:
                df_display = df_filtered[
                    df_filtered['ID_SPPG'].str.contains(search_term, case=False, na=False) |
                    df_filtered['Alamat'].str.contains(search_term, case=False, na=False) |
                    df_filtered['Kota_Kabupaten'].str.contains(search_term, case=False, na=False)
                ]
            else:
                df_display = df_filtered
            
            st.markdown(f"**Total Records:** {len(df_display):,}")
            
            # Display data
            st.dataframe(
                df_display[[
                    'ID_SPPG', 'Zona', 'Wilayah', 'Kota_Kabupaten', 
                    'Status_Operasional', 'Status_Pengajuan', 'Alamat',
                    'Latitude', 'Longitude'
                ]],
                use_container_width=True,
                height=500
            )
            
            # Download
            csv_all = df_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data Lengkap (CSV)",
                data=csv_all,
                file_name='sppg_data_filtered.csv',
                mime='text/csv'
            )
        
    except FileNotFoundError:
        st.error("❌ File 'sppg_data_complete_with_coordinates.csv' tidak ditemukan!")
        st.info("Pastikan file CSV ada di direktori yang sama dengan script ini.")
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {str(e)}")
        st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Dashboard SPPG BGN - Analisis Kebutuhan EOS | © 2025</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
