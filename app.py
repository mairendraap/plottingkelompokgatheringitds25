import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Data Plotting ITDS 25",
    layout="centered"
)

# 2. Custom CSS (Minimalist: Full Black Text, Light Blue Accents)
st.markdown("""
    <style>
    /* Reset Background & Base Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Inter', sans-serif;
    }

    /* Hilangkan Header Streamlit */
    header {visibility: hidden;}

    /* Full Black Text untuk semua elemen teks */
    h1, h2, h3, p, span, div, label {
        color: #000000 !important;
    }

    /* Input Box Minimalis */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #000000;
        background-color: #FFFFFF;
        color: #000000 !important;
        padding: 12px;
    }

    /* Kotak Informasi dengan Aksen Biru Muda di Sisi Kiri */
    .info-box {
        border: 1px solid #E2E8F0;
        border-left: 5px solid #BAE6FD; /* Aksen Biru Muda */
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: #F8FAFC;
    }

    .label-text {
        color: #475569 !important; /* Abu gelap untuk label agar hirarki jelas */
        font-size: 11px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    .value-text {
        color: #000000 !important;
        font-size: 16px;
        font-weight: 600;
    }

    /* Landing Page Styling */
    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        border: 1px dashed #BAE6FD;
        border-radius: 20px;
        background-color: #F0F9FF;
        margin-top: 20px;
    }

    /* Styling Tabel dengan Header Biru Muda */
    .stDataFrame {
        border: 1px solid #BAE6FD;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = 'PLOTTING KELOMPOK_GATHERING ITDS 25_PENS - PLOTTING.csv'
    try:
        df = pd.read_csv(file_path, skiprows=3)
        df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
        df = df.dropna(subset=['Kelompok', 'NAMA'])
        df['Kelompok'] = df['Kelompok'].astype(int)
        return df
    except:
        return None

# --- HEADER SECTION ---
col_logo, col_text = st.columns([1, 4])
with col_logo:
    # Ganti "logo.png" dengan file asli Anda
    # st.image("logo.png", width=80) 
    st.markdown("""<div style="border: 2px solid #000000; width: 75px; height: 75px; display: flex; align-items: center; justify-content: center; color: #000000; font-weight: 900; font-size: 12px; text-align: center; background: #BAE6FD; border-radius: 8px;">LOGO<br>ITDS</div>""", unsafe_allow_html=True)

with col_text:
    st.markdown("<h1 style='margin:0; font-weight: 700; font-size: 28px;'>GATHERING ITDS 2025</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; font-size: 16px; opacity: 0.8;'>Portal Cek Plotting Kelompok & Anggota</p>", unsafe_allow_html=True)

st.write("")

# --- DATA LOADING ---
df = load_data()

if df is not None:
    # Search input ditempatkan di atas
    search_query = st.text_input("", placeholder="🔍 Cari Nama Anda atau Ketik Nomor Kelompok...")
    
    selected_group = None

    if search_query:
        if search_query.isdigit():
            selected_group = int(search_query)
        else:
            match = df[df['NAMA'].str.contains(search_query, case=False, na=False)]
            if not match.empty:
                selected_group = match.iloc[0]['Kelompok']
            else:
                st.error("Data tidak ditemukan. Pastikan ejaan nama benar.")

    # --- TAMPILAN AWAL (KOSONG) ---
    if not search_query:
        st.markdown(f"""
            <div class="welcome-container">
                <h2 style="margin-bottom: 10px;">Selamat Datang! 👋</h2>
                <p style="font-size: 14px; color: #475569 !important;">
                    Silakan masukkan <b>Nama Lengkap</b> atau <b>Nomor Kelompok</b> <br>
                    pada kotak pencarian di atas untuk melihat detail tim Anda.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # --- RESULT SECTION ---
    if selected_group:
        group_df = df[df['Kelompok'] == selected_group]
        
        if not group_df.empty:
            st.markdown(f"<h2 style='margin-top: 20px;'>Kelompok {selected_group}</h2>", unsafe_allow_html=True)
            
            # Info PJ
            pjs = ", ".join(group_df['PJ TIM ACARA'].unique())
            st.markdown(f"""
                <div class="info-box">
                    <div class="label-text">Pendamping / PJ Tim Acara</div>
                    <div class="value-text">{pjs}</div>
                </div>
            """, unsafe_allow_html=True)

            # Statistik
            c1, c2, c3 = st.columns(3)
            l_count = len(group_df[group_df['JK'] == 'L'])
            p_count = len(group_df[group_df['JK'] == 'P'])
            dom_class = group_df['KELAS'].mode()[0]

            with c1:
                st.markdown(f'<div class="info-box"><div class="label-text">Laki-laki</div><div class="value-text">{l_count}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="info-box"><div class="label-text">Perempuan</div><div class="value-text">{p_count}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="info-box"><div class="label-text">Dom. Kelas</div><div class="value-text">{dom_class}</div></div>', unsafe_allow_html=True)

            # Tabel Anggota
            st.markdown("<h4 style='margin-top: 20px; margin-bottom: 10px;'>Daftar Seluruh Kelompok</h4>", unsafe_allow_html=True)
            
            # Styling khusus untuk dataframe agar terlihat menyatu dengan tema biru
            st.dataframe(
                group_df[['NRP', 'NAMA', 'JK', 'KELAS']].reset_index(drop=True), 
                use_container_width=True
            )
        else:
            st.warning("Nomor kelompok tidak terdaftar.")
else:
    st.error("File database tidak ditemukan.")

# Footer
st.markdown("<div style='text-align: center; color: #94A3B8 !important; font-size: 11px; margin-top: 80px;'>DATABASE PLOTTING • DIVISI ACARA ITDS 2025</div>", unsafe_allow_html=True)
