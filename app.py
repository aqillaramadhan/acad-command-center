import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup Halaman (Full Screen & Hide Sidebar default)
st.set_page_config(page_title="Academic Dashboard", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")

# 2. Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv('data_akademik_dummy.csv')

df = load_data()

# 3. CSS Super Custom (New Deep Purple Background - KEEPS THE LAYOUT)
st.markdown("""
    <style>
    /* Gradient Ungu Mewah & Gelap (Ganti Biru Butek) */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0B001F 0%, #1A0A3A 100%); /* Deep Dark Purple to Violet */
        color: #E2E8F0;
    }
    
    /* Sembunyiin top bar dan footer Streamlit bawaan */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Styling Custom Card (Biar nempel di Background Ungu) */
    .custom-card {
        background: rgba(255, 255, 255, 0.03); /* Soft glass */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-left: 5px solid #9F7AEA; /* Aksen ungu pastel yang nyala */
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 24px;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .card-title {
        font-size: 1.1rem;
        color: #A0AEC0; 
        font-weight: 600;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .card-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    .card-value span { font-size: 1.2rem; color: #9F7AEA; } /* Satuan ungu */
    
    /* Styling pemisah */
    hr {
        border-color: rgba(255,255,255,0.08);
        margin-top: 2.5rem;
        margin-bottom: 2.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Header Custom (SAMA PERSIS)
st.markdown("<h1 style='text-align: center; color: #B794F4; font-weight: 800; font-size: 3rem;'>🏛️ Academic Command Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #CBD5E1; font-size: 1.2rem; margin-bottom: 3rem;'>Executive Dashboard for Academic Evaluation & Monitoring</p>", unsafe_allow_html=True)

# 5. Panel Filter di Atas (SAMA PERSIS)
st.markdown("<h3 style='color: #B794F4;'>🎛️ Control Panel</h3>", unsafe_allow_html=True)
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_jalur = st.multiselect(
        "Pilih Jalur Masuk:",
        options=df['Jalur_Masuk'].unique(),
        default=df['Jalur_Masuk'].unique()
    )

with filter_col2:
    selected_status = st.multiselect(
        "Status Akademik:",
        options=df['Status_Akademik'].unique(),
        default=df['Status_Akademik'].unique()
    )

filtered_df = df[(df['Jalur_Masuk'].isin(selected_jalur)) & (df['Status_Akademik'].isin(selected_status))]
st.markdown("<hr>", unsafe_allow_html=True)

# 6. Barisan Metrik (SAMA PERSIS)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-title">Total Mahasiswa</div>
        <div class="card-value">{len(filtered_df)} <span>Orang</span></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-title">Rata-rata Nilai</div>
        <div class="card-value">{filtered_df['Rata_Rata'].mean():.2f} <span>⭐</span></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-title">Kehadiran Global</div>
        <div class="card-value">{filtered_df['Tingkat_Kehadiran'].mean():.1f}<span>%</span></div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    mahasiswa_kritis = len(filtered_df[filtered_df['Status_Akademik'] == 'Butuh Evaluasi'])
    st.markdown(f"""
    <div class="custom-card" style="border-left-color: #FC8181;">
        <div class="card-title" style="color: #FC8181;">Critical Watchlist</div>
        <div class="card-value" style="color: #FC8181;">{mahasiswa_kritis} <span>Mahasiswa</span></div>
    </div>
    """, unsafe_allow_html=True)

# 7. Visualisasi Data (SAMA PERSIS)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### 📊 Proporsi Status Akademik")
    fig_pie = px.pie(filtered_df, names='Status_Akademik', color='Status_Akademik',
                     color_discrete_map={'Aman': '#48BB78', 'Butuh Evaluasi': '#F56565'},
                     hole=0.5, template="plotly_dark")
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.markdown("### 📈 Rata-rata Nilai per Jalur Masuk")
    avg_per_jalur = filtered_df.groupby('Jalur_Masuk')['Rata_Rata'].mean().reset_index()
    fig_bar = px.bar(avg_per_jalur, x='Jalur_Masuk', y='Rata_Rata', 
                     text_auto='.2f', color='Jalur_Masuk',
                     color_discrete_sequence=['#9F7AEA', '#B794F4', '#D6BCFA'], template="plotly_dark")
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 8. Tabel Data Mentah (SAMA PERSIS)
st.markdown("### 📋 Database Eksekutif")
st.dataframe(filtered_df, use_container_width=True, height=300)