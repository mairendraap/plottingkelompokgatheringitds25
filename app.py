import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="Gathering ITDS 2025",
    page_icon="⚡",
    layout="centered" # Menggunakan centered agar UI lebih fokus dan tidak 'lebar' seperti dashboard kaku
)

# 2. Custom CSS untuk UI Simpel & Modern
st.markdown("""
    <style>
    /* Mengubah font global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
    }

    /* Menghilangkan header default streamlit untuk kebersihan */
    header {visibility: hidden;}
    
    /* Style Kartu Nama Kelompok */
    .group-header {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #BAE6FD;
    }

    /* Style Metric/Statistik */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #0284C7;
    }
    
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Tombol & Input */
    .stButton>button {
        border-radius: 8px;
        background-color: #0284C7;
        color: white;
    }

    /* Footer simpel */
    .footer {
        text-align: center;
        color: #94A3B8;
        margin-top: 5rem;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Sesuaikan nama file jika berbeda
    file_path = 'DATA_PLOTTING KELOMPOK_GATHERING ITDS 25_PENS - PLOTTING.csv'
    try:
        df = pd.read_csv(file_path, skiprows=3)
        df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
        df = df.dropna(subset=['Kelompok', 'NAMA'])
        df['Kelompok'] = df['Kelompok'].astype(int)
        return df
    except:
        return None

# --- BAGIAN HEADER & LOGO ---
# Space untuk Logo Angkatan
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Ganti 'logo.png' dengan path file logo Anda nanti
    # st.image("logo_angkatan.png", width=100) 
    st.markdown("""<div style="background: #E2E8F0; width: 80px; height: 80px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #64748B; font-size: 10px; text-align: center;">LOGO<br>DI SINI</div>""", unsafe_allow_html=True)

with col_title:
    st.title("Gathering ITDS 25")
    st.caption("Sistem Pengecekan Plotting Kelompok & Pendamping")

# --- LOGIKA APLIKASI ---
df = load_data()

if df is not None:
    # Search Bar Simpel di Tengah
    search_input = st.text_input("", placeholder="🔍 Ketik Nama atau Nomor Kelompok di sini...")
    
    selected_group = None

    if search_input:
        if search_input.isdigit():
            selected_group = int(search_input)
        else:
            match = df[df['NAMA'].str.contains(search_input, case=False, na=False)]
            if not match.empty:
                selected_group = match.iloc[0]['Kelompok']
            else:
                st.error("Data tidak ditemukan. Coba masukkan nama yang lebih spesifik.")

    if selected_group:
        group_df = df[df['Kelompok'] == selected_group]
        
        if not group_df.empty:
            # Info Utama Kelompok
            st.markdown(f"""
                <div class="group-header">
                    <small style="text-transform: uppercase; letter-spacing: 1px;">Anggota Kelompok</small>
                    <h1 style="margin:0; color: #0369A1;">KELOMPOK {selected_group}</h1>
                </div>
            """, unsafe_allow_html=True)

            # Baris Statistik (Simpel)
            pjs = ", ".join(group_df['PJ TIM ACARA'].unique())
            l_count = len(group_df[group_df['JK'] == 'L'])
            p_count = len(group_df[group_df['JK'] == 'P'])
            dom_class = group_df['KELAS'].mode()[0]

            c1, c2, c3 = st.columns(3)
            c1.metric("Total", f"{len(group_df)} Org")
            c2.metric("Laki-Laki", l_count)
            c3.metric("Perempuan", p_count)

            # Box PJ & Dominasi
            st.markdown(f"""
                <div style="background: white; padding: 1.2rem; border-radius: 12px; border: 1px solid #E2E8F0; margin-top: 1rem;">
                    <p style="margin: 0; color: #64748B; font-size: 0.9rem;"><b>PJ Tim Acara:</b> {pjs}</p>
                    <p style="margin: 0; color: #64748B; font-size: 0.9rem;"><b>Dominasi Kelas:</b> {dom_class}</p>
                </div>
            """, unsafe_allow_html=True)

            # Tabel Anggota
            st.write("---")
            st.dataframe(
                group_df[['NRP', 'NAMA', 'JK', 'KELAS']], 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.warning("Nomor kelompok tidak valid.")
    else:
        # Tampilan Awal (Kosong)
        st.info("Silakan masukkan nama peserta atau nomor kelompok pada kolom pencarian di atas.")

else:
    st.error("File database tidak ditemukan. Pastikan file CSV ada di folder yang sama.")

st.markdown('<div class="footer">Made for ITDS 2025 • PENS</div>', unsafe_allow_html=True)
