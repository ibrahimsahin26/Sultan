
import streamlit as st
import pandas as pd
from utils.io import load_arac_listesi, save_arac_listesi

ARAC_PATH = "data/arac_listesi.csv"

st.set_page_config(page_title="Tanımlamalar", layout="centered")
st.title("⚙️ Araç Tanımlamaları")

araclar_df = load_arac_listesi(ARAC_PATH)
st.subheader("📋 Tanımlı Araçlar")
st.dataframe(araclar_df, use_container_width=True)

st.subheader("➕ Yeni Araç Ekle")
with st.form("arac_formu", clear_on_submit=True):
    yeni_plaka = st.text_input("Plaka")
    aciklama = st.text_input("Açıklama (örn. Araç 1)")
    ekle_arac = st.form_submit_button("Ekle")

if ekle_arac and yeni_plaka:
    if yeni_plaka.upper() in araclar_df["plaka"].values:
        st.warning("Bu plaka zaten tanımlı.")
    else:
        yeni = pd.DataFrame([{"plaka": yeni_plaka.upper(), "aciklama": aciklama}])
        araclar_df = pd.concat([araclar_df, yeni], ignore_index=True)
        save_arac_listesi(araclar_df, ARAC_PATH)
        st.success("Araç eklendi.")
        st.experimental_rerun()
