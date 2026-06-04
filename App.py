import streamlit as st
import pandas as pd
import re
import time
import os

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Store Intelligence System",
    page_icon="📊",
    layout="wide"
)

# ---------------- USERS ----------------
USERS = {
    "admin": "1234",
    "twg": "password",
    "manager": "admin123"
}

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

if "master_list" not in st.session_state:
    st.session_state.master_list = []

FILE_PATH = "master_list.csv"

# ---------------- LOAD MASTER ----------------
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
    st.session_state.master_list = df["store"].tolist()

# ---------------- SAVE MASTER ----------------
def save_master():
    pd.DataFrame({"store": st.session_state.master_list}).to_csv(FILE_PATH, index=False)

# ---------------- LOGIN PAGE ----------------
def login_page():

    st.markdown("""
    <div style='text-align:center; padding:20px'>
        <h1>🔐 Store Intelligence Login</h1>
        <p style='color:gray'>Please login to continue</p>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ---------------- IF NOT LOGGED IN ----------------
if not st.session_state.logged_in:
    login_page()

# ---------------- LOGOUT ----------------
st.sidebar.write(f"👤 Logged in as: {st.session_state.user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

# ---------------- MODERN UI ----------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: #e5e7eb;
}

/* HEADER */
.header {
    text-align: center;
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

.title {
    font-size: 34px;
    font-weight: 800;
}

.subtitle {
    font-size: 13px;
    color: #9ca3af;
}

/* INPUT 4D */
textarea {
    border-radius: 14px !important;
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    transition: 0.3s;
}

textarea:hover {
    transform: translateY(-3px);
}

/* BUTTON */
.stButton > button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    color: white;
    font-weight: 700;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 15px 35px rgba(37,99,235,0.4);
}

/* METRICS */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(f"""
<div class="header">
    <div class="title">📊 Store Intelligence Dashboard</div>
    <div class="subtitle">Welcome {st.session_state.user} • Secure System</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- ADD MASTER STORE ----------------
st.markdown("## 📌 Master List Manager")

new_store = st.text_input("➕ Add Store")

col1, col2 = st.columns(2)

with col1:
    if st.button("Add Store"):
        if new_store:
            st.session_state.master_list.append(new_store)
            save_master()
            st.success("Added & Saved!")

with col2:
    if st.button("🗑 Clear All"):
        st.session_state.master_list = []
        save_master()
        st.warning("Cleared!")

st.markdown("### 📋 Master List")

for i, s in enumerate(st.session_state.master_list):
    st.write(f"{i+1}. {s}")

st.markdown("---")

# ---------------- RAW DATA ----------------
raw_data = st.text_area("📥 Raw Data", height=200)

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not st.session_state.master_list or not raw_data:
        st.warning("Missing Data")
        st.stop()

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.003)
        progress.progress(i + 1)

    master = st.session_state.master_list
    raw_lines = [r.strip() for r in raw_data.splitlines() if r.strip()]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'
    extracted = {}
    current = None

    for line in raw_lines:
        if re.match(time_pattern, line):
            if current:
                extracted[current.upper()] = line
            continue
        current = line

    results = []

    for store in master:
        tval = ""

        for raw_store, t in extracted.items():
            if raw_store.lower() in store.lower():
                tval = t
                break

        results.append({
            "Store": store,
            "Time": tval if tval else "❌ Missing"
        })

    df = pd.DataFrame(results)

    st.metric("Total", len(df))
    st.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "report.csv",
        "text/csv"
    )
