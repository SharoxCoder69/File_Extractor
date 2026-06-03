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

# ---------------- ANIMATION (LOADING) ----------------
with st.spinner("Loading Dashboard... 🚀"):
    time.sleep(1.2)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #4CAF50;
        animation: pulse 1.8s infinite;
        margin-bottom: 10px;
    }

    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }

    .sub-title {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }

    .card {
        background-color: #111;
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>📊 Store Time Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Smart Store & Time Extractor System</div>", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    master_list = st.text_area("📌 Master Store List", height=300)

with col2:
    raw_data = st.text_area("📥 Raw Data", height=300)

# ---------------- PROCESS ----------------
if st.button("🚀 Process Data"):

    if not master_list or not raw_data:
        st.warning("Please fill both Master List and Raw Data")
        st.stop()

    master_stores = [s.strip() for s in master_list.splitlines() if s.strip()]
    lines = [l.strip() for l in raw_data.splitlines() if l.strip()]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    ignore_words = [
        "Panel",
        "Partition",
        "Disarmed by",
        "Armed Away by",
        "[Mobile]",
        "Command:"
    ]

    extracted = {}
    current_store = None

    # ---------------- EXTRACT DATA ----------------
    for line in lines:

        if any(w.lower() in line.lower() for w in ignore_words):
            continue

        if re.match(time_pattern, line):
            if current_store:
                extracted[current_store.upper()] = line
            continue

        current_store = line

    # ---------------- MATCH WITH MASTER ----------------
    results = []

    for store in master_stores:

        time_value = ""

        for raw_store, t in extracted.items():

            words = raw_store.replace(".", "").split()

            if any(w in store.upper() for w in words if len(w) > 2):
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
