
import streamlit as st
import pandas as pd
from utils.io import load_data, save_data, load_arac_listesi

DATA_PATH = "data/teslimatlar.csv"
ARAC_PATH = "data/arac_listesi.csv"

st.set_page_config(page_title="Planlama", layout="centered")
st.title("📅 Teslimat Planlama")

tarih = st.date_input("Tarih Seç")
araclar_df = load_arac_listesi(ARAC_PATH)
plaka_listesi = araclar_df["plaka"].tolist()
plaka = st.selectbox("Araç Plakası", options=plaka_listesi)
tur_no = st.selectbox("Tur No", [1, 2, 3, 4, 5])

st.subheader("📍 Teslimat Noktası Ekle")
with st.form("teslimat_formu", clear_on_submit=True):
    musteri = st.text_input("Müşteri Adı (2 kelime)")
    sira_no = st.number_input("Teslimat Sırası", min_value=1, max_value=20, step=1)
    ekle = st.form_submit_button("➕ Ekle")

df = load_data(DATA_PATH)

if ekle and musteri and plaka:
    yeni_kayit = pd.DataFrame([{
        "tarih": tarih,
        "plaka": plaka,
        "tur_no": tur_no,
        "sira_no": sira_no,
        "musteri": musteri.title(),
        "teslim_durumu": "Bekliyor"
    }])
    df = pd.concat([df, yeni_kayit], ignore_index=True)
    save_data(df, DATA_PATH)
    st.success(f"{musteri.title()} eklendi.")

st.subheader("📋 Günlük Plan")
filtre_df = df[
    (df["tarih"] == pd.to_datetime(tarih)) &
    (df["plaka"] == plaka) &
    (df["tur_no"] == tur_no)
].sort_values("sira_no")

st.dataframe(filtre_df.reset_index(drop=True), use_container_width=True)
