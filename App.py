import streamlit as st
import pandas as pd
import re
from rapidfuzz import fuzz

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Control Center",
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
    "HICKORY": "TWGNC52",
    "MOORESVILLE": "TWGNC53",
    "CANNON": "TWGNC50",
    "SALISBURY NC T17": "TWGNC17",
    "GREENSBORO NC T7": "TWGNC07",
    "LEXINGTON NC T9": "TWGNC09",
    "ASHEBORO NC T10": "TWGNC10"
}

# ---------------- LOGIN STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# ---------------- LOGIN ----------------
def login():
    st.markdown("""
    <style>
    .login-box{
        width: 420px;
        margin: auto;
        padding: 30px;
        background: rgba(255,255,255,0.06);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 40px rgba(0,255,200,0.2);
        text-align:center;
    }

    .title{
        font-size:32px;
        font-weight:800;
        color:#00ffcc;
        margin-bottom:20px;
    }

    div.stButton > button {
        width:100%;
        background: linear-gradient(90deg,#00ffcc,#3b82f6);
        color:black;
        font-weight:bold;
        border-radius:12px;
        padding:10px;
    }

    .stApp{
        background: radial-gradient(circle at top,#050816,#020617);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-box'><div class='title'>TWG Login</div>", unsafe_allow_html=True)

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u] == p:
            st.session_state.logged_in = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Invalid login")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if not st.session_state.logged_in:
    login()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## ⚙ Control Panel")
    st.write(f"👤 {st.session_state.user}")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- FULL UI STYLE ----------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background: radial-gradient(circle at top,#0b1220,#020617);
    color: white;
}

/* Header */
.header {
    font-size: 40px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#00ffcc,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* Glass container */
.block {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 25px rgba(0,255,200,0.1);
}

/* Textarea */
textarea {
    border-radius: 14px !important;
    border: 1px solid #00ffcc !important;
}

/* Button */
div.stButton > button {
    background: linear-gradient(90deg,#00ffcc,#3b82f6);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00ffcc;
}

/* Metrics cards */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 0 15px rgba(0,255,200,0.15);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header'>📊 TWG CONTROL CENTER</div>", unsafe_allow_html=True)

# ---------------- INPUT CARD ----------------
st.markdown("<div class='block'>", unsafe_allow_html=True)
raw_data = st.text_area("📥 Paste Raw Data", height=250)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def normalize(x):
    return re.sub(r'[^a-z0-9]', '', x.lower())

def match(store, data):
    s = normalize(store)
    best = ""
    score_max = 0

    for r, t in data.items():
        score = fuzz.partial_ratio(s, normalize(r))
        if score > score_max and score >= 70:
            score_max = score
            best = t

    return best

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

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
        t = match(store, extracted)
        results.append({
            "Store": store,
            "ID": sid,
            "Time": t if t else "❌ Missing"
        })

    df = pd.DataFrame(results)

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Stores", len(df))
    col2.metric("Matched", len(df[df["Time"] != "❌ Missing"]))
    col3.metric("Missing", len(df[df["Time"] == "❌ Missing"]))

    st.markdown("### 📋 Results")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download Report",
        df.to_csv(index=False).encode(),
        "twg_report.csv",
        "text/csv"
    )
