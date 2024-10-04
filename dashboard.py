# Import semua package yang digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='dark')

# Memuat data yang akan digunakan
@st.cache_data
def load_data():
    data = 'https://raw.githubusercontent.com/Nabillaop/M002B4KX3191_Nabilla-Oktabania-Pratiwi/refs/heads/main/day.csv'
    data_hari = pd.read_csv(data)
    return data_hari

data_hari = load_data()

# Judul dashboard
st.title("Dashboard Analisis Penggunaan Sepeda")

# Deskripsi data
st.write("Dataset ini memuat informasi harian penggunaan sepeda dari sistem Bike Sharing.")

# Mengonversi kolom 'dteday' menjadi tipe datetime
data_hari['dteday'] = pd.to_datetime(data_hari['dteday'])

# Pilihan Menu Sidebar
st.sidebar.title("Opsi Analisis")
menu = st.sidebar.selectbox("Pilih visualisasi:", 
                            ["Jumlah Penggunaan Sepeda per Hari dalam Seminggu",
                            "Total Penggunaan Sepeda Berdasarkan Kondisi Cuaca", 
                             "Jumlah Penggunaan Sepeda Berdasarkan Musim", 
                             "Tren Penggunaan Sepeda dari Waktu ke Waktu"])

# Visualisasi Berdasarkan Pilihan
if menu == "Jumlah Penggunaan Sepeda per Hari dalam Seminggu":
    # Menambahkan kolom baru 'day_of_week' untuk mendapatkan hari dalam seminggu
    data_hari['day_of_week'] = data_hari['dteday'].dt.day_name()  # Menggunakan nama hari dalam bahasa Inggris

    # Mengelompokkan data berdasarkan hari dalam seminggu
    cnt_day= data_hari.groupby('day_of_week')['cnt'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()

    # Membuat bar chart
    st.header("Jumlah Penggunaan Sepeda per Hari dalam Seminggu")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='day_of_week', y='cnt', data=cnt_day, palette='viridis', ax=ax)
    ax.set_title('Total Penggunaan Sepeda Berdasarkan Hari dalam Seminggu')
    ax.set_xlabel('Hari dalam Seminggu')
    ax.set_ylabel('Total Jumlah Penggunaan Sepeda')
    ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'], rotation=45)
    st.pyplot(fig)

elif menu == "Total Penggunaan Sepeda Berdasarkan Kondisi Cuaca":
    cnt_cuaca = data_hari.groupby('weathersit')['cnt'].sum().reindex([0, 1, 2, 3]).reset_index()
    # Mapping kondisi cuaca menjadi nama dalam bahasa Indonesia
    cuaca_mapping = {
        1: 'Cuaca Cerah',
        2: 'Cuaca Mendung',
        3: 'Hujan',
    }

    #  Mengganti nilai numerik cuaca dengan nama cuaca
    cnt_cuaca['weathersit'] = cnt_cuaca['weathersit'].map(cuaca_mapping)

    # Membuat bar chart
    st.header("Total Penggunaan Sepeda Berdasarkan Kondisi Cuaca")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit', y='cnt', data=cnt_cuaca, palette='viridis', ax=ax)
    ax.set_title('Total Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

elif menu == "Jumlah Penggunaan Sepeda Berdasarkan Musim":
    # Mengelompokkan data berdasarkan musim
    cnt_season = data_hari.groupby('season')['cnt'].sum().reset_index()

    # Indeks musim
    musim_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    cnt_season['season'] = cnt_season['season'].map(musim_mapping)

    # Membuat bar chart
    st.header("Jumlah Penggunaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', data=cnt_season, palette='viridis', ax=ax)
    ax.set_title('Total Penggunaan Sepeda Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

elif menu == "Tren Penggunaan Sepeda dari Waktu ke Waktu":
    # Mengelompokkan data berdasarkan tanggal
    tren = data_hari.groupby('dteday')['cnt'].sum().reset_index()

    # Membuat line chart untuk tren penggunaan sepeda dari waktu ke waktu
    st.header("Tren Penggunaan Sepeda dari Waktu ke Waktu")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(tren['dteday'], tren['cnt'], color='orange')
    ax.set_title('Tren Penggunaan Sepeda dari Waktu ke Waktu')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Penjelasan lebih lanjut tentang dataset
st.sidebar.subheader("Tentang Dataset")
st.sidebar.write("Dataset ini mengandung data harian penggunaan sepeda dari sistem bike sharing, mencakup informasi cuaca, musim, hari kerja, dan lainnya. Data ini dapat digunakan untuk analisis tren penggunaan sepeda, hubungan antara kondisi cuaca dan penggunaan, dan perencanaan strategi bisnis untuk sistem berbagi sepeda.")

#streamlit run c:/Users/win 10/Downloads/dashboard.py