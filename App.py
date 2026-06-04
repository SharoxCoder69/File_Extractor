import streamlit as st
import pandas as pd
import re

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Data Pipeline",
    page_icon="📊",
    layout="wide"
)

# ---------------- STORE DATA ----------------
STORE_DATA = {

    "HICKORY": {"id": "TWGNC52", "dm": "Angie"},
    "BRAGG BLVD": {"id": "TWGNC56", "dm": "Ollivanza"},
    "CANNON": {"id": "TWGNC50", "dm": "Kindi"},
    "MOORESVILLE": {"id": "TWGNC53", "dm": "Angie"},
    "ROXIE ST": {"id": "TWGNC51", "dm": "Angie"},
    "CHERRY T42": {"id": "TWGSC42", "dm": "Kindi"},
}

# ---------------- CLEAN ----------------
def clean_text(text):
    text = str(text).upper()
    text = re.sub(r'[^A-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------- MATCH FUNCTION ----------------
def ai_match(text):

    cleaned_input = clean_text(text)

    best_match = None
    best_score = 0

    for store in STORE_DATA:

        cleaned_store = clean_text(store)

        if cleaned_store in cleaned_input or cleaned_input in cleaned_store:
            return store

        common = len(set(cleaned_input.split()) & set(cleaned_store.split()))

        if common > best_score:
            best_score = common
            best_match = store

    if best_score >= 1:
        return best_match

    return "UNMATCHED"

# ---------------- EXTRACT FUNCTION ----------------
def extract_store_time(raw_text):

    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    results = []
    i = 0

    while i < len(lines):

        line = lines[i]

        match = re.search(r'(.+?)\s+(\d{1,2}:\d{2}\s?(AM|PM|am|pm)?)', line)

        if match:
            results.append((match.group(1), match.group(2)))
            i += 1
            continue

        if i + 1 < len(lines):
            time_match = re.search(r'\d{1,2}:\d{2}', lines[i+1])

            if time_match:
                results.append((line, time_match.group()))
                i += 2
                continue

        i += 1

    return results

# ---------------- UI ----------------
st.title("🤖 TWG DATA PIPELINE SYSTEM")

col1, col2 = st.columns(2)

# ---------------- COLUMN 1 ----------------
with col1:
    st.subheader("📥 Raw Data Input")

    raw_data = st.text_area("Paste Raw Data", height=250)

# ---------------- COLUMN 2 (NEW INPUT BOX) ----------------
with col2:
    st.subheader("📥 Manual Store List (NEW)")

    manual_data = st.text_area("Paste Store Names Only", height=250)

# ---------------- PROCESS ----------------
if st.button("🚀 Process Both Inputs"):

    final = []

    # =========================
    # 1. RAW DATA PROCESSING
    # =========================
    extracted = extract_store_time(raw_data)

    for store_raw, time in extracted:

        matched = ai_match(store_raw)

        if matched in STORE_DATA:
            sid = STORE_DATA[matched]["id"]
            dm = STORE_DATA[matched]["dm"]
        else:
            sid = ""
            dm = ""

        final.append({
            "Source": "Raw Data",
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm,
            "Time": time
        })

    # =========================
    # 2. MANUAL DATA PROCESSING
    # =========================
    if manual_data:

        manual_lines = [l.strip() for l in manual_data.splitlines() if l.strip()]

        for line in manual_lines:

            matched = ai_match(line)

            if matched in STORE_DATA:
                sid = STORE_DATA[matched]["id"]
                dm = STORE_DATA[matched]["dm"]
            else:
                sid = ""
                dm = ""

            final.append({
                "Source": "Manual Input",
                "Store Name": matched,
                "Store ID": sid,
                "DM": dm,
                "Time": "",
            })

    # ---------------- OUTPUT ----------------
    df = pd.DataFrame(final)

    df = df.sort_values(by=["Store Name"])

    st.metric("Total Records", len(df))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode(),
        "twg_dual_pipeline.csv",
        "text/csv"
    )
