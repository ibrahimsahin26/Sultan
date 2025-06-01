import streamlit as st
import pandas as pd
import os
from utils.io import load_data, save_data, load_arac_listesi, save_arac_listesi

DATA_PATH = "data/teslimatlar.csv"
ARAC_PATH = "data/arac_listesi.csv"

st.set_page_config(page_title="Sultan Dağıtım Paneli", layout="centered")

# Sayfa yönlendirme kontrolü
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "ana"

# Ana Menü
if st.session_state.sayfa == "ana":
    st.title("🚚 Sultan Dağıtım Paneli")
    st.markdown("Lütfen bir modül seçin:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 Planlama"):
            st.session_state.sayfa = "planlama"
        if st.button("⚙️ Tanımlamalar"):
            st.session_state.sayfa = "tanimlamalar"
    with col2:
        if st.button("🚚 Teslimat"):
            st.session_state.sayfa = "teslimat"
        if st.button("📊 Raporlama"):
            st.session_state.sayfa = "raporlama"

# Planlama Sayfası
if st.session_state.sayfa == "planlama":
    st.title("📅 Teslimat Planlama")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"

    tarih = st.date_input("Tarih Seç")
    araclar_df = load_arac_listesi(ARAC_PATH)
    plaka_listesi = araclar_df["plaka"].tolist()
    plaka = st.selectbox("Araç Plakası", options=plaka_listesi)
    tur_no = st.selectbox("Tur No", [1, 2, 3, 4, 5])

    st.subheader("📍 Teslimat Noktası Ekle")
    with st.form("teslimat_formu", clear_on_submit=True):
        musteri = st.text_input("Müşteri Adı (2 kelime)")
        sira_no = st.number_input("Teslimat Sırası", min_value=1, max_value=20, step=1)
        ekle = st.form_submit_button("➕ Ekle")

    df = load_data(DATA_PATH)

    if ekle and musteri and plaka:
        yeni_kayit = pd.DataFrame([{
            "tarih": tarih,
            "plaka": plaka,
            "tur_no": tur_no,
            "sira_no": sira_no,
            "musteri": musteri.title(),
            "teslim_durumu": "Bekliyor"
        }])
        df = pd.concat([df, yeni_kayit], ignore_index=True)
        save_data(df, DATA_PATH)
        st.success(f"{musteri.title()} eklendi.")

    st.subheader("📋 Günlük Plan")
    filtre_df = df[
        (df["tarih"] == pd.to_datetime(tarih)) &
        (df["plaka"] == plaka) &
        (df["tur_no"] == tur_no)
    ].sort_values("sira_no")

    st.dataframe(filtre_df.reset_index(drop=True), use_container_width=True)

# Teslimat Sayfası
if st.session_state.sayfa == "teslimat":
    st.title("🚚 Şoför Paneli")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"

    tarih_sec = st.date_input("📅 Tarih", key="t2")
    araclar_df = load_arac_listesi(ARAC_PATH)
    plaka_listesi = araclar_df["plaka"].tolist()
    plaka_sec = st.selectbox("🚗 Plaka", options=plaka_listesi, key="p2")
    tur_sec = st.selectbox("📦 Tur No", [1, 2, 3, 4, 5], key="tur2")
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

# Raporlama Sayfası
if st.session_state.sayfa == "raporlama":
    st.title("📊 Raporlama")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"

    df = load_data(DATA_PATH)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rapor_tarih = st.date_input("Tarih", key="rt")
    with col2:
        araclar_df = load_arac_listesi(ARAC_PATH)
        plaka_listesi = [""] + araclar_df["plaka"].tolist()
        rapor_plaka = st.selectbox("Plaka", options=plaka_listesi, key="rp")
    with col3:
        rapor_tur = st.selectbox("Tur No", options=[None, 1, 2, 3, 4, 5], key="rn")
    with col4:
        durum_sec = st.selectbox("Durum", options=["Tümü", "Teslim Edildi", "Bekliyor"], key="rd")

    rapor_df = df[df["tarih"] == pd.to_datetime(rapor_tarih)]
    if rapor_plaka:
        rapor_df = rapor_df[rapor_df["plaka"] == rapor_plaka]
    if rapor_tur is not None:
        rapor_df = rapor_df[rapor_df["tur_no"] == rapor_tur]
    if durum_sec != "Tümü":
        rapor_df = rapor_df[rapor_df["teslim_durumu"] == durum_sec]

    rapor_df = rapor_df.sort_values(by=["plaka", "tur_no", "sira_no"])
    st.write(f"🔽 **{len(rapor_df)} teslimat kaydı bulundu:**")
    st.dataframe(rapor_df.reset_index(drop=True), use_container_width=True)
    csv = rapor_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSV Olarak İndir", data=csv, file_name="teslimat_raporu.csv", mime="text/csv")

# Tanımlamalar Sayfası
if st.session_state.sayfa == "tanimlamalar":
    st.title("⚙️ Araç Tanımları")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"

    araclar_df = load_arac_listesi(ARAC_PATH)
    st.write("📋 Tanımlı Araçlar")
    st.dataframe(araclar_df, use_container_width=True)

    st.subheader("➕ Yeni Araç Ekle")
    with st.form("arac_formu", clear_on_submit=True):
        yeni_plaka = st.text_input("Plaka")
        aciklama = st.text_input("Açıklama (örn. Araç 1)")
        ekle_arac = st.form_submit_button("Ekle")

    if ekle_arac and yeni_plaka:
        if yeni_plaka in araclar_df["plaka"].values:
            st.warning("Bu plaka zaten tanımlı.")
        else:
            yeni = pd.DataFrame([{"plaka": yeni_plaka.upper(), "aciklama": aciklama}])
            araclar_df = pd.concat([araclar_df, yeni], ignore_index=True)
            save_arac_listesi(araclar_df, ARAC_PATH)
            st.success("Araç eklendi.")
            st.experimental_rerun()
