
import streamlit as st

st.set_page_config(page_title="Sultan Dağıtım Paneli", layout="centered")

st.title("🚚 Sultan Dağıtım Paneli")
st.markdown("Lütfen bir modül seçin:")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/planlama.py", label="📅 Planlama", icon="📅")
    st.page_link("pages/tanimlamalar.py", label="⚙️ Tanımlamalar", icon="⚙️")
with col2:
    st.page_link("pages/teslimat.py", label="🚚 Teslimat", icon="🚚")
    st.page_link("pages/raporlama.py", label="📊 Raporlama", icon="📊")
