
import streamlit as st
import pandas as pd
from utils.io import load_data, load_arac_listesi

DATA_PATH = "data/teslimatlar.csv"
ARAC_PATH = "data/arac_listesi.csv"

st.set_page_config(page_title="Raporlama", layout="centered")
st.title("📊 Teslimat Raporlama")

df = load_data(DATA_PATH)
araclar_df = load_arac_listesi(ARAC_PATH)
plaka_listesi = [""] + araclar_df["plaka"].tolist()

col1, col2, col3, col4 = st.columns(4)
with col1:
    rapor_tarih = st.date_input("📅 Tarih", key="rt")
with col2:
    rapor_plaka = st.selectbox("🚗 Plaka", options=plaka_listesi, key="rp")
with col3:
    rapor_tur = st.selectbox("📦 Tur No", options=[None, 1, 2, 3, 4, 5], key="rn")
with col4:
    durum_sec = st.selectbox("📌 Durum", options=["Tümü", "Teslim Edildi", "Bekliyor"], key="rd")

rapor_df = df[df["tarih"] == pd.to_datetime(rapor_tarih)]

if rapor_plaka:
    rapor_df = rapor_df[rapor_df["plaka"] == rapor_plaka]
if rapor_tur is not None:
    rapor_df = rapor_df[rapor_df["tur_no"] == rapor_tur]
if durum_sec != "Tümü":
    rapor_df = rapor_df[rapor_df["teslim_durumu"] == durum_sec]

rapor_df = rapor_df.sort_values(by=["plaka", "tur_no", "sira_no"])
st.write(f"🔎 **{len(rapor_df)} kayıt bulundu.**")
st.dataframe(rapor_df.reset_index(drop=True), use_container_width=True)

csv = rapor_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV Olarak İndir", data=csv, file_name="teslimat_raporu.csv", mime="text/csv")
