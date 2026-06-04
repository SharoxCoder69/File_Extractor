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

# =========================================================
# 🎨 LOGIN PAGE (MODERN CARD UI)
# =========================================================
def login_page():

    st.markdown("""
    <style>
    .login-box {
        width: 380px;
        margin: auto;
        margin-top: 100px;
        padding: 30px;
        border-radius: 18px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 0 40px rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
        text-align: center;
    }

    .login-title {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .login-sub {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-box">
        <div class="login-title">🔐 Store Intelligence</div>
        <div class="login-sub">Login to access dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        login_btn = st.button("🚀 Login")

    with col2:
        st.button("ℹ Info")

    if login_btn:
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")

    st.stop()

# ---------------- SHOW LOGIN IF NOT LOGGED IN ----------------
if not st.session_state.logged_in:
    login_page()

# =========================================================
# 🚪 LOGOUT (VISIBLE + CLEAN)
# =========================================================
st.sidebar.markdown(f"### 👤 {st.session_state.user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

st.markdown(
    f"""
    <div style="
        position: fixed;
        top: 10px;
        right: 20px;
        background: rgba(255,255,255,0.05);
        padding: 8px 14px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        color: #fff;
        font-size: 13px;
    ">
        👤 Logged in as: <b>{st.session_state.user}</b>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 🎨 MAIN UI
# =========================================================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: #e5e7eb;
}

/* INPUT */
textarea {
    border-radius: 14px !important;
    background: rgba(255,255,255,0.04) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
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
st.title("📊 Store Intelligence Dashboard")
st.markdown(f"Welcome **{st.session_state.user}** 👋")

st.markdown("---")

# ---------------- INPUTS ----------------
master_list = st.text_area("📌 Master Store List", height=200)
raw_data = st.text_area("📥 Raw Data", height=200)

master_lines = [m.strip() for m in master_list.splitlines() if m.strip()]

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not master_lines or not raw_data:
        st.warning("Missing data")
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
