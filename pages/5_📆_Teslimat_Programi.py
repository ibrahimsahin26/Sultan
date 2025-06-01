import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

TUR_SAAT_PATH = "data/tur_saatleri.csv"

st.set_page_config(page_title="Teslimat Programı", layout="wide")
st.title("📆 Teslimat Programı")

# Tarih seçimi
secili_tarih = st.date_input("🔎 Haftasını görmek istediğiniz tarihi seçin", value=datetime.today())

# Başlangıç ve bitiş tarihleri (geçmiş 2 hafta, seçili hafta, gelecek 4 hafta)
baslangic_tarih = secili_tarih - timedelta(weeks=2)
bitis_tarih = secili_tarih + timedelta(weeks=4)

# Dosya kontrolü
veri_var = False
if os.path.exists(TUR_SAAT_PATH) and os.path.getsize(TUR_SAAT_PATH) > 0:
    df = pd.read_csv(TUR_SAAT_PATH)
    try:
        df["tarih"] = pd.to_datetime(df["tarih"])
        veri_var = True
    except:
        st.error("Tarih formatı okunamadı. Lütfen CSV dosyasını kontrol edin.")
        st.stop()
else:
    df = pd.DataFrame(columns=["tarih", "plaka", "tur_no", "aciklama", "cikis_saat", "giris_saat"])
    df["tarih"] = pd.to_datetime([])

# Haftaları topla
haftalar = {}

bugun = datetime.today()
basla = baslangic_tarih - timedelta(days=baslangic_tarih.weekday())
bitis = bitis_tarih + timedelta(days=(5 - bitis_tarih.weekday()))
suan = basla

while suan <= bitis:
    yil, hafta_num = suan.isocalendar()[:2]
    pazartesi = suan
    cumartesi = pazartesi + timedelta(days=5)
    hafta_etiketi = f"{hafta_num}. Hafta: {pazartesi.strftime('%-d')}–{cumartesi.strftime('%-d %B')}"

    haftalar[hafta_etiketi] = {gun: [] for gun in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"]}
    haftalar[hafta_etiketi]["_tarih_aralik"] = pazartesi
    suan += timedelta(weeks=1)

# Verileri haftalara yerleştir
if veri_var:
    for _, row in df.iterrows():
        tarih = row["tarih"]
        yil, hafta_num = tarih.isocalendar()[:2]
        pazartesi = tarih - timedelta(days=tarih.weekday())
        cumartesi = pazartesi + timedelta(days=5)
        hafta_etiketi = f"{hafta_num}. Hafta: {pazartesi.strftime('%-d')}–{cumartesi.strftime('%-d %B')}"

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

        if hafta_etiketi in haftalar and gun_tr in haftalar[hafta_etiketi]:
            haftalar[hafta_etiketi][gun_tr].append(f"{int(row['tur_no'])}. Tur: {row['aciklama']}")

# Sırala ve çiz
haftalar = dict(sorted(haftalar.items(), key=lambda x: x[1]["_tarih_aralik"]))

st.markdown("""
<style>
    .st-emotion-cache-13ejsyy p {margin-bottom: 0.3rem;}
</style>
""", unsafe_allow_html=True)

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
