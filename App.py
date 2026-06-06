import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="TWG SmartOps 2-Step", layout="wide")

# ---------------- STORE DATABASE ----------------
STORE_DATA = {
    "HICKORY": {"id": "TWGNC52", "dm": "Angie"},
    "BRAGG BLVD": {"id": "TWGNC56", "dm": "Ollivanza"},
    "CANNON": {"id": "TWGNC50", "dm": "Kindi"},
    "MOORESVILLE": {"id": "TWGNC53", "dm": "Angie"},
    "ROXIE ST": {"id": "TWGNC51", "dm": "Angie"},
    "CHERRY T42": {"id": "TWGSC42", "dm": "Kindi"},
    "SALISBURY": {"id": "TWGNC17", "dm": "Angie"},
    "LINCOLNTON": {"id": "TWGNC30", "dm": "Kindi"},
    "GASTONIA": {"id": "TWGNC42", "dm": "Angie"},
    "BURLINGTON": {"id": "TWGNC13", "dm": "Ollivanza"},
}

# ---------------- CLEAN ----------------
def clean_text(text):
    text = str(text).upper()
    text = re.sub(r'\bNC\b|\bVA\b|\bGA\b|\bSC\b', ' ', text)
    text = re.sub(r'T\d+|\bSTORE\b|\bSHIFT\b', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[^A-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------- MATCH ----------------
def match_store(text):
    text = clean_text(text)

    best_match = "UNMATCHED"
    best_score = 0

    for store in STORE_DATA:
        s = clean_text(store)

        if s in text:
            return store

        score = len(set(text.split()) & set(s.split()))

        if score > best_score:
            best_score = score
            best_match = store

    if best_score >= 1:
        return best_match

    return "UNMATCHED"

# ---------------- UI ----------------
st.title("🚀 TWG SmartOps 2-Step System")

# ================= STEP 1 =================
st.markdown("## 🟢 STEP 1: Raw Data Cleaner")

raw_input = st.text_area("Paste RAW Data", height=200)

if st.button("Clean Data"):

    lines = [l.strip() for l in raw_input.splitlines() if l.strip()]
    cleaned = []

    for line in lines:
        cleaned.append(clean_text(line))

    cleaned_text = "\n".join(cleaned)

    st.success("Cleaned Successfully 🚀")

    st.text_area("COPY THIS CLEAN DATA", cleaned_text, height=200)

# ================= STEP 2 =================
st.markdown("## 🔵 STEP 2: Match Stores (DM + ID)")

final_input = st.text_area("Paste Cleaned Data Here", height=200)

if st.button("Run Matching System"):

    final = []

    for line in final_input.splitlines():
        line = line.strip()
        if not line:
            continue

        matched = match_store(line)

        if matched in STORE_DATA:
            sid = STORE_DATA[matched]["id"]
            dm = STORE_DATA[matched]["dm"]
        else:
            sid = ""
            dm = ""

        final.append({
            "Input": line,
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm
        })

    df = pd.DataFrame(final)

    st.success("Matching Completed 🚀")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "⬇ Download Result",
        csv,
        "twg_final.csv",
        "text/csv"
    )
