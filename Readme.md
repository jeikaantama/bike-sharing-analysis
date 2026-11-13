# Bike Sharing Data Analysis

## Deskripsi Proyek

Proyek ini merupakan analisis data penyewaan sepeda menggunakan Bike Sharing Dataset dari Capital Bikeshare di Washington D.C. selama periode 2011–2012.

Analisis dilakukan untuk memahami pola penyewaan sepeda berdasarkan waktu, kondisi cuaca, jenis pengguna, dan tingkat permintaan. Hasil analisis juga disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Business Questions

Beberapa pertanyaan bisnis yang menjadi fokus dalam proyek ini adalah:

1. Pada jam berapa rata-rata penyewaan sepeda mencapai jumlah tertinggi dan terendah?
2. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca?
3. Bagaimana perbandingan jumlah penyewaan oleh pengguna casual dan registered pada hari kerja dan bukan hari kerja?
4. Bagaimana distribusi tingkat permintaan penyewaan sepeda berdasarkan kategori rendah, sedang, dan tinggi?

## Struktur Folder

```text
Submission/
├── dashboard/
│   ├── dashboard.py
│   ├── day_data.csv
│   └── hour_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
└── requirements.txt
```

## Dataset

Dataset yang digunakan adalah Bike Sharing Dataset yang terdiri dari:

- `day.csv`: Data penyewaan sepeda berdasarkan hari.
- `hour.csv`: Data penyewaan sepeda berdasarkan jam.

Dataset asli disimpan dalam folder `data/`, sedangkan dataset yang telah melalui proses data cleaning disimpan dalam folder `dashboard/` untuk digunakan pada dashboard.

## Proses Analisis

Tahapan yang dilakukan dalam proyek ini meliputi:

1. **Data Gathering**: Mengumpulkan Bike Sharing Dataset.
2. **Data Assessing**: Memeriksa struktur data, tipe data, missing values, dan duplikasi.
3. **Data Cleaning**: Melakukan pembersihan data agar siap digunakan dalam proses analisis.
4. **Exploratory Data Analysis (EDA)**: Menganalisis pola penyewaan berdasarkan business questions.
5. **Data Visualization**: Menyajikan hasil analisis melalui visualisasi.
6. **Dashboard Development**: Membuat dashboard interaktif menggunakan Streamlit.

## Teknologi yang Digunakan

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Google Colab
- Visual Studio Code

## Instalasi Library

Pastikan Python telah terinstal. Buka terminal pada folder utama proyek, kemudian jalankan perintah:

```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

Setelah seluruh library berhasil diinstal, jalankan dashboard menggunakan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis melalui browser. Jika tidak terbuka, akses alamat berikut:

```text
http://localhost:8501
```

## File Proyek

- `notebook.ipynb`: Berisi proses pengumpulan, penilaian, pembersihan, analisis, dan visualisasi data.
- `dashboard/dashboard.py`: Source code dashboard interaktif.
- `requirements.txt`: Daftar library Python yang dibutuhkan untuk menjalankan proyek.
