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

    st.write("""
    Insight: min cnt (total pengguna sepeda) sebanyak 22, dan maks cnt sebanyak 8714, dengan mean 4504.348837. Dapat dilihat bahwa faktor dari cuaca seperti temp dan atemp memiliki korelasi yang cukup kuat dengan cnt (total penggunaan sepeda), sedangkan faktor hum dan windspeed memiliki korelasi yang lemah dengan cnt.
    Dari distribusi data, dapat dilihat bahwa beberapa variabel, seperti suhu (temp) dan kelembaban (hum), memiliki distribusi yang cukup normal. 
    Sedangkan untuk jumlah penggunaan sepeda (cnt), terlihat ada perbedaan distribusi yang menggambarkan variasi pemakaian selama periode tertentu.
    """)

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

    st.write("""
    Insight: Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan akhir pekan.
    """)

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

    st.write("""
    Insight: Kondisi cuaca sangat mempengaruhi penggunaan sepeda. Penggunaan sepeda tertinggi terjadi saat cuaca cerah, sedangkan penggunaan menurun saat kondisi mendung atau hujan.
    """)

    st.subheader("Hubungan Suhu, Kelembaban, dan Kecepatan Angin terhadap Penggunaan Sepeda")
    # Scatterplot hubungan suhu dan penggunaan sepeda
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='temp', y='cnt', data=data_hari, alpha=0.6, ax=ax)
    ax.set_title('Hubungan antara Suhu dan Penggunaan Sepeda')
    ax.set_xlabel('Suhu (normalisasi)')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

    st.write("""
    Insight: Terdapat korelasi positif antara suhu dan jumlah penggunaan sepeda, yang berarti penggunaan sepeda cenderung meningkat pada suhu yang lebih hangat.
    """)

    # Scatterplot hubungan kelembaban dan penggunaan sepeda
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='hum', y='cnt', data=data_hari, alpha=0.6, color='red', ax=ax)
    ax.set_title('Hubungan antara Kelembaban dan Penggunaan Sepeda')
    ax.set_xlabel('Kelembaban')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

    st.write("""
    Insight: Semakin tinggi kelembaban, jumlah penggunaan sepeda cenderung menurun. 

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

    st.write("""
    Insight: Penggunaan sepeda paling tinggi terjadi pada musim gugur dan musim panas, sedangkan pada musim dingin, penggunaan sepeda turun drastis karena cuaca dingin yang tidak terlalu mendukung untuk bersepeda.
    """)

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

    st.write("""
    Insight: Tren penggunaan sepeda meningkat dari bulan Januari hingga Juli 2011, kemudian terjadi penurunan pada bulan Oktober 2011 hingga Januari 2012, namun meningkat cukup signifikan pada Januari hingga April 2012, dan cukup konstan pada April hingga Oktober 2012, lalu terjadi penurunan di awal tahun 2013.
    """)

# Add conclusions
st.markdown("""
## Kesimpulan:
1. **Penggunaan Sepeda pada Hari Kerja dan Akhir Pekan**: Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan akhir pekan.
2. **Pengaruh Cuaca**: Cuaca cerah dan suhu yang lebih nyaman mendorong lebih banyak penggunaan sepeda. Cuaca buruk, kelembaban tinggi, dan kecepatan angin tinggi cenderung mengurangi penggunaan.
3. **Tren Penggunaan dari Waktu ke Waktu**: Penggunaan sepeda bervariasi sepanjang waktu, meningkat pada bulan-bulan musim panas dan menurun selama musim dingin.
""")
