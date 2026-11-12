# Bike Sharing Data Analysis Dashboard

## Deskripsi Proyek

Proyek ini merupakan analisis data penyewaan sepeda (*Bike Sharing*) selama periode 2011–2012. Analisis dilakukan untuk mengetahui pola penyewaan sepeda berdasarkan jam dalam sehari serta perbedaan rata-rata jumlah penyewaan berdasarkan kondisi cuaca.

Hasil analisis disajikan dalam bentuk visualisasi dan dashboard interaktif menggunakan Streamlit untuk membantu memahami pola permintaan penyewaan sepeda.

## Struktur Direktori

```text
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment - Anaconda

```bash
conda create --name bike-sharing python=3.11
conda activate bike-sharing
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

Masuk ke direktori dashboard:

```bash
cd dashboard
```

Jalankan aplikasi Streamlit:

```bash
python -m streamlit run dashboard.py
```

Setelah berhasil dijalankan, dashboard dapat diakses melalui browser pada alamat lokal yang ditampilkan di terminal.

## Teknologi yang Digunakan

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook