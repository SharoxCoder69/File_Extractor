import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Store System", layout="wide")

STORE_MAP = {
    "HICKORY": "TWGNC52",
    "MOORESVILLE": "TWGNC53",
    "CANNON": "TWGNC50",
    "SALISBURY NC T17": "TWGNC17"
}

# -------- CLEAN --------
def clean(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# -------- TIME CHECK --------
def is_time(line):
    return re.match(r'^\d{1,2}:\d{2}\s?(AM|PM|am|pm)?$', line.strip())

# -------- PARSER (FIXED) --------
def parse_raw(lines):

    extracted = {}
    current_store = None

    for line in lines:

        line = line.strip()

        # ignore noise
        if any(x in line.lower() for x in ["panel", "command", "armed", "disarmed"]):
            continue

        # store name detection (ONLY if NOT time)
        if not is_time(line):
            current_store = line
            continue

        # time line
        if is_time(line) and current_store:
            extracted[current_store] = line
            current_store = None   # 🔥 IMPORTANT FIX (prevents wrong carryover)

    return extracted

# -------- MATCH --------
def match(store, raw_dict):

    s = clean(store)

    for r, t in raw_dict.items():

        if s == clean(r):
            return t

        if s in clean(r) or clean(r) in s:
            return t

    return ""

# -------- UI --------
st.title("📊 Store Dashboard")

raw_data = st.text_area("Paste Raw Data", height=300)

if st.button("Generate"):

    lines = raw_data.splitlines()

    extracted = parse_raw(lines)

    results = []

    for store, sid in STORE_MAP.items():

        time_value = match(store, extracted)

        results.append({
            "Store": store,
            "Store ID": sid,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    st.metric("Total", len(df))
    st.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)
