import streamlit as st
import pickle
import pandas as pd

# =========================
# Load Model dan Encoder
# =========================
model = pickle.load(open("car_price_model.pkl", "rb"))
encoders = pickle.load(open("label_encoders.pkl", "rb"))

# =========================
# Konfigurasi Halaman
# =========================
st.set_page_config(
    page_title="Prediksi Harga Mobil",
    page_icon="🚗",
    layout="wide"
)

# =========================
# Header
# =========================
st.title("🚗 Website Prediksi Harga Mobil")
st.write("Masukkan spesifikasi mobil untuk mengetahui estimasi harga jual mobil.")

st.markdown("---")

# =========================
# Layout 2 Kolom
# =========================
col1, col2 = st.columns(2)

with col1:
    merek = st.selectbox(
        "Merek Mobil",
        encoders["Merek"].classes_
    )

    model_mobil = st.selectbox(
        "Model Mobil",
        encoders["Model"].classes_
    )

    tahun = st.number_input(
        "Tahun Mobil",
        min_value=2000,
        max_value=2026,
        value=2020
    )

    kapasitas_mesin = st.number_input(
        "Kapasitas Mesin (Liter)",
        min_value=0.8,
        max_value=5.0,
        value=2.0
    )

with col2:
    jarak_tempuh = st.number_input(
        "Jarak Tempuh (KM)",
        min_value=0,
        max_value=300000,
        value=50000
    )

    bahan_bakar = st.selectbox(
        "Jenis Bahan Bakar",
        encoders["Jenis bahan bakar"].classes_
    )

    transmisi = st.selectbox(
        "Jenis Transmisi",
        encoders["Jenis transmisi"].classes_
    )

# =========================
# Encoding
# =========================
merek_encoded = encoders["Merek"].transform([merek])[0]
model_encoded = encoders["Model"].transform([model_mobil])[0]
bahan_bakar_encoded = encoders["Jenis bahan bakar"].transform([bahan_bakar])[0]
transmisi_encoded = encoders["Jenis transmisi"].transform([transmisi])[0]

st.markdown("---")

# =========================
# Tombol Prediksi
# =========================
if st.button("Prediksi Harga"):

    input_data = pd.DataFrame([[
        merek_encoded,
        model_encoded,
        tahun,
        kapasitas_mesin,
        jarak_tempuh,
        bahan_bakar_encoded,
        transmisi_encoded
    ]], columns=[
        "Merek",
        "Model",
        "Tahun",
        "Kapasitas mesin mobil",
        "Jarak tempuh mobil",
        "Jenis bahan bakar",
        "Jenis transmisi"
    ])

    prediksi = model.predict(input_data)[0]

    # Konversi ke Rupiah (jika dataset asli dolar)
    kurs = 16000
    harga_rupiah = prediksi * kurs

    st.success(
        f"Estimasi Harga Mobil: Rp {harga_rupiah:,.0f}"
    )