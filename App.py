import streamlit as st
import pandas as pd
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TWG SmartOps SaaS",
    page_icon="🚀",
    layout="wide"
)

# ---------------- SIMPLE LOGIN (DEMO) ----------------
def login():
    st.title("🔐 TWG SmartOps Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user and pwd:
            st.session_state["logged_in"] = True
        else:
            st.error("Enter credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------- STORE DATABASE ----------------
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

# ---------------- MATCH ENGINE ----------------
def match_store(text):
    text = clean_text(text)

    best = None
    score_max = 0

    for store in STORE_DATA:
        s = clean_text(store)

        if s in text or text in s:
            return store

        score = len(set(text.split()) & set(s.split()))

        if score > score_max:
            score_max = score
            best = store

    if score_max >= 1:
        return best

    return "UNMATCHED"

# ---------------- PARSER ----------------
def extract(raw):
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    out = []
    i = 0

    while i < len(lines):

        line = lines[i]

        m = re.search(r'(.+?)\s+(\d{1,2}:\d{2}\s?(AM|PM|am|pm)?)', line)

        if m:
            out.append((m.group(1), m.group(2)))
            i += 1
            continue

        if i + 1 < len(lines):
            t = re.search(r'\d{1,2}:\d{2}', lines[i+1])

            if t:
                out.append((line, t.group()))
                i += 2
                continue

        i += 1

    return out

# ---------------- UI ----------------
st.title("🚀 TWG SmartOps SaaS Dashboard")

st.markdown("### 📊 Data Processing System")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Raw Data")
    raw_data = st.text_area("Paste raw data", height=300)

with col2:
    st.subheader("📥 Manual Store Input")
    manual = st.text_area("Paste store names", height=300)

# ---------------- PROCESS ----------------
if st.button("🚀 Run System"):

    final = []

    # RAW
    for store_raw, time in extract(raw_data):

        m = match_store(store_raw)

        if m in STORE_DATA:
            sid = STORE_DATA[m]["id"]
            dm = STORE_DATA[m]["dm"]
        else:
            sid = ""
            dm = ""

        final.append({
            "Source": "Raw",
            "Store": m,
            "Store ID": sid,
            "DM": dm,
            "Time": time
        })

    # MANUAL
    for line in manual.splitlines():

        line = line.strip()
        if not line:
            continue

        m = match_store(line)

        if m in STORE_DATA:
            sid = STORE_DATA[m]["id"]
            dm = STORE_DATA[m]["dm"]
        else:
            sid = ""
            dm = ""

        final.append({
            "Source": "Manual",
            "Store": m,
            "Store ID": sid,
            "DM": dm,
            "Time": ""
        })

    df = pd.DataFrame(final)

    st.success("Processing Complete 🚀")

    st.metric("Total Records", len(df))

    st.dataframe(df, use_container_width=True)

    # ---------------- DOWNLOAD ----------------
    csv = df.to_csv(index=False).encode()

    st.download_button(
        "⬇ Download Report",
        csv,
        "twg_report.csv",
        "text/csv"
    )

    # ---------------- COPY ----------------
    st.subheader("📋 Copy Data")

    st.text_area("Copy from here", df.to_csv(index=False), height=200)
