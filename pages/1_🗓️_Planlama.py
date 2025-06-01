import os
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.io import load_data, save_data, load_arac_listesi

# 📁 Dosya yolları
DATA_PATH = "data/teslimatlar.csv"
ARAC_PATH = "data/arac_listesi.csv"
TUR_SAAT_PATH = "data/tur_saatleri.csv"

# ⛑ Eğer tur_saatleri.csv yoksa veya tamamen boşsa, başlıkları ile oluştur
if not os.path.exists(TUR_SAAT_PATH) or os.path.getsize(TUR_SAAT_PATH) == 0:
    pd.DataFrame(columns=[
        "tarih", "plaka", "tur_no", "aciklama", "cikis_saat", "giris_saat"
    ]).to_csv(TUR_SAAT_PATH, index=False)

# ✅ Artık dosyayı rahatça okuyabiliriz
tur_saat_df = pd.read_csv(TUR_SAAT_PATH)

# 📄 Sayfa ayarı
st.set_page_config(page_title="Dağıtım Planlama", layout="centered")
st.title("🗓️ Dağıtım Planlama")

# 📅 Tarih ve plaka seçimi
tarih = st.date_input("📅 Tarih Seçin", value=datetime.today())
araclar_df = load_arac_listesi(ARAC_PATH)
plaka_sec = st.selectbox("🚗 Araç Seçin", araclar_df["plaka"].tolist())

# 📦 Teslimat planı verisi
plan_df = load_data(DATA_PATH)

# 🔁 1–5 arası tur planlama alanları
for tur_no in range(1, 6):
    st.markdown(f"### 🚚 {tur_no}. Tur Planı")
    with st.form(f"form_{tur_no}", clear_on_submit=False):
        tur_aciklama = st.text_input(f"{tur_no}. Tur Açıklama", key=f"aciklama_{tur_no}")
        teslimat_sayisi = st.slider(f"Teslimat Nokta Sayısı", 1, 10, key=f"adet_{tur_no}")
        teslimatlar = []
        for i in range(teslimat_sayisi):
            musteri = st.text_input(f"{i+1}. Müşteri Adı", key=f"musteri_{tur_no}_{i}")
not_ = ""
if musteri:
    not_ = st.text_input(f"↪️ {i+1}. Müşteri Notu", placeholder="örn: Tahsilat yapılacak", key=f"not_{tur_no}_{i}")
teslimatlar.append({"musteri": musteri, "not": not_})
            teslimatlar.append(musteri)
        kaydet = st.form_submit_button("💾 Kaydet")

    if kaydet:
        for i, musteri in enumerate(teslimatlar):
            yeni_kayit = {
                "tarih": tarih,
                "plaka": plaka_sec,
                "tur_no": tur_no,
                "sira_no": i+1,
                "musteri": musteri,
                "teslim_durumu": "Planlandı"
            }
            plan_df = pd.concat([plan_df, pd.DataFrame([yeni_kayit])], ignore_index=True)

        # Tur açıklamasını ve saat alanlarını boş olarak kaydet
        tur_saat_df = pd.concat([
            tur_saat_df,
            pd.DataFrame([{
                "tarih": tarih,
                "plaka": plaka_sec,
                "tur_no": tur_no,
                "aciklama": tur_aciklama,
                "cikis_saat": "",
                "giris_saat": ""
            }])
        ], ignore_index=True)

        save_data(plan_df, DATA_PATH)
        tur_saat_df.to_csv(TUR_SAAT_PATH, index=False)
        st.success(f"{tur_no}. Tur planı ve açıklaması kaydedildi.")
# 📋 Planlanan teslimatları göster
st.markdown("---")
st.subheader("📋 Planlanan Teslimatlar")

# Eğer plan_df boş değilse
if not plan_df.empty:
    plan_df["tarih"] = pd.to_datetime(plan_df["tarih"])
    plan_df = plan_df.sort_values(by=["tarih", "tur_no", "sira_no"])

    grouped = plan_df.groupby(["tarih", "plaka", "tur_no"])

    for (tarih, plaka, tur_no), grup in grouped:
        st.markdown(f"### 🛻 {tur_no}. Tur – {tarih.strftime('%d %B %Y')} – 🚗 {plaka}")
        for i, row in grup.iterrows():
            musteri = row["musteri"]
            not_text = row.get("not", "")
            if not_text:
                st.markdown(f"- **{musteri}**  \n  🔖 _{not_text}_")
            else:
                st.markdown(f"- **{musteri}**")
        st.markdown("---")
else:
    st.info("Henüz planlanan bir teslimat bulunmuyor.")
