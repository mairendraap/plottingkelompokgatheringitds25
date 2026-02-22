import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman (Clean Mode)
st.set_page_config(
    page_title="Data Plotting ITDS 25",
    layout="centered"
)

# 2. Custom CSS (Minimalist: Putih, Garis Tipis, Biru Netral)
st.markdown("""
    <style>
    /* Reset Background */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Hilangkan Header Streamlit */
    header {visibility: hidden;}

    /* Input Box Minimalis */
    .stTextInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #E2E8F0;
        background-color: #FFFFFF;
        color: #1E293B;
    }

    /* Kotak Informasi (Box Only) */
    .info-box {
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: #FFFFFF;
    }

    .label-text {
        color: #64748B;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .value-text {
        color: #1E293B;
        font-size: 16px;
        font-weight: 600;
    }

    /* Styling Tabel */
    .stDataFrame {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = 'DATA_PLOTTING KELOMPOK_GATHERING ITDS 25_PENS - PLOTTING.csv'
    try:
        # Menyesuaikan pembacaan file berdasarkan struktur CSV Anda
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
    # SLOT UNTUK LOGO: Ganti baris di bawah dengan st.image("logo.png") jika file sudah ada
    st.markdown("""<div style="border: 2px solid #0284C7; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; color: #0284C7; font-weight: bold; font-size: 10px; text-align: center;">LOGO<br>ANGKATAN</div>""", unsafe_allow_html=True)

with col_text:
    st.markdown("<h2 style='margin:0; color: #1E293B;'>Gathering ITDS 2025</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; color: #64748B; font-size: 14px;'>Database Plotting Kelompok</p>", unsafe_allow_html=True)

st.markdown("<hr style='margin: 20px 0; border: 0; border-top: 1px solid #F1F5F9;'>", unsafe_allow_html=True)

# --- SEARCH ---
df = load_data()

if df is not None:
    search_query = st.text_input("Pencarian", placeholder="Ketik Nama Peserta atau Nomor Kelompok...")
    
    selected_group = None

    if search_query:
        if search_query.isdigit():
            selected_group = int(search_query)
        else:
            # Cari nama (case insensitive)
            match = df[df['NAMA'].str.contains(search_query, case=False, na=False)]
            if not match.empty:
                selected_group = match.iloc[0]['Kelompok']
            else:
                st.error("Data tidak ditemukan.")

    # --- RESULT SECTION ---
    if selected_group:
        group_df = df[df['Kelompok'] == selected_group]
        
        if not group_df.empty:
            st.markdown(f"### Kelompok {selected_group}")
            
            # Row 1: PJ
            pjs = ", ".join(group_df['PJ TIM ACARA'].unique())
            st.markdown(f"""
                <div class="info-box">
                    <div class="label-text">PJ Tim Acara</div>
                    <div class="value-text">{pjs}</div>
                </div>
            """, unsafe_allow_html=True)

            # Row 2: Stats (3 Columns)
            c1, c2, c3 = st.columns(3)
            l_count = len(group_df[group_df['JK'] == 'L'])
            p_count = len(group_df[group_df['JK'] == 'P'])
            dom_class = group_df['KELAS'].mode()[0]

            with c1:
                st.markdown(f'<div class="info-box"><div class="label-text">Laki-laki</div><div class="value-text">{l_count}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="info-box"><div class="label-text">Perempuan</div><div class="value-text">{p_count}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="info-box"><div class="label-text">Kelas Dominan</div><div class="value-text">{dom_class}</div></div>', unsafe_allow_html=True)

            # Row 3: Table
            st.markdown("<div style='margin-top: 10px; font-weight: bold; font-size: 14px; color: #64748B;'>DAFTAR ANGGOTA</div>", unsafe_allow_html=True)
            st.dataframe(
                group_df[['NRP', 'NAMA', 'JK', 'KELAS']], 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.warning("Nomor kelompok tidak terdaftar.")
    else:
        st.markdown("<p style='text-align: center; color: #94A3B8; margin-top: 50px;'>Masukkan data pada kolom pencarian untuk melihat detail.</p>", unsafe_allow_html=True)
else:
    st.error("File CSV tidak ditemukan di direktori.")

# Footer
st.markdown("<div style='text-align: center; color: #CBD5E1; font-size: 12px; margin-top: 50px;'>ITDS 25 • PENS</div>", unsafe_allow_html=True)
