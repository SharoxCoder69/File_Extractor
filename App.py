import streamlit as st
import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- STORE DATA ----------------
STORE_DATA = {
    "VICTORY DR GA T32": {"id": "TWGGA32", "dm": "-"},
    "MILGEN GA T34": {"id": "TWGGA34", "dm": "-"},
    "WOODRUFF GA T33": {"id": "TWGGA33", "dm": "-"},

    "W FRANKLIN T42": {"id": "TWGNC41", "dm": "Kindi"},
    "CHERRY T42": {"id": "TWGSC42", "dm": "Kindi"},
    "LANCASTER SC T29": {"id": "TWGSC29", "dm": "Kindi"},

    "CANNON": {"id": "TWGNC50", "dm": "Kindi"},
    "HICKORY": {"id": "TWGNC52", "dm": "Angie"},
    "HUNTERSVILLE": {"id": "TWGNC54", "dm": "Angie"},
    "LINCOLNTON NC T30": {"id": "TWGNC30", "dm": "Angie"},
    "MOORESVILLE": {"id": "TWGNC53", "dm": "Angie"},
    "MORGANTON": {"id": "TWGNC55", "dm": "Angie"},
    "ROXIE ST": {"id": "TWGNC51", "dm": "Angie"},
    "SALISBURY NC T17": {"id": "TWGNC17", "dm": "Angie"},

    "OWEN NC T36": {"id": "TWGNC36", "dm": "Ollivanza"},
    "BONANZA NC T37": {"id": "TWGNC37", "dm": "Ollivanza"},
    "BRAGG BLVD": {"id": "TWGNC56", "dm": "Ollivanza"},
    "LUMBERTON NC": {"id": "TWGNC57", "dm": "Ollivanza"},
    "GOOD MIDDLING": {"id": "TWGNC74", "dm": "Ollivanza"},
    "N EASTERN BLVD": {"id": "TWGNC75", "dm": "Ollivanza"},
    "6916 CLIFFDALE RD": {"id": "TWGNC76", "dm": "Ollivanza"},
    "NC FAY DUNN": {"id": "TWGNC77", "dm": "Ollivanza"},
    "3620 RAMSEY ST": {"id": "TWGNC78", "dm": "Ollivanza"},
    "5135 RAEFORD RD": {"id": "TWGNC79", "dm": "Ollivanza"},
    "NC LAURINBURG": {"id": "TWGNC80", "dm": "Ollivanza"},
}

# ---------------- CLEAN FUNCTION (MAIN FIX) ----------------
def clean_text(text):
    text = str(text).upper()
    text = re.sub(r'[^A-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------- SMART MATCH FUNCTION ----------------
def ai_match(raw_text):

    cleaned_input = clean_text(raw_text)

    for store in STORE_DATA.keys():

        cleaned_store = clean_text(store)

        # EXACT MATCH AFTER CLEANING
        if cleaned_store == cleaned_input:
            return store

    # PARTIAL MATCH (IMPORTANT FOR DIRTY RAW DATA)
    for store in STORE_DATA.keys():

        cleaned_store = clean_text(store)

        if cleaned_store in cleaned_input or cleaned_input in cleaned_store:
            return store

    return None

# ---------------- PARSER ----------------
def parse_raw(raw_text):
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    results = []
    i = 0

    while i < len(lines):
        line = lines[i]

        match = re.search(r'(.+?)\s+(\d{1,2}:\d{2}\s?(AM|PM|am|pm)?)', line)

        if match:
            results.append((match.group(1).strip(), match.group(2).strip()))
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
st.title("🤖 TWG AI SMART DASHBOARD")

raw_data = st.text_area("📥 Paste Raw Data", height=300)

if st.button("🚀 Generate Report"):

    parsed = parse_raw(raw_data)

    if not parsed:
        st.error("No data parsed")
        st.stop()

    results = []

    for raw_store, time in parsed:

        matched = ai_match(raw_store)

        if matched:
            sid = STORE_DATA[matched]["id"]
            dm = STORE_DATA[matched]["dm"]
        else:
            sid = ""
            dm = ""

        results.append({
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm,
            "Raw Store": raw_store,
            "Time": time
        })

    df = pd.DataFrame(results)

    st.metric("Total Records", len(df))
    st.metric("Matched Stores", len(df[df["Store Name"] != ""]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode(),
        "twg_ai_report.csv",
        "text/csv"
    )
