import streamlit as st
import pandas as pd
from utils.io import (
    load_data, save_data,
    load_arac_listesi, save_arac_listesi
)

DATA_PATH = "data/teslimatlar.csv"
ARAC_PATH = "data/arac_listesi.csv"

st.set_page_config(page_title="Sultan Dağıtım Paneli", layout="centered")

# Sayfa kontrolü
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "ana"

# ---------------------------
# 🏠 ANA SAYFA
# ---------------------------
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

# ---------------------------
# 📅 PLANLAMA
# ---------------------------
if st.session_state.sayfa == "planlama":
    st.title("📅 Teslimat Planlama")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"
    # ... Planlama modülü buraya eklenecek

# ---------------------------
# 🚚 TESLİMAT
# ---------------------------
if st.session_state.sayfa == "teslimat":
    st.title("🚚 Şoför Teslimat Paneli")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"
    # ... Teslimat modülü buraya eklenecek

# ---------------------------
# 📊 RAPORLAMA
# ---------------------------
if st.session_state.sayfa == "raporlama":
    st.title("📊 Teslimat Raporları")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"
    # ... Raporlama modülü buraya eklenecek

# ---------------------------
# ⚙️ TANIMLAMALAR
# ---------------------------
if st.session_state.sayfa == "tanimlamalar":
    st.title("⚙️ Araç Tanımları")
    if st.button("🔙 Ana Menü"):
        st.session_state.sayfa = "ana"
    # ... Tanımlamalar modülü buraya eklenecek
