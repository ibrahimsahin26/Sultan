
import streamlit as st
import pandas as pd
import os
from utils.io import load_data, save_data, load_arac_listesi

DATA_PATH = "data/teslimatlar.csv"
ARAC_PATH = "data/arac_listesi.csv"
TUR_SAAT_PATH = "data/tur_saatleri.csv"

st.set_page_config(page_title="Teslimat Takibi", layout="centered")
st.title("🚚 Şoför Teslimat Paneli")

tarih_sec = st.date_input("📅 Tarih")
araclar_df = load_arac_listesi(ARAC_PATH)
plaka_listesi = araclar_df["plaka"].tolist()
plaka_sec = st.selectbox("🚗 Plaka", options=plaka_listesi)

# ------------------------------
# 🕒 TUR BAZLI GİRİŞ / ÇIKIŞ SAATİ GİRİŞİ
# ------------------------------
st.markdown("---")
st.subheader("🕒 Tur Bazlı Giriş / Çıkış Saatleri")

with st.form("tur_saatleri_form"):
    tur_kayitlari = []
    for tur_no in range(1, 6):
        st.markdown(f"**🚚 {tur_no}. Tur**")
        cols = st.columns(4)
        aciklama = cols[0].text_input(f"Açıklama {tur_no}", key=f"aciklama_{tur_no}")
        cikis_saat = cols[1].time_input(f"Çıkış {tur_no}", key=f"cikis_{tur_no}")
        giris_saat = cols[2].time_input(f"Giriş {tur_no}", key=f"giris_{tur_no}")
        tur_kayitlari.append({
            "tarih": tarih_sec,
            "plaka": plaka_sec,
            "tur_no": tur_no,
            "aciklama": aciklama,
            "cikis_saat": cikis_saat.strftime("%H:%M"),
            "giris_saat": giris_saat.strftime("%H:%M")
        })
    kaydet_tur = st.form_submit_button("💾 Saatleri Kaydet")

if kaydet_tur:
    if not os.path.exists(TUR_SAAT_PATH):
        saat_df = pd.DataFrame(columns=["tarih", "plaka", "tur_no", "aciklama", "cikis_saat", "giris_saat"])
    else:
        saat_df = pd.read_csv(TUR_SAAT_PATH)

    yeni_df = pd.DataFrame(tur_kayitlari)
    saat_df = pd.concat([saat_df, yeni_df], ignore_index=True)
    saat_df.to_csv(TUR_SAAT_PATH, index=False)
    st.success("Tüm tur saatleri başarıyla kaydedildi.")

# ------------------------------
# TESLİMAT PLAN GÖSTERİMİ
# ------------------------------
st.markdown("---")
st.subheader("📋 Teslimat Planı ve Durumu")

tur_sec = st.selectbox("📦 Tur No", [1, 2, 3, 4, 5])
goster = st.button("📋 Seçili Planı Göster")

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
