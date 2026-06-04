import streamlit as st
import pandas as pd
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Store Time System",
    page_icon="📊",
    layout="wide"
)

# ---------------- STORE MAP ----------------
STORE_MAP = {
    "HICKORY": "TWGNC52",
    "MOORESVILLE": "TWGNC53",
    "CANNON": "TWGNC50",
    "SALISBURY NC T17": "TWGNC17",
    "LINCOLNTON NC T30": "TWGNC30",
    "ROXIE ST": "TWGNC51",
    "ASHEBORO NC T10": "TWGNC10",
    "GREENSBORO NC T7": "TWGNC07",
    "LEXINGTON NC T9": "TWGNC09"
}

# ---------------- CLEAN FUNCTION ----------------
def clean(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# ---------------- TIME CHECK ----------------
def is_time(line):
    return bool(re.match(r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?$', line.strip()))

# ---------------- SAFE PARSER (FIXED BUG) ----------------
def parse_raw(lines):

    extracted = {}
    current_store = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # ignore noise
        if any(x in line.lower() for x in ["panel", "command", "armed", "disarmed", "mobile"]):
            continue

        # if time line
        if is_time(line):
            if current_store:
                extracted[current_store] = line
                current_store = None   # 🔥 CRITICAL FIX (no carryover bug)
            continue

        # store line
        current_store = line

    return extracted

# ---------------- MATCH FUNCTION (SAFE) ----------------
def match_store(store_name, raw_dict):

    store_clean = clean(store_name)

    for raw_store, time in raw_dict.items():

        raw_clean = clean(raw_store)

        # exact match
        if store_clean == raw_clean:
            return time

        # partial safe match
        if store_clean in raw_clean or raw_clean in store_clean:
            return time

    return ""

# ---------------- UI ----------------
st.title("📊 Store Time Dashboard (Stable Version)")

raw_data = st.text_area("📥 Paste Raw Data", height=300)

# ---------------- RUN ----------------
if st.button("🚀 Generate Report"):

    if not raw_data:
        st.warning("Please paste raw data")
        st.stop()

    lines = raw_data.splitlines()

    extracted = parse_raw(lines)

    results = []

    for store, store_id in STORE_MAP.items():

        time_value = match_store(store, extracted)

        results.append({
            "Store Name": store,
            "Store ID": store_id,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    st.metric("Total Stores", len(df))
    st.metric("Matched Stores", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "store_report.csv",
        "text/csv"
    )
