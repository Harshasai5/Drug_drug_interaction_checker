import os
import re
import pandas as pd
from google.cloud import vision
from fuzzywuzzy import process
from spellchecker import SpellChecker

# 🔐 Set your service account JSON key path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"credentials/vision_key.json"

# 🔍 Load Google Vision API client
client = vision.ImageAnnotatorClient()

# 📸 1. OCR using Google Vision API
def google_vision_extract_text(image_path):
    with open(image_path, 'rb') as img_file:
        content = img_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")
    
    texts = response.text_annotations
    return texts[0].description if texts else ""

# 🧼 2. Clean and split OCR text into words
def preprocess_text(raw_text):
    cleaned_text = raw_text.lower()
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)
    words = cleaned_text.split()
    return words

# 🔎 3. Match words to known drug names using fuzzy matching
def fuzzy_match(drug_list, words, threshold=85):
    matched_drugs = []
    for word in words:
        best_match, score = process.extractOne(word, drug_list)
        if score >= threshold:
            matched_drugs.append(best_match)
    return list(set(matched_drugs))  # Remove duplicates

# ⚠️ 4. Check interactions between detected drugs
def check_interactions(drug_list, interaction_df):
    found_interactions = []

    # Normalize column names for safety
    interaction_df.columns = [col.strip() for col in interaction_df.columns]

    for i in range(len(drug_list)):
        for j in range(i + 1, len(drug_list)):
            d1, d2 = drug_list[i], drug_list[j]

            # Check both (d1, d2) and (d2, d1) regardless of case
            interaction = interaction_df[
                ((interaction_df['Drug 1'].str.lower() == d1.lower()) &
                 (interaction_df['Drug 2'].str.lower() == d2.lower())) |
                ((interaction_df['Drug 1'].str.lower() == d2.lower()) &
                 (interaction_df['Drug 2'].str.lower() == d1.lower()))
            ]

            if not interaction.empty:
                found_interactions.append({
                    'Drug 1': d1,
                    'Drug 2': d2,
                    'Interaction': interaction.iloc[0]['Interaction Description']
                })

    return found_interactions
