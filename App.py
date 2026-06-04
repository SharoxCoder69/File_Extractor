import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Store Dashboard", layout="wide")

# ---------------- STORE LIST ----------------
STORE_MAP = {
    "HICKORY": "TWGNC52",
    "MOORESVILLE": "TWGNC53",
    "CANNON": "TWGNC50",
    "SALISBURY NC T17": "TWGNC17",
    "LINCOLNTON NC T30": "TWGNC30",
    "ROXIE ST": "TWGNC51",
    "GREENSBORO NC T7": "TWGNC07",
    "LEXINGTON NC T9": "TWGNC09",
    "ASHEBORO NC T10": "TWGNC10"
}

# ---------------- CLEAN ----------------
def clean(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

# ---------------- TIME CHECK ----------------
def is_time(line):
    return bool(re.match(r'^\d{1,2}:\d{2}\s?(am|pm|AM|PM)?$', line.strip()))

# ---------------- PARSER ----------------
def parse_raw(lines):
    extracted = {}
    current = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if is_time(line):
            if current:
                extracted[current] = line
                current = None
            continue

        current = line

    return extracted

# ---------------- MATCH ----------------
def match(store, data):
    s = clean(store)

    for r, t in data.items():
        if s == clean(r):
            return t
        if s in clean(r) or clean(r) in s:
            return t

    return ""

# ---------------- UI ----------------
st.title("📊 Store Dashboard (RUN NOW VERSION)")

raw_data = st.text_area("Paste Raw Data", height=300)

if st.button("Generate"):

    lines = raw_data.splitlines()
    extracted = parse_raw(lines)

    results = []

    for store, sid in STORE_MAP.items():

        time_value = match(store, extracted)

        results.append({
            "Store Name": store,
            "Store ID": sid,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    st.metric("Total Stores", len(df))
    st.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False).encode(),
        "report.csv",
        "text/csv"
    )
