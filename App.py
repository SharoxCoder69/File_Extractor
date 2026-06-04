import streamlit as st
import pandas as pd
import re

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG SmartOps SaaS",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CSS STYLE ----------------
st.markdown(
    """
    <style>

    /* Background */
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    /* Main title */
    h1 {
        text-align: center;
        color: #38bdf8;
        font-weight: 800;
    }

    /* Sub headings */
    h3 {
        color: #e2e8f0;
        font-weight: 600;
    }

    /* Text area */
    textarea {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9, #3b82f6);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #3b82f6, #0ea5e9);
        transform: scale(1.02);
    }

    /* Dataframe */
    .dataframe {
        background-color: white;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 30px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOGIN ----------------
def login():
    st.markdown("<h1>🔐 TWG SmartOps Login</h1>", unsafe_allow_html=True)

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

# ---------------- MATCH ----------------
def match_store(text):
    text = clean_text(text)

    best = None
    best_score = 0

    for store in STORE_DATA:

        s = clean_text(store)

        if s in text or text in s:
            return store

        score = len(set(text.split()) & set(s.split()))

        if score > best_score:
            best_score = score
            best = store

    if best_score >= 1:
        return best

    return "UNMATCHED"

# ---------------- EXTRACT ----------------
def extract_store_time(raw):

    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    result = []
    i = 0

    while i < len(lines):

        line = lines[i]

        match = re.search(r'(.+?)\s+(\d{1,2}:\d{2}\s?(AM|PM|am|pm)?)', line)

        if match:
            result.append((match.group(1), match.group(2)))
            i += 1
            continue

        if i + 1 < len(lines):
            t = re.search(r'\d{1,2}:\d{2}', lines[i+1])

            if t:
                result.append((line, t.group()))
                i += 2
                continue

        i += 1

    return result

# ---------------- UI ----------------
st.markdown("<h1>🚀 TWG SmartOps SaaS Dashboard</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Raw Data Input")
    raw_data = st.text_area("", height=300)

with col2:
    st.markdown("### 📥 Manual Store Input")
    manual_data = st.text_area("", height=300)

# ---------------- PROCESS ----------------
if st.button("🚀 Run System"):

    final = []

    for store_raw, time in extract_store_time(raw_data):

        matched = match_store(store_raw)

        if matched in STORE_DATA:
            sid = STORE_DATA[matched]["id"]
            dm = STORE_DATA[matched]["dm"]
        else:
            sid = ""
            dm = ""

        final.append({
            "Source": "Raw",
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm,
            "Time": time
        })

    for line in manual_data.splitlines():

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
            "Source": "Manual",
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm,
            "Time": ""
        })

    df = pd.DataFrame(final)

    st.success("Processing Completed 🚀")

    st.metric("Total Records", len(df))

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "⬇ Download Report",
        csv,
        "twg_report.csv",
        "text/csv"
    )

    st.subheader("📋 Copy Data")

    st.text_area("Copy from here", df.to_csv(index=False), height=200)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div class='footer'>
        Created by <b>Noor Ul Ain</b> <br>
        Managed by <b>Sharox Javaid</b>
    </div>
    """,
    unsafe_allow_html=True
)
