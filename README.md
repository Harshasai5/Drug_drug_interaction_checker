# 🧪 Drug-Drug Interaction Checker from Handwritten Notes

Automatically extract drug names from handwritten prescriptions and identify possible drug-drug interactions using OCR, fuzzy matching, and a domain-specific interaction database.

---

## 📸 Overview

Doctors often write prescriptions by hand, which can be difficult to read and interpret. This tool helps identify potential drug-drug interactions directly from images of handwritten notes or prescriptions.

It uses OCR to extract drug names, corrects errors using spell-check and fuzzy matching, and then checks for known interactions from a trusted database.


---

## 🛠️ Tech Stack

- **Python** – Core logic and data processing  
- **Streamlit** – Lightweight and interactive web interface  
- **Google Cloud Vision API** – OCR for handwritten text  
- **FuzzyWuzzy** – Approximate matching of misspelled drug names  
- **PySpellChecker** – Spell correction for drug names  
- **Pandas** – Data handling and analysis  
- **Custom Drug Interaction Dataset** – Domain-specific database of drug interactions

---

## 🧠 How It Works

1. 📷 **Upload** an image of a handwritten prescription.
2. 🔍 **Text Extraction** using Google Vision OCR.
3. 🧾 **Text Preprocessing** to clean and split drug names.
4. 🧠 **Spell Check & Fuzzy Matching** to match misspelled or unclear drug names.
5. 💊 **Interaction Checking** from a CSV drug interaction dataset.
6. 📋 **Output**:
   - Extracted and matched drug names (side-by-side).
   - Identified drug interactions (listed below).

---
