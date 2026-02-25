import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(
    page_title="KLIK 25 - PLOTTING KELOMPOK",
    page_icon="💙",
    layout="centered"
)

# File assets (Pastikan file ini ada di folder yang sama agar tidak error)
background_image_file = "BGKLIK25.jpg"  
logo_path = "logoklik.png"             

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Pengaturan Background
if os.path.exists(background_image_file):
    bg_base64 = get_base64_of_bin_file(background_image_file)
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
else:
    bg_css = "<style>.stApp { background-color: #FFFFFF; }</style>"

st.markdown(bg_css, unsafe_allow_html=True)

# Styling CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.95); 
        padding: 40px !important;
        border-radius: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    header {visibility: hidden;}

    h1, h2, h3, h4, p, span, div, label, .stMarkdown {
        color: #000000 !important;
    }

    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #000000;
        background-color: #FFFFFF;
        color: #000000 !important;
        padding: 12px;
    }

    .info-box {
        border: 1px solid #E2E8F0;
        border-left: 5px solid #BAE6FD;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: #FFFFFF; 
    }

    .label-text {
        color: #475569 !important;
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

    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        border: 1px dashed #BAE6FD;
        border-radius: 20px;
        background-color: rgba(240, 249, 255, 0.8);
        margin-top: 20px;
    }

    .stDataFrame {
        border: 1px solid #BAE6FD;
        border-radius: 8px;
        background-color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Menyesuaikan dengan nama file hasil plotting yang sudah dibuat
    file_path = 'HASIL_PLOT_KELOMPOK_GATHERING.csv'
    try:
        # Load data tanpa skip baris karena file sudah memiliki header
        df = pd.read_csv(file_path)
        
        # Pastikan kolom 'Kelompok' dalam bentuk integer
        df['Kelompok'] = df['Kelompok'].astype(int)
        
        return df
    except Exception as e:
        st.error(f"Gagal membaca database: {e}")
        return None

# Header Section
col_logo, col_text = st.columns([1, 4])
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)
    else:
        st.markdown("""<div style="border: 2px solid #000000; width: 75px; height: 75px; display: flex; align-items: center; justify-content: center; color: #000000; font-weight: 900; font-size: 12px; text-align: center; background: #BAE6FD; border-radius: 8px;">LOGO<br>ITDS</div>""", unsafe_allow_html=True)

with col_text:
    st.markdown("<h1 style='margin:0; font-weight: 700; font-size: 28px;'>GATHERING ITDS 2025</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; font-size: 16px; opacity: 0.8;'>Portal Cek Plotting Kelompok & Anggota Gathering Klik 25</p>", unsafe_allow_html=True)

st.write("")

df = load_data()

if df is not None:
    search_query = st.text_input("", placeholder="🔍 Cari Nama Lengkap atau Nomor Kelompok...")
    
    selected_group = None

    if search_query:
        if search_query.isdigit():
            selected_group = int(search_query)
        else:
            # Menggunakan kolom 'Nama' (sesuai CSV)
            match = df[df['Nama'].str.contains(search_query, case=False, na=False)]
            if not match.empty:
                selected_group = match.iloc[0]['Kelompok']
            else:
                st.error("Nama tidak ditemukan. Gunakan nama lengkap atau cek ejaan kembali.")

    if not search_query:
        st.markdown(f"""
            <div class="welcome-container">
                <h2 style="margin-bottom: 10px;">Selamat Datang! 👋</h2>
                <p style="font-size: 14px; color: #475569 !important;">
                    Silakan masukkan <b>Nama Lengkap</b> atau <b>Nomor Kelompok</b> <br>
                    pada kotak pencarian di atas untuk melihat detail plotting Kamu!.
                </p>
            </div>
        """, unsafe_allow_html=True)

    if selected_group:
        group_df = df[df['Kelompok'] == selected_group]
        
        if not group_df.empty:
            st.markdown(f"<h2 style='margin-top: 20px;'>Kartu Kelompok {selected_group}</h2>", unsafe_allow_html=True)
            
            # Kolom 'PJ Tim Acara' sesuai CSV
            pjs = ", ".join(group_df['PJ Tim Acara'].unique())
            st.markdown(f"""
                <div class="info-box">
                    <div class="label-text">Pendamping / PJ Tim Acara</div>
                    <div class="value-text">{pjs}</div>
                </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            # Kolom 'Jenis Kelamin' dan 'Kelas' sesuai CSV
            l_count = len(group_df[group_df['Jenis Kelamin'] == 'L'])
            p_count = len(group_df[group_df['Jenis Kelamin'] == 'P'])
            mode_kelas = group_df['Kelas'].mode()
            dom_class = mode_kelas[0] if not mode_kelas.empty else "-"

            with c1:
                st.markdown(f'<div class="info-box"><div class="label-text">Laki-laki</div><div class="value-text">{l_count}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="info-box"><div class="label-text">Perempuan</div><div class="value-text">{p_count}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="info-box"><div class="label-text">Dominasi Kelas</div><div class="value-text">{dom_class}</div></div>', unsafe_allow_html=True)

            st.markdown("<h4 style='margin-top: 20px; margin-bottom: 10px;'>Daftar Anggota Kelompok</h4>", unsafe_allow_html=True)
            
            # Menampilkan kolom yang ada di CSV
            st.dataframe(
                group_df[['NRP', 'Nama', 'Jenis Kelamin', 'Kelas']].reset_index(drop=True), 
                use_container_width=True
            )
        else:
            st.warning(f"Kelompok {selected_group} tidak ditemukan.")

st.markdown("<div style='text-align: center; color: #94A3B8 !important; font-size: 11px; margin-top: 80px;'>KLIK 25 • PANITIA GATHERING ITDS 2025</div>", unsafe_allow_html=True)
