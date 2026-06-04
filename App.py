import streamlit as st
import pandas as pd
import re
import time
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Store Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

FILE_PATH = "master_list.csv"

# ---------------- LOAD MASTER LIST ----------------
if "master_list" not in st.session_state:
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        st.session_state.master_list = df["store"].tolist()
    else:
        st.session_state.master_list = []

# ---------------- SAVE MASTER LIST ----------------
def save_master():
    df = pd.DataFrame({"store": st.session_state.master_list})
    df.to_csv(FILE_PATH, index=False)

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

/* INPUT BOX 3D STYLE */
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
    box-shadow: 0 18px 40px rgba(0,0,0,0.6);
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

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <div class="title">📊 Store Intelligence Dashboard</div>
    <div class="subtitle">TOTALLYWIRELESSGROUP • Persistent Smart System</div>
</div>
""", unsafe_allow_html=True)

# ---------------- MASTER LIST MANAGEMENT ----------------
st.markdown("## 📌 Master List Manager")

new_store = st.text_input("➕ Add New Store")

col1, col2 = st.columns(2)

with col1:
    if st.button("Add Store"):
        if new_store:
            st.session_state.master_list.append(new_store)
            save_master()
            st.success("Store Added & Saved!")

with col2:
    if st.button("🗑 Clear All Stores"):
        st.session_state.master_list = []
        save_master()
        st.warning("Master List Cleared!")

# ---------------- SHOW MASTER LIST ----------------
st.markdown("### 📋 Saved Master List")

for i, s in enumerate(st.session_state.master_list):
    st.write(f"{i+1}. {s}")

st.markdown("---")

# ---------------- RAW DATA ----------------
raw_data = st.text_area("📥 Raw Data Input", height=200)

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not st.session_state.master_list or not raw_data:
        st.warning("Master list or raw data missing")
        st.stop()

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.003)
        progress.progress(i + 1)

    master_lines = st.session_state.master_list
    raw_lines = [r.strip() for r in raw_data.splitlines() if r.strip()]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    extracted = {}
    current_store = None

    for line in raw_lines:

        if re.match(time_pattern, line):
            if current_store:
                extracted[current_store.upper()] = line
            continue

        current_store = line

    results = []

    for store in master_lines:

        time_value = ""

        for raw_store, t in extracted.items():
            if raw_store.lower() in store.lower():
                time_value = t
                break

        results.append({
            "Store": store,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    # ---------------- STATS ----------------
    total = len(df)
    matched = len(df[df["Time"] != "❌ Missing"])
    missing = total - matched

    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Total", total)
    c2.metric("✅ Matched", matched)
    c3.metric("❌ Missing", missing)

    st.markdown("---")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Report",
        csv,
        "store_report.csv",
        "text/csv"
    )
