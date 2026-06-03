import streamlit as st
import pandas as pd
import re

st.title("Store Time Extractor")

master_list = st.text_area(
    "Paste Master Store List",
    height=250
)

raw_data = st.text_area(
    "Paste Raw Data",
    height=400
)

if st.button("Process Data"):

    master_stores = [
        s.strip()
        for s in master_list.splitlines()
        if s.strip()
    ]

    lines = [
        line.strip()
        for line in raw_data.splitlines()
        if line.strip()
    ]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    ignore_words = [
        "Panel",
        "Partition",
        "Disarmed by",
        "Armed Away by",
        "[Mobile]"
    ]

    extracted = {}

    current_store = None

    for line in lines:

        if any(
            word.lower() in line.lower()
            for word in ignore_words
        ):
            continue

        if re.match(time_pattern, line):

            if current_store:
                extracted[current_store.upper()] = line

            continue

        current_store = line

    results = []

    for master_store in master_stores:

        best_time = ""

        master_upper = master_store.upper()

        for raw_store, time_value in extracted.items():

            words = raw_store.replace(".", "").split()

            if any(
                word in master_upper
                for word in words
                if len(word) > 2
            ):
                best_time = time_value
                break

        results.append({
            "Store Name": master_store,
            "Time": best_time
        })

    df = pd.DataFrame(results)

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "stores.csv",
        "text/csv"
    )
