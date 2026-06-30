import streamlit as st
import pickle
import pandas as pd

# Load model
model_prediksi = pickle.load(open("car_price_model.pkl", "rb"))
encoder_label = pickle.load(open("label_encoders.pkl", "rb"))

# Konfigurasi halaman
st.set_page_config(page_title="Prediksi Harga Mobil", layout="wide")

# Judul
st.title("🚗 Prediksi Harga Mobil")
st.write("Masukkan spesifikasi mobil untuk memprediksi harga jualnya")

# Input user
merek = st.selectbox("Merek Mobil", encoder_label["Merek"].classes_)

model_mobil = st.selectbox(
    "Model Mobil",
    encoder_label["Model"].classes_
)

tahun = st.number_input("Tahun Mobil", 2000, 2026, 2020)

kapasitas_mesin = st.number_input(
    "Kapasitas Mesin (Liter)",
    0.8,
    5.0,
    2.0
)

jarak_tempuh = st.number_input(
    "Jarak Tempuh (KM)",
    0,
    300000,
    50000
)

jenis_bahan_bakar = st.selectbox(
    "Jenis Bahan Bakar",
    encoder_label["Jenis bahan bakar"].classes_
)

jenis_transmisi = st.selectbox(
    "Jenis Transmisi",
    encoder_label["Jenis transmisi"].classes_
)

# Encoding
merek_encoded = encoder_label["Merek"].transform([merek])[0]
model_encoded = encoder_label["Model"].transform([model_mobil])[0]
bahan_bakar_encoded = encoder_label["Jenis bahan bakar"].transform([jenis_bahan_bakar])[0]
transmisi_encoded = encoder_label["Jenis transmisi"].transform([jenis_transmisi])[0]

# Tombol prediksi
if st.button("Prediksi Harga"):

    data_input = pd.DataFrame([[
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

    prediksi_harga = model_prediksi.predict(data_input)[0]

    # Jika dataset aslinya dolar lalu ingin konversi ke rupiah
    kurs = 16000
    harga_rupiah = prediksi_harga * kurs

    st.success(f"Estimasi Harga Mobil: Rp {harga_rupiah:,.0f}")