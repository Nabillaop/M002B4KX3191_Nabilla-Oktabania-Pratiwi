# Import packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul dan deskripsi data
st.title("Data Analysis: Bike Sharing (Day)")
st.markdown("""
Aplikasi ini menganalisis penggunaan sepeda dari data Bike Sharing. 
""")

# dataset yang digunakan
data_url = 'https://raw.githubusercontent.com/Nabillaop/M002B4KX3191_Nabilla-Oktabania-Pratiwi/refs/heads/main/day.csv'
data_hari = pd.read_csv(data_url)

# Data Wrangling
data_hari['dteday'] = pd.to_datetime(data_hari['dteday'])  # Convert 'dteday' to datetime

# Pilihan pada sidebar
st.sidebar.header("Filter Data")
option = st.sidebar.selectbox(
    "Pilih Analisis:",
    ("Data Summary", "Working Day vs Holiday", "Cuaca dan Penggunaan Sepeda", "Musim dan Penggunaan Sepeda", "Tren Penggunaan Sepeda dari Waktu ke Waktu")
)

# Data Summary  (Statistika deskriptif)
if option == "Data Summary":
    st.subheader("Summary Data")
    st.write(data_hari.describe())
    st.write("Tidak ada data yang hilang atau duplikat dalam dataset.")

    st.subheader("Distribusi Data")
    fig, ax = plt.subplots(figsize=(17, 12))
    data_hari.hist(ax=ax)
    st.pyplot(fig)

# Analysis: Working Day vs Holiday
elif option == "Working Day vs Holiday":
    st.subheader("Total Penggunaan Sepeda Berdasarkan Hari Kerja dan Akhir Pekan")
    cnt_workingday = data_hari.groupby('workingday')['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='workingday', y='cnt', data=cnt_workingday, ax=ax)
    ax.set_title('Total Penggunaan Sepeda Berdasarkan Hari')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    ax.set_xticklabels(['Akhir Pekan', 'Hari Kerja'])
    st.pyplot(fig)

# Analysis: Cuaca dan Penggunaan Sepeda
elif option == "Cuaca dan Penggunaan Sepeda":
    st.subheader("Pengaruh Cuaca terhadap Penggunaan Sepeda")

    # Total penggunaan sepeda berdasarkan kondisi cuaca
    cnt_cuaca = data_hari.groupby('weathersit')['cnt'].sum().reset_index()
    cuaca_mapping = {1: 'Cuaca Cerah', 2: 'Cuaca Mendung', 3: 'Hujan'}
    cnt_cuaca['weathersit'] = cnt_cuaca['weathersit'].map(cuaca_mapping)

    # Visualisasi penggunaan sepeda berdasarkan cuaca
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit', y='cnt', data=cnt_cuaca, ax=ax)
    ax.set_title('Total Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Total Penggunaan Sepeda')
    st.pyplot(fig)

    st.subheader("Hubungan Suhu, Kelembaban, dan Kecepatan Angin terhadap Penggunaan Sepeda")
    # Scatterplot hubungan suhu dan penggunaan sepeda
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='temp', y='cnt', data=data_hari, alpha=0.6, ax=ax)
    ax.set_title('Hubungan antara Suhu dan Penggunaan Sepeda')
    ax.set_xlabel('Suhu (normalisasi)')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

    # Scatterplot hubungan kelembaban dan penggunaan sepeda
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='hum', y='cnt', data=data_hari, alpha=0.6, color='red', ax=ax)
    ax.set_title('Hubungan antara Kelembaban dan Penggunaan Sepeda')
    ax.set_xlabel('Kelembaban')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

# Analysis: Musim dan Penggunaan Sepeda
elif option == "Musim dan Penggunaan Sepeda":
    st.subheader("Total Penggunaan Sepeda Berdasarkan Musim")
    cnt_season = data_hari.groupby('season')['cnt'].sum().reset_index()
    cnt_season['season'] = cnt_season['season'].map({
        1: 'Musim Semi',
        2: 'Musim Panas',
        3: 'Musim Gugur',
        4: 'Musim Dingin'
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season', y='cnt', data=cnt_season, color='purple', ax=ax)
    ax.set_title('Total Penggunaan Sepeda Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Penggunaan Sepeda')
    st.pyplot(fig)

# Analysis: Tren Penggunaan Sepeda dari Waktu ke Waktu
elif option == "Tren Penggunaan Sepeda dari Waktu ke Waktu":
    st.subheader("Tren Penggunaan Sepeda dari Waktu ke Waktu")
    tren = data_hari.groupby('dteday')['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(tren['dteday'], tren['cnt'], color='orange')
    ax.set_title('Tren Penggunaan Sepeda dari Waktu ke Waktu')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Add conclusions
st.markdown("""
## Kesimpulan:
1. **Penggunaan Sepeda pada Hari Kerja dan Akhir Pekan**: Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan akhir pekan.
2. **Pengaruh Cuaca dan Suhu**: Cuaca dan suhu memberikan pengaruh yang cukup signifikan pada permintaan penggunaan sepeda. Semakin cerah cuaca dan semakin normal suhu, permintaan pengguanaan sepeda semakin banyak. Kelembaban dan kecepatan angin tidak memberikan pengaruh yang signifikan pada permintaan penggunaan sepeda.
3. **Tren Penggunaan dari Waktu ke Waktu**: Tren permintaan penggunaan sepeda dari waktu ke waktu tidak selalu konstan, ada waktu dimana permintaan meningkat ataupun sebaliknya. Permintaan di akhir tahun cenderung menurun dan kembali meningkat ketika awal tahun.
""")
