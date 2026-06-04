import streamlit as st
import pandas as pd
import re
from rapidfuzz import fuzz

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Store Intelligence Pro",
    page_icon="📊",
    layout="wide"
)

# ---------------- STORE MAP ----------------
STORE_MAP = {
    "VICTORY DR GA T32": "TWGGA32",
    "MILGEN GA T34": "TWGGA34",
    "WOODRUFF GA T33": "TWGGA33",
    "W FRANKLIN T42": "TWGNC41",
    "CHERRY T42": "TWGSC42",
    "LANCASTER SC T29": "TWGSC29",
    "CANNON": "TWGNC50",
    "HICKORY": "TWGNC52",
    "HUNTERSVILLE": "TWGNC54",
    "LINCOLNTON NC T30": "TWGNC30",
    "MOORESVILLE": "TWGNC53",
    "MORGANTON": "TWGNC55",
    "ROXIE ST": "TWGNC51",
    "SALISBURY NC T17": "TWGNC17",
    "OWEN NC T36": "TWGNC36",
    "BONANZA NC T37": "TWGNC37",
    "HOPE MILLS T39": "TWGNC39",
    "BRAGG BLVD": "TWGNC56",
    "LUMBERTON NC": "TWGNC57",
    "GOOD MIDDLING": "TWGNC74",
    "N EASTERN BLVD": "TWGNC75",
    "6916 CLIFFDALE RD": "TWGNC76",
    "NC FAY DUNN": "TWGNC77",
    "3620 RAMSEY ST": "TWGNC78",
    "5135 RAEFORD RD": "TWGNC79",
    "NC LAURINBURG": "TWGNC80"
}

# ---------------- CLEAN FUNCTION ----------------
def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# ---------------- SMART MATCH ENGINE ----------------
def best_match(store_name, raw_dict):

    best_score = 0
    best_time = ""

    store_clean = normalize(store_name)

    for raw_store, t in raw_dict.items():

        raw_clean = normalize(raw_store)

        # dual scoring system
        score1 = fuzz.partial_ratio(store_clean, raw_clean)
        score2 = fuzz.token_sort_ratio(store_clean, raw_clean)

        score = max(score1, score2)

        if score > best_score and score >= 80:
            best_score = score
            best_time = t

    return best_time

# ---------------- UI ----------------
st.title("📊 TWG Store Intelligence Pro Dashboard")

raw_data = st.text_area("📥 Paste Raw Data", height=250)

# ---------------- PARSER ----------------
time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

def parse_raw(lines):

    extracted = {}
    current = None

    for line in lines:

        if re.match(time_pattern, line):
            if current:
                extracted[current.upper()] = line
            continue

        current = line

    return extracted

# ---------------- RUN ----------------
if st.button("🚀 Generate Report"):

    if not raw_data:
        st.warning("Please add raw data")
        st.stop()

    lines = [l.strip() for l in raw_data.splitlines() if l.strip()]

    extracted = parse_raw(lines)

    results = []

    for store_name, store_id in STORE_MAP.items():

        time_value = best_match(store_name, extracted)

        results.append({
            "Store Name": store_name,
            "Store ID": store_id,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    st.metric("Total Stores", len(df))
    st.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "twg_report.csv",
        "text/csv"
    )
