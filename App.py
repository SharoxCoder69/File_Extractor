import streamlit as st
import pandas as pd
import re
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TOTALLYWIRELESSGROUP Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- MODERN CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(90deg,#00f5d4,#00bbf9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {filter: drop-shadow(0 0 5px #00f5d4);}
    to {filter: drop-shadow(0 0 20px #00bbf9);}
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 16px;
    margin-bottom: 20px;
}

/* Text Areas */
textarea {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
}

/* Button */
.stButton > button {
    width: 100%;
    padding: 14px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg,#00f5d4,#00bbf9);
    color: black;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,245,212,0.6);
}

/* Metrics cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Table */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Footer */
.footer {
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 12px;
    color: #00f5d4;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-title">🚀 TOTALLYWIRELESSGROUP</div>
<div class="sub-title">Smart Store Time Extraction Dashboard</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    master_list = st.text_area("📌 Master Store List", height=300)

with col2:
    raw_data = st.text_area("📥 Raw Data", height=300)

# ---------------- PROCESS BUTTON ----------------
if st.button("🚀 Process Data"):

    if not master_list or not raw_data:
        st.warning("Please fill both inputs")
        st.stop()

    # Loading animation
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # ---------------- CLEAN DATA ----------------
    master_stores = [s.strip() for s in master_list.splitlines() if s.strip()]
    lines = [l.strip() for l in raw_data.splitlines() if l.strip()]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    ignore_words = ["Panel", "Partition", "Disarmed", "Armed", "[Mobile]", "Command:"]

    extracted = {}
    current_store = None

    for line in lines:

        if any(w.lower() in line.lower() for w in ignore_words):
            continue

        if re.match(time_pattern, line):
            if current_store:
                extracted[current_store.upper()] = line
            continue

        current_store = line

    # ---------------- MATCHING ----------------
    results = []

    for store in master_stores:

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

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Stores", total)
    col2.metric("✅ Matched", matched)
    col3.metric("❌ Missing", missing)

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

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">👑 Developed for TOTALLYWIRELESSGROUP</div>
""", unsafe_allow_html=True)
