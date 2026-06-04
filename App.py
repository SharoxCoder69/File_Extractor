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

# ---------------- MODERN CLEAN UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0b1220, #111827);
    color: #e5e7eb;
}

/* MAIN TITLE (SOFT + PROFESSIONAL) */
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #e5e7eb;
    letter-spacing: 1px;
    margin-bottom: 5px;
}

/* SUBTITLE */
.sub-title {
    text-align: center;
    color: #9ca3af;
    font-size: 14px;
    margin-bottom: 25px;
}

/* TEXT AREA */
textarea {
    border-radius: 12px !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: white !important;
}

/* BUTTON (MODERN SOFT GRADIENT) */
.stButton > button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    color: white;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 20px rgba(37,99,235,0.3);
}

/* METRICS CARDS */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    padding: 15px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* FOOTER */
.footer {
    text-align: center;
    font-size: 12px;
    color: #6b7280;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-title">Store Time Dashboard</div>
<div class="sub-title">TOTALLYWIRELESSGROUP • Smart Extraction System</div>
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
        st.warning("Please fill both fields")
        st.stop()

    # Progress animation
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress.progress(i + 1)

    # ---------------- CLEAN DATA ----------------
    master_stores = [s.strip() for s in master_list.splitlines() if s.strip()]
    lines = [l.strip() for l in raw_data.splitlines() if l.strip()]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    ignore_words = ["Panel", "Partition", "Disarmed", "Armed", "[Mobile]", "Command:"]

    extracted = {}
    current_store = None

    for line in lines:

        if any(word.lower() in line.lower() for word in ignore_words):
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
    col1.metric("📦 Total", total)
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
<div class="footer">
Built for TOTALLYWIRELESSGROUP
</div>
""", unsafe_allow_html=True)
