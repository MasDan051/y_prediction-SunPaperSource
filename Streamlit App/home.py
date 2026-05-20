import streamlit as st

st.set_page_config(
    page_title="Paper Machine Prediction App",
    layout="wide"
)

st.title("Paper Machine Prediction System")

st.markdown("""
## Pilih Jenis Prediksi
""")

# =========================
# MDT SECTION
# =========================

st.subheader("📌 Prediksi MDT")

col1, col2 = st.columns(2)

with col1:
    st.page_link(
        "pages/MDT_1_PM14.py",
        label="PM14 MDT",
        icon="📄"
    )

with col2:
    st.page_link(
        "pages/MDT_2_PM15.py",
        label="PM15 MDT",
        icon="📄"
    )

# =========================
# MDS SECTION
# =========================

st.subheader("📌 Prediksi MDS")

col3, col4 = st.columns(2)

with col3:
    st.page_link(
        "pages/MDS_1_PM14.py",
        label="PM14 MDS",
        icon="📊"
    )

with col4:
    st.page_link(
        "pages/MDS_2_PM15.py",
        label="PM15 MDS",
        icon="📊"
    )

st.divider()

st.caption("""
    Paper Machine Simulation System for MDT and MDS Prediction.    
    Create by Daniel Wicaksono N. & Michael Adi H.

""")