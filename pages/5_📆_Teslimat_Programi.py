import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

TUR_SAAT_PATH = "data/tur_saatleri.csv"

st.set_page_config(page_title="Teslimat Programı", layout="wide")
st.title("📆 Teslimat Programı")

# Dosya kontrolü
if not os.path.exists(TUR_SAAT_PATH):
    st.info("Henüz tanımlı tur bulunmuyor.")
    st.stop()

# Veri yükleme
df = pd.read_csv(TUR_SAAT_PATH)

# Tarihleri datetime objesine çevir
try:
    df["tarih"] = pd.to_datetime(df["tarih"])
except:
    st.error("Tarih formatı okunamadı. Lütfen CSV dosyasını kontrol edin.")
    st.stop()

# Bu haftanın pazartesi - pazar arası
bugun = datetime.today()
pazartesi = bugun - timedelta(days=bugun.weekday())
pazar = pazartesi + timedelta(days=6)

haftalik_df = df[(df["tarih"] >= pazartesi) & (df["tarih"] <= pazar)]

# Gün isimleri
hafta_gunleri = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
gun_sutunlari = {gun: [] for gun in hafta_gunleri}

# Veriyi günlere ayır
for i, row in haftalik_df.iterrows():
    gun = row["tarih"].strftime("%A")
    gun_tr = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }[gun]
    gun_sutunlari[gun_tr].append(f"{int(row['tur_no'])}. Tur: {row['aciklama']}")

# Tabloyu çiz
cols = st.columns(7)
for i, gun in enumerate(hafta_gunleri):
    with cols[i]:
        st.markdown(f"### {gun}")
        if gun_sutunlari[gun]:
            for tur in gun_sutunlari[gun]:
                st.markdown(f"- {tur}")
        else:
            st.write("—")
