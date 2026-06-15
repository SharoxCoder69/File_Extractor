import streamlit as st
import pandas as pd
import re
from io import BytesIO
from openpyxl import load_workbook

st.set_page_config(page_title="Store Employee YES Generator")

STORES = [
    "TWGSC18 -CEDAR LANE SC",
    "TWGSC20 -EASLEY SC",
    "TWGSC21 -MONITOR SC",
    "TWGSC22 -SHOCKLEY SC",
    "TWGSC31 -LAURENS SC",
    "TWGSC66 -ANDERSON MAIN ST SC",
    "TWGVA24 -HIGH ST VA",
    "TWGVA25 -GEORGE W. VA",
    "TWGVA26 -KECOUGHTAN VA",
    "TWGVA27 -NORFOLK VA",
    "TWGVA28 -ABERDEEN VA",
    "TWGVA40 -VIRGINIA BEACH VA",
    "TWGVA58 -WEST MERCURY BLVD VA",
    "TWGVA59 -BATTLEFIELD BLVD VA",
    "TWGVA60 -GREAT NECK RD VA",
    "TWGVA61 -WARWICK BLVD VA",
    "TWGVA62 - NEWMARKET DR VA",
    "TWGVA63 -J CLYDE MORRIS VA",
]

st.title("Store Employee YES Generator")

raw_file = st.file_uploader(
    "Upload Raw Data TXT File",
    type=["txt"]
)

report_file = st.file_uploader(
    "Upload EMP Report XLSX",
    type=["xlsx"]
)

def extract_ntids(text):

    ntids = set()

    for store in STORES:

        if store not in text:
            continue

        start = text.find(store)

        next_pos = len(text)

        for s in STORES:
            pos = text.find(s, start + 1)

            if pos != -1 and pos < next_pos:
                next_pos = pos

        block = text[start:next_pos]

        for line in block.splitlines():

            match = re.match(
                r"^([A-Z]{3}\d{5})",
                line.strip()
            )

            if match:
                ntids.add(match.group(1))

    return ntids

if st.button("Generate Report"):

    if raw_file is None or report_file is None:
        st.error("Please upload both files.")
        st.stop()

    text = raw_file.read().decode(
        "utf-8",
        errors="ignore"
    )

    ntids = extract_ntids(text)

    wb = load_workbook(report_file)

    updated_count = 0

    for ws in wb.worksheets:

        for row in range(1, ws.max_row + 1):

            ntid = ws.cell(
                row=row,
                column=3
            ).value

            if ntid in ntids:

                for col in range(5, 11):
                    ws.cell(
                        row=row,
                        column=col
                    ).value = "Yes"

                updated_count += 1

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    st.success(
        f"{updated_count} employees updated successfully."
    )

    st.download_button(
        label="Download Updated Report",
        data=output,
        file_name="EMP_Report_UPDATED.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
