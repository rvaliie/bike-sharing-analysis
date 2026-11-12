import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide"
)


WARNA_UTAMA = "#238477"
WARNA_HIGHLIGHT = "#E59A45"

tema_grafik = (
    "plotly_dark"
    if st.context.theme == "dark"
    else "plotly_white"
)

st.markdown("""
<style>
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: var(--text-color);
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 15px;
        color: var(--text-color);
        opacity: 0.75;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: var(--text-color);
        margin-top: 15px;
        margin-bottom: 10px;
    }

    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 13px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricDelta"] {
        color: var(--text-color);
    }

    div[data-testid="stPlotlyChart"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-radius: 13px;
        padding: 10px;
    }

    .insight-box {
        background-color: var(--secondary-background-color);
        border-left: 5px solid #238477;
        padding: 15px 18px;
        border-radius: 8px;
        color: var(--text-color);
        margin-bottom: 10px;
    }

    .footer {
        text-align: center;
        color: var(--text-color);
        opacity: 0.65;
        font-size: 13px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)


# memuat dataset
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    data = pd.read_csv(BASE_DIR / "main_data.csv")
    data["dteday"] = pd.to_datetime(data["dteday"])
    return data

df = load_data()


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



st.markdown(
    '<div class="main-title">🚲 Bike Sharing Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Dashboard Analisis Pola Penyewaan Sepeda Tahun 2011–2012'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


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



def warna_bar(data, kolom_nilai):
    nilai_tertinggi = data[kolom_nilai].max()

    return [
        WARNA_HIGHLIGHT if nilai == nilai_tertinggi
        else WARNA_UTAMA
        for nilai in data[kolom_nilai]
    ]


# grafik 1: pola penyewaan berdasarkan jam
st.markdown(
    '<div class="section-title">1. Pola Penyewaan Berdasarkan Jam</div>',
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


# grafik 2: penyewaan berdasarkan kondisi cuaca
st.markdown(
    '<div class="section-title">2. Penyewaan Berdasarkan Kondisi Cuaca</div>',
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


# grafik 3: penyewaan berdasarkan periode waktu

st.markdown(
    '<div class="section-title">3. Penyewaan Berdasarkan Periode Waktu</div>',
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


# grafik 4: penyewaan berdasarkan kategori suhu

st.markdown(
    '<div class="section-title">4. Penyewaan Berdasarkan Kategori Suhu</div>',
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


# grafik 5: tren penyewaan sepeda harian

st.markdown(
    '<div class="section-title">5. Tren Penyewaan Sepeda</div>',
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


# insight analisis

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
            <b>Pola Waktu Penyewaan</b><br>
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
            <b>Pola Cuaca dan Suhu</b><br>
            Rata-rata penyewaan tertinggi berdasarkan cuaca
            terjadi saat <b>{cuaca_tertinggi['Nama Cuaca']}</b>,
            sedangkan berdasarkan suhu terjadi pada kategori
            <b>{suhu_tertinggi['kategori_suhu']}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


# footer
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
