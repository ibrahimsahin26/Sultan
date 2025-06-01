import streamlit as st
import pandas as pd
from utils.io import load_data, save_data

DATA_PATH = "data/teslimatlar.csv"

st.set_page_config(page_title="Sultan Dağıtım Paneli", layout="centered")

st.title("🚚 Sultan İçecek - Şehir İçi Dağıtım Planı")

# 1. Takvim ve Araç Seçimi
st.header("📅 Planlama Yap")
col1, col2, col3 = st.columns(3)
with col1:
    tarih = st.date_input("Tarih Seç")
with col2:
    plaka = st.text_input("Araç Plakası", max_chars=20)
with col3:
    tur_no = st.selectbox("Tur No", [1, 2, 3, 4, 5])

st.markdown("---")

# 2. Müşteri Girişi
st.subheader("📍 Teslimat Noktaları")

with st.form("teslimat_formu", clear_on_submit=True):
    musteri = st.text_input("Müşteri Adı (2 kelime)")
    sira_no = st.number_input("Teslimat Sırası", min_value=1, max_value=20, step=1)
    ekle = st.form_submit_button("➕ Noktayı Ekle")

# 3. Veri Yükle ve Güncelle
df = load_data(DATA_PATH)

if ekle and musteri and plaka:
    yeni_kayit = pd.DataFrame([{
        "tarih": tarih,
        "plaka": plaka.upper(),
        "tur_no": tur_no,
        "sira_no": sira_no,
        "musteri": musteri.title(),
        "teslim_durumu": "Bekliyor"
    }])
    df = pd.concat([df, yeni_kayit], ignore_index=True)
    save_data(df, DATA_PATH)
    st.success(f"{musteri.title()} eklendi.")

# 4. Günlük Plan Tablosu
st.subheader("📋 Günlük Plan Görünümü")

filtre_df = df[
    (df["tarih"] == pd.to_datetime(tarih)) &
    (df["plaka"] == plaka.upper()) &
    (df["tur_no"] == tur_no)
].sort_values("sira_no")

st.dataframe(filtre_df.reset_index(drop=True), use_container_width=True)
