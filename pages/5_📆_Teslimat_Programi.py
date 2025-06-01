import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

TUR_SAAT_PATH = "data/tur_saatleri.csv"

st.set_page_config(page_title="Teslimat Programı", layout="wide")
st.title("📆 Teslimat Programı")

# ⛑ Dosya kontrolü
if not os.path.exists(TUR_SAAT_PATH):
    st.info("Henüz tanımlı tur bulunmuyor.")
    st.stop()

# 📄 CSV veri yükleme
df = pd.read_csv(TUR_SAAT_PATH)

# 🗓️ Tarih sütununu datetime yap
try:
    df["tarih"] = pd.to_datetime(df["tarih"])
except:
    st.error("Tarih formatı okunamadı. Lütfen CSV dosyasını kontrol edin.")
    st.stop()

# 📆 Tüm haftaları sırayla ayır
haftalar = {}
for _, row in df.iterrows():
    tarih = row["tarih"]
    yil, hafta_num = tarih.isocalendar()[:2]
    pazartesi = tarih - timedelta(days=tarih.weekday())
    cumartesi = pazartesi + timedelta(days=5)
    hafta_etiketi = f"{hafta_num}. Hafta: {pazartesi.strftime('%-d')}–{cumartesi.strftime('%-d %B')}"

    if hafta_etiketi not in haftalar:
        haftalar[hafta_etiketi] = {gun: [] for gun in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"]}
        haftalar[hafta_etiketi]["_tarih_aralik"] = pazartesi  # sıralama için

    gun = tarih.strftime("%A")
    gun_tr = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }.get(gun, gun)

    if gun_tr in haftalar[hafta_etiketi]:
        haftalar[hafta_etiketi][gun_tr].append(f"{int(row['tur_no'])}. Tur: {row['aciklama']}")

# 🔽 Geçmişten bugüne doğru sırala
haftalar = dict(sorted(haftalar.items(), key=lambda x: x[1]["_tarih_aralik"]))

# 🧾 Tablo başlığı
cols = ["Hafta"] + ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"]
st.markdown("""
<style>
    .st-emotion-cache-13ejsyy p {margin-bottom: 0.3rem;}
</style>
"", unsafe_allow_html=True)

for hafta_etiketi, veri in haftalar.items():
    with st.expander(hafta_etiketi):
        cols = st.columns(6)
        for idx, gun in enumerate(["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"]):
            with cols[idx]:
                st.markdown(f"**{gun}**")
                if veri[gun]:
                    for satir in veri[gun]:
                        st.markdown(f"- {satir}")
                else:
                    st.write("—")
