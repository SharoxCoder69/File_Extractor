import streamlit as st
import pandas as pd
import re
from rapidfuzz import fuzz

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Store Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- USERS ----------------
USERS = {
    "admin": "1234",
    "twg": "password",
    "manager": "admin123"
}

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
    "LUMBERTON NC": "TWGNC57"
}

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

def login():
    st.title("🔐 TWG Login Portal")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u] == p:
            st.session_state.logged_in = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Wrong credentials")

    st.stop()

if not st.session_state.logged_in:
    login()

# ---------------- LOGOUT ----------------
st.sidebar.write(f"👤 Logged in: {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

# ---------------- MODERN CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: white;
}

/* Title Glow */
h1 {
    color: #00ffcc;
    text-align: center;
    text-shadow: 0 0 15px #00ffcc;
}

/* Text area */
textarea {
    border-radius: 12px !important;
    border: 1px solid #00ffcc !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg,#00ffcc,#2563eb);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 20px;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00ffcc;
}

/* Metrics */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 0 10px rgba(0,255,204,0.2);
}

</style>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.title("📊 TWG Store Dashboard")

raw_data = st.text_area("📥 Raw Data", height=250)

# ---------------- CLEAN ----------------
def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# ---------------- FIXED FUZZY MATCH ----------------
def best_match(store_name, raw_dict):

    best_score = 0
    best_time = ""

    store_clean = normalize(store_name)

    for raw_store, t in raw_dict.items():

        raw_clean = normalize(raw_store)

        score = fuzz.partial_ratio(store_clean, raw_clean)

        if score > best_score and score >= 70:
            best_score = score
            best_time = t

    return best_time

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not raw_data:
        st.warning("Add raw data first")
        st.stop()

    lines = [l.strip() for l in raw_data.splitlines() if l.strip()]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    extracted = {}
    current = None

    for line in lines:

        if re.match(time_pattern, line):
            if current:
                extracted[current.upper()] = line
            continue

        current = line

    results = []

    for store_name, store_id in STORE_MAP.items():

        time_value = best_match(store_name, extracted)

        results.append({
            "Store Name": store_name,
            "Store ID": store_id,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    col1, col2 = st.columns(2)
    col1.metric("Total Stores", len(df))
    col2.metric("Matched Stores", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "twg_report.csv",
        "text/csv"
    )
