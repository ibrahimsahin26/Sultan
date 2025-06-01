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
# --------------------------
# 🚚 ŞOFÖR GÖRÜNÜMÜ ve BUTONLAR
# --------------------------
st.markdown("---")
st.subheader("🚚 Şoför Paneli - Teslimat Takibi")

with st.form("sofor_formu"):
    tarih_sec = st.date_input("📅 Tarih", value=tarih, key="t2")
    plaka_sec = st.text_input("🚗 Plaka", value=plaka, key="p2")
    tur_sec = st.selectbox("📦 Tur No", [1, 2, 3, 4, 5], index=tur_no-1, key="tur2")
    goster = st.form_submit_button("📋 Planı Göster")

if goster:
    df = load_data(DATA_PATH)
    aktif_tur = df[
        (df["tarih"] == pd.to_datetime(tarih_sec)) &
        (df["plaka"] == plaka_sec.upper()) &
        (df["tur_no"] == tur_sec)
    ].sort_values("sira_no").reset_index(drop=True)

    if aktif_tur.empty:
        st.warning("Bu tarihte seçilen araç ve tur için plan bulunamadı.")
    else:
        st.write(f"📦 **{plaka_sec.upper()} / {tur_sec}. Tur** için teslimat listesi:")
        for i, row in aktif_tur.iterrows():
            cols = st.columns([5, 2])
            cols[0].markdown(f"**{row['sira_no']}. {row['musteri']}**  —  `{row['teslim_durumu']}`")
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
# --------------------------
# 📊 RAPORLAMA MODÜLÜ
# --------------------------
st.markdown("---")
st.subheader("📊 Raporlama ve Dışa Aktarım")

df = load_data(DATA_PATH)

with st.expander("🔍 Teslimat Raporu"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rapor_tarih = st.date_input("Tarih Seç", value=tarih, key="rt")
    with col2:
        rapor_plaka = st.text_input("Araç Plakası", value="", key="rp")
    with col3:
        rapor_tur = st.selectbox("Tur No", options=[None, 1, 2, 3, 4, 5], key="rn")
    with col4:
        durum_sec = st.selectbox("Durum", options=["Tümü", "Teslim Edildi", "Bekliyor"], key="rd")

    # Filtreleme işlemi
    rapor_df = df.copy()
    rapor_df = rapor_df[rapor_df["tarih"] == pd.to_datetime(rapor_tarih)]

    if rapor_plaka:
        rapor_df = rapor_df[rapor_df["plaka"] == rapor_plaka.upper()]

    if rapor_tur is not None:
        rapor_df = rapor_df[rapor_df["tur_no"] == rapor_tur]

    if durum_sec != "Tümü":
        rapor_df = rapor_df[rapor_df["teslim_durumu"] == durum_sec]

    rapor_df = rapor_df.sort_values(by=["plaka", "tur_no", "sira_no"])

    st.write(f"🔽 **{len(rapor_df)} teslimat kaydı bulundu:**")
    st.dataframe(rapor_df.reset_index(drop=True), use_container_width=True)

    # CSV çıktısı
    csv = rapor_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSV Olarak İndir", data=csv, file_name="teslimat_raporu.csv", mime="text/csv")
