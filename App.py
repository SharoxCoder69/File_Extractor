import streamlit as st
import pandas as pd
import re

st.title("Store & Time Extractor")

raw_data = st.text_area(
    "Paste Raw Data Here",
    height=250,
    placeholder="Example:\nWalmart 9:00 AM\nTarget 10:30 AM"
)

if st.button("Process Data"):

    if not raw_data.strip():
        st.warning("Please paste some data first.")
        st.stop()

    lines = raw_data.splitlines()
    results = []

    time_pattern = r'(\d{1,2}:\d{2}\s?(?:AM|PM|am|pm))'

    for line in lines:
        line = line.strip()

        if not line:
            continue

        match = re.search(time_pattern, line)

        if match:
            time_value = match.group(1)
            store_name = re.sub(time_pattern, "", line).strip()

            results.append({
                "Store Name": store_name,
                "Time": time_value
            })

    if results:
        df = pd.DataFrame(results)

        st.success(f"Found {len(df)} records")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="stores.csv",
            mime="text/csv"
        )
    else:
        st.warning("No store/time data found.")
