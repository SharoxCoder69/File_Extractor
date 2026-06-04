import streamlit as st
import pandas as pd
import re
from rapidfuzz import fuzz

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Intelligence Dashboard",
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

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# ---------------- LOGIN PAGE ----------------
def login_page():

    st.markdown("""
    <style>
    .login-title{
        text-align:center;
        font-size:40px;
        font-weight:800;
        color:#00ffcc;
        margin-bottom:30px;
        text-shadow:0 0 20px #00ffcc;
    }

    .stApp{
        background: radial-gradient(circle at top,#0f172a,#020617);
    }

    div[data-testid="stTextInput"] input{
        border-radius:12px;
        padding:10px;
    }

    div.stButton > button {
        width:100%;
        background: linear-gradient(90deg,#00ffcc,#2563eb);
        color:black;
        font-weight:bold;
        border-radius:12px;
        padding:10px;
        transition:0.3s;
    }

    div.stButton > button:hover{
        transform:scale(1.03);
        box-shadow:0 0 20px #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-title'>🔐 TWG Login Portal</div>", unsafe_allow_html=True)

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u] == p:
            st.session_state.logged_in = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

if not st.session_state.logged_in:
    login_page()

# ---------------- LOGOUT ----------------
st.sidebar.markdown(f"👤 **User:** {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

# ---------------- MAIN UI STYLE ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top,#0b1220,#050814);
    color:white;
}

/* Title */
.main-title{
    text-align:center;
    font-size:38px;
    font-weight:800;
    color:#00ffcc;
    text-shadow:0 0 20px #00ffcc;
    margin-bottom:10px;
}

/* Card effect */
.block-container{
    padding-top:2rem;
}

/* Textarea */
textarea{
    border-radius:14px !important;
    border:1px solid #00ffcc !important;
    background: rgba(255,255,255,0.03) !important;
    color:white !important;
}

/* Button */
div.stButton > button{
    background: linear-gradient(90deg,#00ffcc,#3b82f6);
    color:black;
    font-weight:bold;
    border-radius:12px;
    padding:10px;
    transition:0.3s;
}

div.stButton > button:hover{
    transform:scale(1.05);
    box-shadow:0 0 25px #00ffcc;
}

/* Metrics cards */
div[data-testid="metric-container"]{
    background: rgba(255,255,255,0.05);
    border-radius:16px;
    padding:15px;
    box-shadow:0 0 15px rgba(0,255,204,0.15);
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='main-title'>📊 TWG Intelligence Dashboard</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
raw_data = st.text_area("📥 Paste Raw Data Here", height=250)

# ---------------- CLEAN ----------------
def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# ---------------- MATCH ----------------
def best_match(store_name, raw_dict):

    best_score = 0
    best_time = ""

    s = normalize(store_name)

    for r, t in raw_dict.items():

        score = fuzz.partial_ratio(s, normalize(r))

        if score > best_score and score >= 70:
            best_score = score
            best_time = t

    return best_time

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not raw_data:
        st.warning("Please paste raw data")
        st.stop()

    lines = raw_data.splitlines()

    extracted = {}
    current = None

    time_pattern = r'^\d{1,2}:\d{2}\s?(AM|PM|am|pm)?$'

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if re.match(time_pattern, line):
            if current:
                extracted[current] = line
            continue

        current = line

    results = []

    for store, sid in STORE_MAP.items():

        time_value = best_match(store, extracted)

        results.append({
            "Store Name": store,
            "Store ID": sid,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    col1, col2 = st.columns(2)
    col1.metric("Total Stores", len(df))
    col2.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode(),
        "twg_report.csv",
        "text/csv"
    )
