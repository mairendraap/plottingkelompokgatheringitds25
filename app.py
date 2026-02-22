import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Gathering ITDS 25",
    page_icon="💙",
    layout="centered"
)

# 2. Custom CSS (Fokus pada White Space & Warna Biru Pastel)
st.markdown("""
    <style>
    /* Import Font Modern */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #FFFFFF;
    }

    /* Hilangkan Header Streamlit */
    header {visibility: hidden;}

    /* Input Box Styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 10px 15px;
        background-color: #F8FAFC;
    }

    /* Card Styling */
    .info-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 10px 25px rgba(0, 104, 255, 0.05);
        margin-bottom: 20px;
    }

    .status-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #CBD5E1;
        margin-top: 40px;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = 'DATA_PLOTTING KELOMPOK_GATHERING ITDS 25_PENS - PLOTTING.csv'
    try:
        df = pd.read_csv(file_path, skiprows=3)
        df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
        df = df.dropna(subset=['Kelompok', 'NAMA'])
        df['Kelompok'] = df['Kelompok'].astype(int)
        return df
    except:
        return None

# --- UI HEADER ---
# Space untuk Logo Angkatan
col_a, col_b = st.columns([1, 5])
with col_a:
    # Jika file logo ada, pakai: st.image("logo.png")
    st.markdown("""<div style="width: 70px; height: 70px; background: #0068FF; border-radius: 18px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 10px; text-align: center;">LOGO<br>ITDS</div>""", unsafe_allow_html=True)

with col_b:
    st.markdown("<h2 style='margin:0; color: #1E293B;'>Gathering ITDS 2025</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; color: #64748B;'>Cek Kelompok & PJ Pendamping</p>", unsafe_allow_html=True)

st.write("")

# --- SEARCH ENGINE ---
df = load_data()

if df is not None:
    search_query = st.text_input("", placeholder="Masukkan Nama atau Nomor Kelompok...")
    
    selected_group = None

    if search_query:
        if search_query.isdigit():
            selected_group = int(search_query)
        else:
            match = df[df['NAMA'].str.contains(search_query, case=False, na=False)]
            if not match.empty:
                selected_group = match.iloc[0]['Kelompok']
            else:
                st.error("Data tidak ditemukan.")

    if selected_group:
        group_df = df[df['Kelompok'] == selected_group]
        
        if not group_df.empty:
            # Header Kelompok
            st.markdown(f"""
                <div style="margin-top: 20px;">
                    <span style="background: #E0F2FE; color: #0068FF;" class="status-badge">AKTIF</span>
                    <h1 style="margin:0; color: #1E293B;">Kelompok {selected_group}</h1>
                </div>
            """, unsafe_allow_html=True)

            # Informasi PJ
            pjs = ", ".join(group_df['PJ TIM ACARA'].unique())
            st.markdown(f"""
                <div class="info-card">
                    <p style="margin:0; color: #64748B; font-size: 13px;">PJ Tim Acara</p>
                    <p style="margin:0; color: #1E293B; font-weight: 600; font-size: 18px;">{pjs}</p>
                </div>
            """, unsafe_allow_html=True)

            # Quick Stats
            c1, c2, c3 = st.columns(3)
            l_count = len(group_df[group_df['JK'] == 'L'])
            p_count = len(group_df[group_df['JK'] == 'P'])
            dom_class = group_df['KELAS'].mode()[0]

            with c1:
                st.markdown(f"<div class='info-card'><small>♂️ Laki-laki</small><br><b>{l_count}</b></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='info-card'><small>♀️ Perempuan</small><br><b>{p_count}</b></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='info-card'><small>🏫 Dominasi</small><br><b>{dom_class}</b></div>", unsafe_allow_html=True)

            # Tabel Daftar Anggota
            st.markdown("<p style='color: #64748B; font-weight: 600; margin-top: 10px;'>Daftar Anggota</p>", unsafe_allow_html=True)
            st.dataframe(
                group_df[['NRP', 'NAMA', 'KELAS']], 
                use_container_width=True, 
                hide_index=True
            )
    else:
        # Default State
        st.markdown("""
            <div style="text-align: center; padding: 50px; color: #94A3B8;">
                <p>Silakan cari nama untuk melihat detail kelompok.</p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error("File tidak ditemukan.")

st.markdown('<div class="footer">ITDS 2025 • Politeknik Elektronika Negeri Surabaya</div>', unsafe_allow_html=True)
