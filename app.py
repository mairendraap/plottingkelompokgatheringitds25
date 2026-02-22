import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Gathering ITDS 25 - Plotting", layout="wide")

# Custom CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stDataFrame { border-radius: 10px; }
    h1 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Pastikan file CSV berada di folder yang sama
    file_path = 'DATA_PLOTTING KELOMPOK_GATHERING ITDS 25_PENS - PLOTTING.csv'
    df = pd.read_csv(file_path, skiprows=3)
    df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
    df = df.dropna(subset=['Kelompok', 'NAMA'])
    df['Kelompok'] = df['Kelompok'].astype(int)
    return df

try:
    df = load_data()

    st.title("🔎 Plotting Kelompok Gathering ITDS 25")
    st.markdown("Cari detail kelompok berdasarkan **Nama Peserta** atau **Nomor Kelompok**.")

    # Sidebar untuk Pencarian
    st.sidebar.header("Fitur Pencarian")
    search_type = st.sidebar.radio("Cari berdasarkan:", ["Nomor Kelompok", "Nama Peserta"])

    selected_group = None

    if search_type == "Nomor Kelompok":
        list_kelompok = sorted(df['Kelompok'].unique())
        selected_group = st.sidebar.selectbox("Pilih Nomor Kelompok:", list_kelompok)
    else:
        search_name = st.sidebar.text_input("Masukkan Nama Peserta:")
        if search_name:
            match = df[df['NAMA'].str.contains(search_name, case=False, na=False)]
            if not match.empty:
                selected_group = match.iloc[0]['Kelompok']
                st.sidebar.success(f"Ditemukan di Kelompok {selected_group}")
            else:
                st.sidebar.error("Nama tidak ditemukan.")

    if selected_group:
        group_df = df[df['Kelompok'] == selected_group]
        
        # Kalkulasi Data
        pjs = ", ".join(group_df['PJ TIM ACARA'].unique())
        l_count = len(group_df[group_df['JK'] == 'L'])
        p_count = len(group_df[group_df['JK'] == 'P'])
        dom_class = group_df['KELAS'].mode()[0]

        # Row 1: Dashboard Stats
        st.subheader(f"📊 Ringkasan Kelompok {selected_group}")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total Anggota", len(group_df))
        col2.metric("Laki-laki (L)", l_count)
        col3.metric("Perempuan (P)", p_count)
        col4.metric("Dominasi Kelas", dom_class)

        # Row 2: PJ & Detail
        st.info(f"**PJ Tim Acara:** {pjs}")

        # Row 3: Tabel Anggota
        st.subheader("📋 Daftar Anggota")
        # Styling dataframe agar JK berwarna atau lebih rapi
        st.dataframe(group_df[['NRP', 'NAMA', 'JK', 'KELAS']], use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan file CSV sudah benar. Error: {e}")
