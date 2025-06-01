
import streamlit as st
import pandas as pd
from utils.io import load_data, save_data, load_arac_listesi

DATA_PATH = "data/teslimatlar.csv"
ARAC_PATH = "data/arac_listesi.csv"

st.set_page_config(page_title="Teslimat Takibi", layout="centered")
st.title("🚚 Şoför Teslimat Paneli")

tarih_sec = st.date_input("📅 Tarih")
araclar_df = load_arac_listesi(ARAC_PATH)
plaka_listesi = araclar_df["plaka"].tolist()
plaka_sec = st.selectbox("🚗 Plaka", options=plaka_listesi)
tur_sec = st.selectbox("📦 Tur No", [1, 2, 3, 4, 5])
goster = st.button("📋 Planı Göster")

if goster:
    df = load_data(DATA_PATH)
    aktif_tur = df[
        (df["tarih"] == pd.to_datetime(tarih_sec)) &
        (df["plaka"] == plaka_sec) &
        (df["tur_no"] == tur_sec)
    ].sort_values("sira_no").reset_index(drop=True)

    if aktif_tur.empty:
        st.warning("Bu seçim için plan bulunamadı.")
    else:
        for i, row in aktif_tur.iterrows():
            cols = st.columns([5, 2])
            cols[0].markdown(f"**{row['sira_no']}. {row['musteri']}** — `{row['teslim_durumu']}`")
            if row["teslim_durumu"] != "Teslim Edildi":
                if cols[1].button("✅ Teslim Edildi", key=f"teslim_{i}"):
                    df_index = df[
                        (df["tarih"] == row["tarih"]) &
                        (df["plaka"] == row["plaka"]) &
                        (df["tur_no"] == row["tur_no"]) &
                        (df["sira_no"] == row["sira_no"])
                    ].index
                    df.loc[df_index, "teslim_durumu"] = "Teslim Edildi"
                    save_data(df, DATA_PATH)
                    st.experimental_rerun()
