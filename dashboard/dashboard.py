
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide"
)


# Konfigurasi warna
WARNA_UTAMA = "#238477"
WARNA_HIGHLIGHT = "#E59A45"

tema_grafik = (
    "plotly_dark"
    if st.context.theme == "dark"
    else "plotly_white"
)


# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }

    /* Header Dashboard */
    .header-card {
        background: rgba(35, 132, 119, 0.10);
        border: 1px solid rgba(35, 132, 119, 0.35);
        border-left: 6px solid #238477;
        border-radius: 16px;
        padding: 25px 28px;
        margin-bottom: 20px;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: var(--text-color);
        margin-bottom: 8px;
    }

    .subtitle {
        font-size: 15px;
        color: var(--text-color);
        opacity: 0.75;
        margin-bottom: 0;
    }

    /* Judul Bagian */
    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: var(--text-color);
        border-left: 4px solid #238477;
        padding-left: 12px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        min-height: 115px;
        transition: 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #238477;
        transform: translateY(-3px);
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricDelta"] {
        color: var(--text-color);
    }

    /* Grafik Cards */
    div[data-testid="stPlotlyChart"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    /* Insight Cards */
    .insight-box {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-left: 5px solid #238477;
        padding: 18px 20px;
        border-radius: 12px;
        color: var(--text-color);
        margin-bottom: 10px;
        line-height: 1.7;
        min-height: 145px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: var(--text-color);
        opacity: 0.65;
        font-size: 13px;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)


# Memuat dataset
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    data = pd.read_csv(BASE_DIR / "main_data.csv")
    data["dteday"] = pd.to_datetime(data["dteday"])
    return data

df = load_data()


# Sidebar
st.sidebar.markdown("## 🚲 Bike Sharing")
st.sidebar.caption("Analytics Dashboard")
st.sidebar.divider()

st.sidebar.subheader("Filter Data")

tanggal_min = df["dteday"].min().date()
tanggal_max = df["dteday"].max().date()

rentang_tanggal = st.sidebar.date_input(
    "Pilih rentang tanggal",
    value=(tanggal_min, tanggal_max),
    min_value=tanggal_min,
    max_value=tanggal_max
)

if isinstance(rentang_tanggal, (tuple, list)) and len(rentang_tanggal) == 2:
    tanggal_awal, tanggal_akhir = rentang_tanggal

    data_filter = df[
        (df["dteday"].dt.date >= tanggal_awal) &
        (df["dteday"].dt.date <= tanggal_akhir)
    ].copy()
else:
    data_filter = df.copy()

st.sidebar.divider()

st.sidebar.markdown("### Tentang Dashboard")
st.sidebar.caption(
    "Dashboard analisis pola penyewaan sepeda berdasarkan "
    "jam, kondisi cuaca, suhu, dan tren harian."
)

st.sidebar.caption("Dataset: Bike Sharing Dataset")
st.sidebar.caption("Periode: 2011–2012")

if data_filter.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()


# Header Dashboard
st.markdown(
    """
    <div class="header-card">
        <div class="main-title">
            🚲 Bike Sharing Analytics
        </div>
        <div class="subtitle">
            Dashboard Analisis Pola Penyewaan Sepeda Tahun 2011–2012
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# Ringkasan Penyewaan Sepeda
st.markdown(
    '<div class="section-title">Ringkasan Penyewaan Sepeda</div>',
    unsafe_allow_html=True
)

total_penyewaan = data_filter["cnt"].sum()
rata_penyewaan = data_filter["cnt"].mean()
total_casual = data_filter["casual"].sum()
total_registered = data_filter["registered"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Penyewaan",
    f"{total_penyewaan:,.0f}"
)

col2.metric(
    "Rata-rata per Jam",
    f"{rata_penyewaan:,.2f}"
)

col3.metric(
    "Pengguna Casual",
    f"{total_casual:,.0f}"
)

col4.metric(
    "Pengguna Registered",
    f"{total_registered:,.0f}"
)

st.divider()


# Fungsi warna grafik
def warna_bar(data, kolom_nilai):
    nilai_tertinggi = data[kolom_nilai].max()

    return [
        WARNA_HIGHLIGHT if nilai == nilai_tertinggi
        else WARNA_UTAMA
        for nilai in data[kolom_nilai]
    ]


# Grafik 1: Pola penyewaan berdasarkan jam
st.markdown(
    '<div class="section-title">🕒 Pola Penyewaan Berdasarkan Jam</div>',
    unsafe_allow_html=True
)

rata_jam = (
    data_filter.groupby("hr", as_index=False)["cnt"]
    .mean()
)

fig_jam = px.line(
    rata_jam,
    x="hr",
    y="cnt",
    markers=True,
    labels={
        "hr": "Jam",
        "cnt": "Rata-rata Penyewaan"
    }
)

fig_jam.update_traces(
    line=dict(color=WARNA_UTAMA, width=2.5),
    marker=dict(color=WARNA_UTAMA, size=7),
    hovertemplate="Jam: %{x}.00<br>Rata-rata: %{y:.2f}<extra></extra>"
)

fig_jam.update_layout(
    template=tema_grafik,
    height=370,
    margin=dict(l=20, r=20, t=25, b=20),
    xaxis=dict(
        title="Jam",
        tickmode="linear",
        dtick=1,
        range=[-0.5, 23.5]
    ),
    yaxis=dict(
        title="Rata-rata Penyewaan",
        rangemode="tozero"
    ),
    showlegend=False
)

st.plotly_chart(fig_jam, use_container_width=True)


# Grafik 2: Penyewaan berdasarkan kondisi cuaca
st.markdown(
    '<div class="section-title">🌤️ Penyewaan Berdasarkan Kondisi Cuaca</div>',
    unsafe_allow_html=True
)

nama_cuaca = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan Ringan",
    4: "Hujan Lebat"
}

rata_cuaca = (
    data_filter.groupby("weathersit", as_index=False)
    .agg(
        cnt=("cnt", "mean"),
        jumlah_observasi=("cnt", "count")
    )
)

rata_cuaca["Nama Cuaca"] = rata_cuaca["weathersit"].map(nama_cuaca)

fig_cuaca = px.bar(
    rata_cuaca,
    x="Nama Cuaca",
    y="cnt",
    text="cnt",
    labels={
        "Nama Cuaca": "Kondisi Cuaca",
        "cnt": "Rata-rata Penyewaan"
    }
)

fig_cuaca.update_traces(
    marker_color=warna_bar(rata_cuaca, "cnt"),
    texttemplate="%{y:.1f}",
    textposition="outside",
    cliponaxis=False,
    hovertemplate="%{x}<br>Rata-rata: %{y:.2f}<extra></extra>"
)

fig_cuaca.update_layout(
    template=tema_grafik,
    height=370,
    margin=dict(l=20, r=20, t=35, b=20),
    yaxis=dict(
        title="Rata-rata Penyewaan",
        rangemode="tozero"
    ),
    showlegend=False
)

st.plotly_chart(fig_cuaca, use_container_width=True)

st.caption(
    "Catatan: Kategori cuaca dengan jumlah observasi sedikit "
    "perlu diinterpretasikan secara hati-hati."
)


# Grafik 3: Penyewaan berdasarkan periode waktu
st.markdown(
    '<div class="section-title">☀️ Penyewaan Berdasarkan Periode Waktu</div>',
    unsafe_allow_html=True
)

def kategori_waktu(jam):
    if 6 <= jam <= 10:
        return "Pagi"
    elif 11 <= jam <= 15:
        return "Siang"
    elif 16 <= jam <= 20:
        return "Sore"
    else:
        return "Malam"

data_filter["kategori_waktu"] = data_filter["hr"].apply(kategori_waktu)

urutan_waktu = ["Pagi", "Siang", "Sore", "Malam"]

rata_waktu = (
    data_filter.groupby("kategori_waktu", as_index=False)["cnt"]
    .mean()
)

rata_waktu["kategori_waktu"] = pd.Categorical(
    rata_waktu["kategori_waktu"],
    categories=urutan_waktu,
    ordered=True
)

rata_waktu = rata_waktu.sort_values("kategori_waktu")

fig_waktu = px.bar(
    rata_waktu,
    x="kategori_waktu",
    y="cnt",
    text="cnt",
    labels={
        "kategori_waktu": "Periode Waktu",
        "cnt": "Rata-rata Penyewaan"
    }
)

fig_waktu.update_traces(
    marker_color=warna_bar(rata_waktu, "cnt"),
    texttemplate="%{y:.1f}",
    textposition="outside",
    cliponaxis=False
)

fig_waktu.update_layout(
    template=tema_grafik,
    height=370,
    margin=dict(l=20, r=20, t=35, b=20),
    yaxis=dict(
        title="Rata-rata Penyewaan",
        rangemode="tozero"
    ),
    showlegend=False
)

st.plotly_chart(fig_waktu, use_container_width=True)


# Grafik 4: Penyewaan berdasarkan kategori suhu
st.markdown(
    '<div class="section-title">🌡️ Penyewaan Berdasarkan Kategori Suhu</div>',
    unsafe_allow_html=True
)

data_filter["kategori_suhu"] = pd.cut(
    data_filter["temp"],
    bins=[0, 0.3, 0.6, 1.0],
    labels=["Dingin", "Sedang", "Panas"],
    include_lowest=True
)

rata_suhu = (
    data_filter.groupby(
        "kategori_suhu",
        observed=True,
        as_index=False
    )["cnt"].mean()
)

fig_suhu = px.bar(
    rata_suhu,
    x="kategori_suhu",
    y="cnt",
    text="cnt",
    labels={
        "kategori_suhu": "Kategori Suhu",
        "cnt": "Rata-rata Penyewaan"
    }
)

fig_suhu.update_traces(
    marker_color=warna_bar(rata_suhu, "cnt"),
    texttemplate="%{y:.1f}",
    textposition="outside",
    cliponaxis=False
)

fig_suhu.update_layout(
    template=tema_grafik,
    height=370,
    margin=dict(l=20, r=20, t=35, b=20),
    yaxis=dict(
        title="Rata-rata Penyewaan",
        rangemode="tozero"
    ),
    xaxis_title="Kategori Suhu (Nilai Normalisasi)",
    showlegend=False
)

st.plotly_chart(fig_suhu, use_container_width=True)

st.caption(
    "Catatan: Kategori suhu dibentuk berdasarkan nilai temp "
    "yang telah dinormalisasi pada dataset."
)


# Grafik 5: Tren penyewaan sepeda harian
st.markdown(
    '<div class="section-title">📈 Tren Penyewaan Sepeda</div>',
    unsafe_allow_html=True
)

tren_harian = (
    data_filter.groupby("dteday", as_index=False)["cnt"]
    .sum()
)

fig_tren = px.line(
    tren_harian,
    x="dteday",
    y="cnt",
    labels={
        "dteday": "Tanggal",
        "cnt": "Total Penyewaan"
    }
)

fig_tren.update_traces(
    line=dict(color=WARNA_UTAMA, width=2)
)

fig_tren.update_layout(
    template=tema_grafik,
    height=370,
    margin=dict(l=20, r=20, t=25, b=20),
    xaxis_title="Tanggal",
    yaxis=dict(
        title="Total Penyewaan",
        rangemode="tozero"
    ),
    showlegend=False
)

st.plotly_chart(fig_tren, use_container_width=True)


# Insight Analisis
st.divider()

st.markdown(
    '<div class="section-title">Insight Analisis</div>',
    unsafe_allow_html=True
)

jam_tertinggi = rata_jam.loc[rata_jam["cnt"].idxmax()]
jam_terendah = rata_jam.loc[rata_jam["cnt"].idxmin()]

cuaca_tertinggi = rata_cuaca.loc[rata_cuaca["cnt"].idxmax()]
cuaca_terendah = rata_cuaca.loc[rata_cuaca["cnt"].idxmin()]

waktu_tertinggi = rata_waktu.loc[rata_waktu["cnt"].idxmax()]
suhu_tertinggi = rata_suhu.loc[rata_suhu["cnt"].idxmax()]

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>🕒 Pola Waktu Penyewaan</b><br>
            Jam tersibuk adalah pukul
            <b>{int(jam_tertinggi['hr']):02d}.00</b>
            dengan rata-rata
            <b>{jam_tertinggi['cnt']:.2f}</b> penyewaan.
            Jam terendah adalah pukul
            <b>{int(jam_terendah['hr']):02d}.00</b>.
            Periode dengan rata-rata tertinggi adalah
            <b>{waktu_tertinggi['kategori_waktu']}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>🌤️ Pola Cuaca dan Suhu</b><br>
            Rata-rata penyewaan tertinggi berdasarkan cuaca
            terjadi saat <b>{cuaca_tertinggi['Nama Cuaca']}</b>,
            sedangkan berdasarkan suhu terjadi pada kategori
            <b>{suhu_tertinggi['kategori_suhu']}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


# Footer
st.divider()

st.markdown(
    """
    <div class="footer">
        Bike Sharing Analytics Dashboard<br>
        Data Source: Bike Sharing Dataset | 2011–2012
    </div>
    """,
    unsafe_allow_html=True
)
