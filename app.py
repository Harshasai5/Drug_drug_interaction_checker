import streamlit as st
import pandas as pd
import os
from PIL import Image
from interaction_utils import (
    google_vision_extract_text,
    preprocess_text,
    fuzzy_match,
    check_interactions
)

# 🗂️ Load drug interaction dataset
@st.cache_data
def load_interaction_data():
    return pd.read_csv("db_drug_interactions.csv")

interaction_df = load_interaction_data()

# 🧠 Generate drug list
drug_list = list(set(interaction_df['Drug 1'].tolist() + interaction_df['Drug 2'].tolist()))

# 🚀 App Title
st.set_page_config(page_title="Drug Interaction Checker", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #2C3E50;'>🩺 Drug Interaction Checker</h1>
    <p style='text-align: center; font-size: 16px;'>Upload a handwritten or printed prescription and detect harmful drug interactions automatically.</p>
    <hr style='margin-top: 10px; margin-bottom: 20px;'>
""", unsafe_allow_html=True)

# 📤 Image Upload Section
with st.container():
    st.subheader("📤 Upload Prescription Image")
    uploaded_file = st.file_uploader("Accepted formats: PNG, JPG, JPEG", type=["png", "jpg", "jpeg"])

# 🧪 Processing Section
if uploaded_file:
    image_path = "temp_image.png"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(image_path, caption="🖼️ Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text using Google Vision API..."):
        raw_text = google_vision_extract_text(image_path)

    with st.expander("📄 View Extracted Text"):
        st.text_area("Extracted Text", raw_text, height=200)

    # 🧹 Preprocess + Fuzzy Match
    words = preprocess_text(raw_text)
    matched_drugs = fuzzy_match(drug_list, words)

    st.markdown("### 💊 Matched Drugs")
    if matched_drugs:
        st.success(", ".join(matched_drugs))
    else:
        st.warning("⚠️ No known drug names matched. Please try with a clearer image.")

    # 🧪 Interaction Checker
    if len(matched_drugs) >= 2:
        st.markdown("### ⚠️ Drug Interaction Results")
        interactions = check_interactions(matched_drugs, interaction_df)

        if interactions:
            for item in interactions:
                st.error(f"🔺 **{item['Drug 1']} + {item['Drug 2']}** → _{item['Interaction']}_")
        else:
            st.success("✅ No interactions found among the matched drugs.")
    else:
        st.info("ℹ️ At least **two drugs** are needed to check for interactions.")

# 📝 Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 14px;'>
        Made with ❤️ using Streamlit & Google Vision API | 2025
    </div>
""", unsafe_allow_html=True)
