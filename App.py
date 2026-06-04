import streamlit as st
import pandas as pd
import re
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Store Time Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- MODERN UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0b1220, #0f172a);
    color: #e5e7eb;
}

/* Title */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #e5e7eb;
    margin-top: 10px;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    margin-bottom: 15px;
}

/* Inputs */
textarea {
    border-radius: 10px !important;
    background: rgba(255,255,255,0.04) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* Button */
.stButton > button {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    color: white;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 20px rgba(37,99,235,0.25);
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    padding: 12px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* Table */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title">Store Time Dashboard</div>
<div class="subtitle">TOTALLYWIRELESSGROUP • Smart Extraction System</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- SEARCH BOXES ----------------
s1, s2 = st.columns(2)

with s1:
    master_search = st.text_input("🔍 Search Master List")

with s2:
    raw_search = st.text_input("🔍 Search Raw Data")

# ---------------- INPUT BOXES (SMALL) ----------------
col1, col2 = st.columns([1, 1])

with col1:
    master_list = st.text_area("📌 Master Store List", height=180)

with col2:
    raw_data = st.text_area("📥 Raw Data", height=180)

# ---------------- PROCESS ----------------
if st.button("🚀 Process Data"):

    if not master_list or not raw_data:
        st.warning("Please fill both inputs")
        st.stop()

    # Progress bar
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress.progress(i + 1)

    # ---------------- CLEAN INPUT ----------------
    master_lines = [m.strip() for m in master_list.splitlines() if m.strip()]
    raw_lines = [r.strip() for r in raw_data.splitlines() if r.strip()]

    # Search filter
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

    # ---------------- MATCHING ----------------
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
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    # ---------------- STATS ----------------
    total = len(df)
    matched = len(df[df["Time"] != "❌ Missing"])
    missing = total - matched

    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Total Stores", total)
    c2.metric("✅ Matched", matched)
    c3.metric("❌ Missing", missing)

    st.markdown("---")

    # ---------------- TABLE ----------------
    st.dataframe(df, use_container_width=True)

    # ---------------- DOWNLOAD ----------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "store_times.csv",
        "text/csv"
    )
