import streamlit as st
import pandas as pd
import re
import time

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

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# ---------------- LOGIN ----------------
def login_page():
    st.markdown("## 🔐 Login Required")

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

if not st.session_state.logged_in:
    login_page()

# ---------------- LOGOUT ----------------
st.sidebar.write(f"👤 Logged in as: {st.session_state.user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

# ---------------- STYLE ----------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: #e5e7eb;
}

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

/* 3D INPUT */
textarea {
    border-radius: 14px !important;
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}

/* BUTTON */
.stButton > button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    color: white;
    font-weight: 700;
}

.stButton > button:hover {
    transform: scale(1.03);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(f"""
<div class="header">
    <div class="title">📊 Store Intelligence Dashboard</div>
    <div class="subtitle">Welcome {st.session_state.user}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- MASTER LIST (OLD STYLE TEXTBOX) ----------------
st.markdown("## 📌 Master Store List")

master_list = st.text_area("Enter Master Stores (one per line)", height=200)

# convert to list
master_lines = [m.strip() for m in master_list.splitlines() if m.strip()]

st.markdown("---")

# ---------------- RAW DATA ----------------
raw_data = st.text_area("📥 Raw Data", height=200)

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not master_lines or not raw_data:
        st.warning("Please fill both Master List and Raw Data")
        st.stop()

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.003)
        progress.progress(i + 1)

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

    for store in master_lines:
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

    st.metric("Total Stores", len(df))
    st.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "report.csv",
        "text/csv"
    )
