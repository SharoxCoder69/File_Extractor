import streamlit as st
import pandas as pd
import re

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="Store Time Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center; color:#4CAF50;'>📊 Store Time Dashboard</h1>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙ Settings")
    st.write("Paste your master list + raw data")

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

    ignore_words = ["Panel", "Partition", "Disarmed by", "Armed Away by", "[Mobile]"]

    extracted = {}
    current_store = None

    # -------- Extract store + time --------
    for line in lines:

        if any(w.lower() in line.lower() for w in ignore_words):
            continue

        if re.match(time_pattern, line):
            if current_store:
                extracted[current_store.upper()] = line
            continue

        current_store = line

    # -------- Match with master list --------
    results = []

    for store in master_stores:

        time_value = ""

        for raw_store, t in extracted.items():

            words = raw_store.split()

            if any(w in store.upper() for w in words if len(w) > 2):
                time_value = t
                break

        results.append({
            "Store Name": store,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    # ---------------- OUTPUT UI ----------------
    st.markdown("## 📋 Result Table")
    st.dataframe(df, use_container_width=True)

    # ---------------- STATS ----------------
    total = len(df)
    filled = len(df[df["Time"] != "❌ Missing"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Stores", total)
    col2.metric("Matched", filled)
    col3.metric("Missing", total - filled)

    # ---------------- DOWNLOAD ----------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "store_times.csv",
        "text/csv"
    )
