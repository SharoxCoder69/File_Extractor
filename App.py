import streamlit as st
import pandas as pd
import re
import time
import os

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Store Dashboard",
    page_icon="📊",
    layout="wide"
)

FILE_PATH = "master_list.csv"

# ---------------- LOAD SAVED MASTER LIST ----------------
if "master_list" not in st.session_state:

    if os.path.exists(FILE_PATH):
        df_saved = pd.read_csv(FILE_PATH)
        st.session_state.master_list = df_saved["store"].tolist()
    else:
        st.session_state.master_list = []

# ---------------- SAVE FUNCTION ----------------
def save_master_list():
    df = pd.DataFrame({"store": st.session_state.master_list})
    df.to_csv(FILE_PATH, index=False)

# ---------------- ADD MASTER STORE ----------------
st.title("📊 Store Dashboard")

new_store = st.text_input("➕ Add Store to Master List")

colA, colB = st.columns(2)

with colA:
    if st.button("Add Store"):
        if new_store:
            st.session_state.master_list.append(new_store)
            save_master_list()
            st.success("Store Added & Saved!")

with colB:
    if st.button("🗑 Clear Master List"):
        st.session_state.master_list = []
        save_master_list()
        st.warning("Master List Cleared!")

# ---------------- SHOW MASTER LIST ----------------
st.markdown("## 📌 Saved Master List")

for i, store in enumerate(st.session_state.master_list):
    st.write(f"{i+1}. {store}")

st.markdown("---")

# ---------------- RAW INPUT ----------------
raw_data = st.text_area("📥 Raw Data", height=200)

# ---------------- PROCESS ----------------
if st.button("🚀 Process"):

    if not st.session_state.master_list or not raw_data:
        st.warning("Master List or Raw Data missing")
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

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "report.csv",
        "text/csv"
    )
