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

# ---------------- LOADING ANIMATION ----------------
with st.spinner("Loading TOTALLYWIRELESSGROUP Dashboard... 🚀"):
    time.sleep(1.2)

# ---------------- BACKGROUND WATERMARK ----------------
st.markdown(
    """
    <style>

    .watermark {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-20deg);
        font-size: 80px;
        font-weight: 900;
        color: rgba(0, 255, 200, 0.06);
        z-index: -1;
        white-space: nowrap;
        animation: floatText 6s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes floatText {
        0% {transform: translate(-50%, -50%) rotate(-20deg) scale(1);}
        50% {transform: translate(-50%, -52%) rotate(-20deg) scale(1.05);}
        100% {transform: translate(-50%, -50%) rotate(-20deg) scale(1);}
    }

    /* Founder Box */
    .founder-box {
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
        animation: slideDown 1.2s ease-in-out, glow 2s infinite;
    }

    @keyframes slideDown {
        from {transform: translateY(-40px); opacity: 0;}
        to {transform: translateY(0); opacity: 1;}
    }

    @keyframes glow {
        0% {box-shadow: 0 0 5px #00ffcc;}
        50% {box-shadow: 0 0 20px #00ffcc;}
        100% {box-shadow: 0 0 5px #00ffcc;}
    }

    /* Title */
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }

    .sub-title {
        text-align: center;
        color: gray;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- WATERMARK TEXT ----------------
st.markdown(
    "<div class='watermark'>TOTALLYWIRELESSGROUP</div>",
    unsafe_allow_html=True
)

# ---------------- FOUNDER BOX ----------------
st.markdown(
    "<div class='founder-box'>👑 Founder: Sharox Javaid</div>",
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>📊 Store Time Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Smart Store & Time Extraction System</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    master_list = st.text_area("📌 Master Store List", height=300)

with col2:
    raw_data = st.text_area("📥 Raw Data", height=300)

# ---------------- PROCESS ----------------
if st.button("🚀 Process Data"):

    if not master_list or not raw_data:
        st.warning("Please fill both inputs")
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
