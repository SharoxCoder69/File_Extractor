import streamlit as st
import pandas as pd
import re
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Store Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- PREMIUM UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: #e5e7eb;
}

/* Top Header Card */
.header {
    background: linear-gradient(135deg, rgba(37,99,235,0.15), rgba(6,182,212,0.08));
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Title */
.title {
    font-size: 32px;
    font-weight: 800;
    color: #e5e7eb;
}

/* Subtitle */
.subtitle {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 5px;
}

/* INPUT BOXES */
textarea {
    border-radius: 12px !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: white !important;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    font-weight: 700;
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px rgba(37,99,235,0.25);
}

/* METRICS CARDS */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 16px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* SECTION BOX */
.box {
    background: rgba(255,255,255,0.03);
    padding: 15px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER CARD ----------------
st.markdown("""
<div class="header">
    <div class="title">📊 Store Intelligence Dashboard</div>
    <div class="subtitle">TOTALLYWIRELESSGROUP • Advanced Analytics System</div>
</div>
""", unsafe_allow_html=True)

# ---------------- STATS PLACEHOLDER ----------------
st.markdown("### 📌 Quick Controls")

colA, colB = st.columns(2)

with colA:
    master_search = st.text_input("🔍 Search Master List")

with colB:
    raw_search = st.text_input("🔍 Search Raw Data")

st.markdown("---")

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📌 Master Store List")
    master_list = st.text_area("", height=220)

with col2:
    st.markdown("### 📥 Raw Data Logs")
    raw_data = st.text_area("", height=220)

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not master_list or not raw_data:
        st.warning("Please fill both inputs")
        st.stop()

    # loading animation
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.003)
        progress.progress(i + 1)

    # ---------------- CLEAN ----------------
    master_lines = [m.strip() for m in master_list.splitlines() if m.strip()]
    raw_lines = [r.strip() for r in raw_data.splitlines() if r.strip()]

    if master_search:
        master_lines = [m for m in master_lines if master_search.lower() in m.lower()]

    if raw_search:
        raw_lines = [r for r in raw_lines if raw_search.lower() in r.lower()]

    # ---------------- LOGIC ----------------
    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'
    ignore_words = ["Panel", "Partition", "Disarmed", "Armed", "[Mobile]", "Command:"]

    extracted = {}
    current_store = None

    for line in raw_lines:

        if any(w.lower() in line.lower() for w in ignore_words):
            continue

        if re.match(time_pattern, line):
            if current_store:
                extracted[current_store.upper()] = line
            continue

        current_store = line

    # ---------------- MATCH ----------------
    results = []

    for store in master_lines:

        time_value = ""

        for raw_store, t in extracted.items():
            words = raw_store.replace(".", "").split()

            if any(w.upper() in store.upper() for w in words if len(w) > 2):
                time_value = t
                break

        results.append({
            "Store Name": store,
            "Status": "✅ Found" if time_value else "❌ Missing",
            "Time": time_value if time_value else "-"
        })

    df = pd.DataFrame(results)

    # ---------------- STATS ----------------
    total = len(df)
    matched = len(df[df["Status"] == "✅ Found"])
    missing = total - matched
    rate = int((matched / total) * 100) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Total", total)
    c2.metric("✅ Found", matched)
    c3.metric("❌ Missing", missing)
    c4.metric("📊 Success Rate", f"{rate}%")

    st.markdown("---")

    # ---------------- TABLE ----------------
    st.dataframe(df, use_container_width=True)

    # ---------------- DOWNLOAD ----------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Report",
        csv,
        "store_report.csv",
        "text/csv"
    )
