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
    Insight: Dari distribusi data, dapat dilihat bahwa beberapa variabel, seperti suhu (temp) dan kelembaban (hum), memiliki distribusi yang cukup normal. 
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
    Insight: Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan akhir pekan, yang menunjukkan bahwa sepeda lebih sering digunakan sebagai sarana transportasi untuk bekerja atau sekolah daripada untuk kegiatan rekreasi.
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
    Insight: Semakin tinggi kelembaban, jumlah penggunaan sepeda cenderung menurun. Hal ini mungkin disebabkan karena tingkat kelembaban tinggi membuat kondisi bersepeda menjadi kurang nyaman.
    """)

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
    Insight: Tren penggunaan sepeda menunjukkan peningkatan selama musim panas dan penurunan selama musim dingin. Tren ini menunjukkan bahwa pengguna lebih aktif menggunakan sepeda saat cuaca mendukung.
    """)
# RFM Analysis
elif option == "RFM Analysis":
    st.subheader("RFM Analysis")

    # Menghitung recency
    data_terbaru = data_hari['dteday'].max()  # Mengambil data terbaru (terbesar) dari kolom dteday
    data_hari['Recency'] = (data_terbaru - data_hari['dteday']).dt.days  # Menghitung selisih antara tanggal terbaru dan setiap tanggal dalam dteday

    # Menghitung frequency
    frekuensi = data_hari.groupby('instant').size().reset_index(name='Frequency')  # Menghitung jumlah peminjaman sepeda per hari

    # Menghitung total peminjaman (monetary)
    monetary = data_hari.groupby('instant')['cnt'].sum().reset_index(name='Monetary')

    # Menggabungkan recency, frequency, dan monetary
    rfm = pd.merge(frekuensi, monetary, on='instant')
    rfm = pd.merge(rfm, data_hari[['instant', 'Recency']].drop_duplicates(), on='instant')

    # Menampilkan RFM
    st.write(rfm.head())

    # Memvisualisasikan RFM
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))  # membuat subplot

    # Plot Recency
    sns.barplot(y="Recency", x="instant", data=rfm.sort_values(by="Recency", ascending=True).head(5), ax=ax[0])
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis='x', labelsize=15)

   # Plot Frequency
    sns.barplot(y="Frequency", x="instant", data=rfm.sort_values(by="Frequency", ascending=False).head(5), ax=ax[1])
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)

    # Plot Monetary
    sns.barplot(y="Monetary", x="instant", data=rfm.sort_values(by="Monetary", ascending=False).head(5), ax=ax[2])
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)

    # Atur suptitle
    plt.suptitle("Pengguna Terbaik Berdasarkan RFM Parameters (instant)", fontsize=20)
    st.pyplot(fig)

# Kesimpulan
st.markdown("""
## Kesimpulan:
1. **Penggunaan Sepeda pada Hari Kerja dan Akhir Pekan**: Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan akhir pekan.
2. **Pengaruh Cuaca**: Cuaca cerah dan suhu yang lebih nyaman mendorong lebih banyak penggunaan sepeda. Cuaca buruk, kelembaban tinggi, dan kecepatan angin tinggi cenderung mengurangi penggunaan.
3. **Tren Penggunaan dari Waktu ke Waktu**: Penggunaan sepeda bervariasi sepanjang waktu, meningkat pada bulan-bulan musim panas dan menurun selama musim dingin.
4. **RFM Analysis**: Dari analisis RFM, kita dapat mengidentifikasi pengguna yang paling sering menggunakan sepeda, yang paling baru menggunakan sepeda, serta yang menyumbang jumlah pemakaian tertinggi.
""")

