import streamlit as st
import pandas as pd
import re
import time

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Store Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: #e5e7eb;
}

/* HEADER */
.header {
    text-align: center;
    padding: 18px;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

.title {
    font-size: 32px;
    font-weight: 800;
}

.subtitle {
    font-size: 13px;
    color: #9ca3af;
}

/* TEXT AREA FIX (IMPORTANT) */
textarea {
    border-radius: 12px !important;
    background: rgba(255,255,255,0.04) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    min-height: 200px !important;
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
    box-shadow: 0 10px 25px rgba(37,99,235,0.25);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <div class="title">📊 Store Intelligence Dashboard</div>
    <div class="subtitle">TOTALLYWIRELESSGROUP • Smart Extraction System</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- SEARCH ----------------
c1, c2 = st.columns(2)

with c1:
    master_search = st.text_input("🔍 Search Master List")

with c2:
    raw_search = st.text_input("🔍 Search Raw Data")

st.markdown("## 📥 INPUT DATA")

# ---------------- INPUT BOXES (FIXED GUARANTEED VISIBLE) ----------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📌 Master Store List")
    master_list = st.text_area("Enter master stores here", height=250)

with col2:
    st.markdown("### 📥 Raw Data Logs")
    raw_data = st.text_area("Enter raw logs here", height=250)

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not master_list or not raw_data:
        st.warning("Please fill both Master List and Raw Data")
        st.stop()

    # loading
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

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Total", total)
    c2.metric("✅ Found", matched)
    c3.metric("❌ Missing", missing)
    c4.metric("📊 Success Rate", f"{int((matched/total)*100)}%")

    st.markdown("---")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Report",
        csv,
        "store_report.csv",
        "text/csv"
    )
