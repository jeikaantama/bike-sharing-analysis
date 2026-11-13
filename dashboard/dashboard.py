
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi dashboard
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)


# Styling dashboard
st.markdown("""
    <style>
    /* Background utama */
    [data-testid="stAppViewContainer"] {
        background-color: #F4F7FB !important;
    }

    .stApp {
        background-color: #F4F7FB !important;
        color: #26364A !important;
    }

    /* Warna teks umum */
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stCaptionContainer"],
    label {
        color: #26364A !important;
    }

    /* Judul dan subjudul */
    h1, h2, h3, h4, h5, h6 {
        color: #17365D !important;
        font-weight: 700 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #E8F0FA !important;
    }

    [data-testid="stSidebar"] * {
        color: #26364A !important;
    }

    /* Kartu KPI */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #D5E1EF;
    }

    [data-testid="stMetricLabel"] {
        color: #52657A !important;
    }

    [data-testid="stMetricValue"] {
        color: #17365D !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #26364A !important;
    }

    /* Input dan pilihan filter */
    [data-testid="stSelectbox"],
    [data-testid="stMultiSelect"] {
        color: #26364A !important;
    }

    /* Informasi dan peringatan */
    [data-testid="stAlert"] {
        color: #26364A !important;
    }

    /* Garis pemisah */
    hr {
        border-color: #C8D5E5 !important;
    }

    /* Footer */
    .footer {
        color: #64748B !important;
        text-align: center;
        padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

sns.set_theme(style="whitegrid")


# Membaca dataset
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    day_data = pd.read_csv(BASE_DIR / "day_data.csv")
    hour_data = pd.read_csv(BASE_DIR / "hour_data.csv")

    day_data["dteday"] = pd.to_datetime(day_data["dteday"])
    hour_data["dteday"] = pd.to_datetime(hour_data["dteday"])

    return day_data, hour_data

try:
    day, hour = load_data()
except FileNotFoundError:
    st.error(
        "Dataset tidak ditemukan. Pastikan file day_data.csv "
        "dan hour_data.csv berada di folder dashboard."
    )
    st.stop()

# Persiapan data
weather_labels = {
    1: "Cerah",
    2: "Berawan / Berkabut",
    3: "Hujan Ringan / Salju Ringan",
    4: "Hujan Lebat"
}

day["weather_label"] = day["weathersit"].map(weather_labels)
hour["weather_label"] = hour["weathersit"].map(weather_labels)

day["day_type"] = day["workingday"].map({
    0: "Hari Bukan Kerja",
    1: "Hari Kerja"
})

hour["day_type"] = hour["workingday"].map({
    0: "Hari Bukan Kerja",
    1: "Hari Kerja"
})

# Kategori permintaan berdasarkan kuantil
day["demand_level"] = pd.qcut(
    day["cnt"],
    q=3,
    labels=["Rendah", "Sedang", "Tinggi"]
)

# Sidebar filter
st.sidebar.title("🚲 Bike Sharing")
st.sidebar.caption("Dashboard Analisis Penyewaan Sepeda")
st.sidebar.markdown("---")
st.sidebar.subheader("Filter Data")

year_labels = {
    0: "2011",
    1: "2012"
}

year_options = sorted(day["yr"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Pilih Tahun",
    options=year_options,
    default=year_options,
    format_func=lambda x: year_labels.get(x, str(x))
)

month_options = sorted(day["mnth"].dropna().unique())

selected_months = st.sidebar.multiselect(
    "Pilih Bulan",
    options=month_options,
    default=month_options
)

weather_options = sorted(
    day["weather_label"].dropna().unique()
)

selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=weather_options,
    default=weather_options
)

# Filter dataset
filtered_day = day[
    (day["yr"].isin(selected_years)) &
    (day["mnth"].isin(selected_months)) &
    (day["weather_label"].isin(selected_weather))
].copy()

filtered_hour = hour[
    (hour["yr"].isin(selected_years)) &
    (hour["mnth"].isin(selected_months)) &
    (hour["weather_label"].isin(selected_weather))
].copy()

# Header dashboard
st.title("🚲 Bike Sharing Dashboard")

st.markdown("""
Dashboard ini menyajikan analisis data penyewaan sepeda
Capital Bikeshare di Washington D.C. selama periode 2011–2012.

Analisis mencakup pola penyewaan berdasarkan waktu,
kondisi cuaca, jenis pengguna, dan tingkat permintaan.
""")

st.markdown("---")

# Pemeriksaan hasil filter
if filtered_day.empty or filtered_hour.empty:
    st.warning(
        "Tidak ada data yang sesuai dengan filter yang dipilih. "
        "Silakan ubah pilihan filter."
    )
    st.stop()

# Ringkasan data
st.subheader("Ringkasan Data")

total_rentals = filtered_day["cnt"].sum()
average_rentals = filtered_day["cnt"].mean()
total_casual = filtered_day["casual"].sum()
total_registered = filtered_day["registered"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Penyewaan",
    f"{total_rentals:,.0f}"
)

col2.metric(
    "Rata-rata Penyewaan Harian",
    f"{average_rentals:,.0f}"
)

col3.metric(
    "Casual Users",
    f"{total_casual:,.0f}"
)

col4.metric(
    "Registered Users",
    f"{total_registered:,.0f}"
)

st.markdown("---")

# Analisis penyewaan berdasarkan jam
st.subheader("1. Analisis Penyewaan Berdasarkan Jam")

hourly_avg = (
    filtered_hour.groupby("hr")["cnt"]
    .mean()
    .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(12, 5))

sns.lineplot(
    data=hourly_avg,
    x="hr",
    y="cnt",
    marker="o",
    linewidth=2.5,
    ax=ax1
)

ax1.set_title(
    "Rata-rata Penyewaan Sepeda per Jam",
    fontsize=14,
    pad=15
)
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rata-rata Penyewaan")
ax1.set_xticks(range(24))
ax1.grid(alpha=0.3)

st.pyplot(fig1, use_container_width=True)
plt.close(fig1)

peak_hour = hourly_avg.loc[hourly_avg["cnt"].idxmax()]
lowest_hour = hourly_avg.loc[hourly_avg["cnt"].idxmin()]

st.info(
    f"Jam dengan penyewaan tertinggi adalah "
    f"{int(peak_hour['hr']):02d}:00 dengan rata-rata "
    f"{peak_hour['cnt']:.2f} penyewaan. "
    f"Sedangkan penyewaan terendah terjadi pada "
    f"{int(lowest_hour['hr']):02d}:00 dengan rata-rata "
    f"{lowest_hour['cnt']:.2f} penyewaan."
)

st.markdown("---")

# Analisis penyewaan berdasarkan cuaca
st.subheader("2. Analisis Penyewaan Berdasarkan Cuaca")

weather_avg = (
    filtered_day.groupby("weather_label")["cnt"]
    .mean()
    .reset_index()
    .sort_values("cnt", ascending=False)
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=weather_avg,
    x="weather_label",
    y="cnt",
    ax=ax2
)

ax2.set_title(
    "Rata-rata Penyewaan Berdasarkan Kondisi Cuaca",
    fontsize=14,
    pad=15
)
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan")

plt.xticks(rotation=15)

st.pyplot(fig2, use_container_width=True)
plt.close(fig2)

if not weather_avg.empty:
    best_weather = weather_avg.iloc[0]

    st.info(
        f"Rata-rata penyewaan tertinggi terjadi pada kondisi "
        f"{best_weather['weather_label']}, yaitu "
        f"{best_weather['cnt']:.2f} penyewaan per hari."
    )

st.markdown("---")

# Perbandingan jenis pengguna
st.subheader("3. Perbandingan Jenis Pengguna")

user_comparison = (
    filtered_hour.groupby("day_type")[
        ["casual", "registered"]
    ]
    .mean()
    .reset_index()
)

user_comparison = user_comparison.melt(
    id_vars="day_type",
    value_vars=["casual", "registered"],
    var_name="Jenis Pengguna",
    value_name="Rata-rata Penyewaan"
)

fig3, ax3 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=user_comparison,
    x="day_type",
    y="Rata-rata Penyewaan",
    hue="Jenis Pengguna",
    ax=ax3
)

ax3.set_title(
    "Perbandingan Pengguna pada Hari Kerja dan Bukan Hari Kerja",
    fontsize=14,
    pad=15
)
ax3.set_xlabel("Jenis Hari")
ax3.set_ylabel("Rata-rata Penyewaan per Jam")
ax3.legend(title="Jenis Pengguna")

st.pyplot(fig3, use_container_width=True)
plt.close(fig3)

st.markdown("---")

# Distribusi tingkat permintaan menggunakan pie chart
st.subheader("4. Distribusi Tingkat Permintaan")

demand_distribution = (
    filtered_day["demand_level"]
    .value_counts()
    .reindex(["Rendah", "Sedang", "Tinggi"], fill_value=0)
)

demand_distribution = demand_distribution[
    demand_distribution > 0
]

fig4, ax4 = plt.subplots(figsize=(8, 6))

ax4.pie(
    demand_distribution,
    labels=demand_distribution.index,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.75,
    wedgeprops={
        "edgecolor": "white",
        "linewidth": 2
    },
    textprops={
        "fontsize": 11
    }
)

ax4.set_title(
    "Distribusi Tingkat Permintaan Penyewaan Sepeda",
    fontsize=14,
    pad=20
)

ax4.axis("equal")

st.pyplot(fig4, use_container_width=True)
plt.close(fig4)

st.caption(
    "Tingkat permintaan dibagi menjadi tiga kategori "
    "menggunakan metode quantile binning (qcut)."
)

st.markdown("---")

# Footer
st.markdown("""
    <div style="text-align: center; color: gray; padding: 15px;">
        Bike Sharing Dashboard | Capital Bikeshare Washington D.C.
        <br>
        Dataset periode 2011–2012
    </div>
""", unsafe_allow_html=True)
