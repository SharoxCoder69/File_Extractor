import streamlit as st
import pandas as pd
import re

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Store Intelligence System",
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

# ---------------- CLEAN TEXT ----------------
def clean(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# ---------------- PARSER ----------------
def parse_raw(lines):

    extracted = {}
    current_store = None

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    ignore_words = [
        "panel", "command", "armed", "disarmed",
        "mobile", "partition"
    ]

    for line in lines:

        line = line.strip()

        if any(w in line.lower() for w in ignore_words):
            continue

        if re.match(time_pattern, line):
            if current_store:
                extracted[current_store] = line
            continue

        current_store = line

    return extracted

# ---------------- SIMPLE MATCH (NO OVER ENGINEERING) ----------------
def match_store(store_name, raw_dict):

    store_clean = clean(store_name)

    for raw_store, time in raw_dict.items():

        raw_clean = clean(raw_store)

        # strict but flexible match
        if store_clean == raw_clean:
            return time

        if store_clean in raw_clean or raw_clean in store_clean:
            return time

    return ""

# ---------------- UI ----------------
st.title("📊 Store Intelligence System")

raw_data = st.text_area("📥 Paste Raw Data", height=300)

# ---------------- RUN ----------------
if st.button("Generate Report"):

    if not raw_data:
        st.warning("Please add raw data")
        st.stop()

    lines = raw_data.splitlines()

    extracted = parse_raw(lines)

    results = []

    for store_name, store_id in STORE_MAP.items():

        time_value = match_store(store_name, extracted)

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
        "store_report.csv",
        "text/csv"
    )
