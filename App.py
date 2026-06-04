import streamlit as st
import pandas as pd
import re
from rapidfuzz import fuzz

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Smart Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- STORE DATABASE ----------------
STORE_DATA = {
    "VICTORY DR GA T32": {"id": "TWGGA32", "dm": "-"},
    "MILGEN GA T34": {"id": "TWGGA34", "dm": "-"},
    "WOODRUFF GA T33": {"id": "TWGGA33", "dm": "-"},
    "W FRANKLIN T42": {"id": "TWGNC41", "dm": "Kindi"},
    "CHERRY T42": {"id": "TWGSC42", "dm": "Kindi"},
    "LANCASTER SC T29": {"id": "TWGSC29", "dm": "Kindi"},
    "CANNON": {"id": "TWGNC50", "dm": "Kindi"},
    "HICKORY": {"id": "TWGNC52", "dm": "Angie"},
    "HUNTERSVILLE": {"id": "TWGNC54", "dm": "Angie"},
    "LINCOLNTON NC T30": {"id": "TWGNC30", "dm": "Angie"},
    "MOORESVILLE": {"id": "TWGNC53", "dm": "Angie"},
    "MORGANTON": {"id": "TWGNC55", "dm": "Angie"},
    "ROXIE ST": {"id": "TWGNC51", "dm": "Angie"},
    "SALISBURY NC T17": {"id": "TWGNC17", "dm": "Angie"},
    "OWEN NC T36": {"id": "TWGNC36", "dm": "Ollivanza"},
    "BONANZA NC T37": {"id": "TWGNC37", "dm": "Ollivanza"},
    "HOPE MILLS T39": {"id": "TWGNC39", "dm": "Ollivanza"},
    "BRAGG BLVD": {"id": "TWGNC56", "dm": "Ollivanza"},
    "LUMBERTON NC": {"id": "TWGNC57", "dm": "Ollivanza"},
    "GOOD MIDDLING": {"id": "TWGNC74", "dm": "Ollivanza"},
    "N EASTERN BLVD": {"id": "TWGNC75", "dm": "Ollivanza"},
    "6916 CLIFFDALE RD": {"id": "TWGNC76", "dm": "Ollivanza"},
    "NC FAY DUNN": {"id": "TWGNC77", "dm": "Ollivanza"},
    "3620 RAMSEY ST": {"id": "TWGNC78", "dm": "Ollivanza"},
    "5135 RAEFORD RD": {"id": "TWGNC79", "dm": "Ollivanza"},
    "NC LAURINBURG": {"id": "TWGNC80", "dm": "Ollivanza"},
    "AVONDALE NC T38": {"id": "TWGNC38", "dm": "Ben"},
    "GATE CITY NC T3": {"id": "TWGNC03", "dm": "Tom"},
    "COLISEUM NC T11": {"id": "TWGNC11", "dm": "Ben"},
    "EAST CONE NC T12": {"id": "TWGNC12", "dm": "Ben"},
    "EAST MARKET NC T1": {"id": "TWGNC01", "dm": "Ben"},
    "WEST MARKET NC T2": {"id": "TWGNC02", "dm": "Ben"},
    "RAMADA NC T13": {"id": "TWGNC13", "dm": "Ben"},
    "ASHEBORO NC T10": {"id": "TWGNC10", "dm": "Ben"},
    "EASTCHESTER NC T8": {"id": "TWGNC08", "dm": "Ben"},
    "GREENSBORO NC T7": {"id": "TWGNC07", "dm": "Tom"},
    "LEXINGTON NC T9": {"id": "TWGNC09", "dm": "Kindi"},
    "THOMASVILLE NC T6": {"id": "TWGNC06", "dm": "Ahmed"},
    "HANES MALL NC T5": {"id": "TWGNC05", "dm": "Ahmed"},
    "WALKERTOWN NC T4": {"id": "TWGNC04", "dm": "Ahmed"},
    "WAUGHTOWN NC T14": {"id": "TWGNC14", "dm": "Ahmed"},
    "UNIVERSITY NC T16": {"id": "TWGNC16", "dm": "Ahmed"},
    "REYNOLDA NC T15": {"id": "TWGNC15", "dm": "Kindi"},
    "MONITOR SC T21": {"id": "TWGSC21", "dm": "Noaman"},
    "SHOCKLEY SC T22": {"id": "TWGSC22", "dm": "Noaman"},
    "ANDERSON MAIN ST": {"id": "TWGSC66", "dm": "Noaman"},
    "CEDAR LANE SC T18": {"id": "TWGSC18", "dm": "Noaman"},
    "EASLEY SC T20": {"id": "TWGSC20", "dm": "Noaman"},
    "LAURENS SC T31": {"id": "TWGSC31", "dm": "Noaman"},
    "VA73 LYNCHBURG": {"id": "TWGVA73", "dm": "Mekail"},
    "S LABURNUM T48": {"id": "TWGVA48", "dm": "Syed"},
    "STAPLES MILL": {"id": "TWGVA67", "dm": "Syed"},
    "NINE MILE": {"id": "TWGVA65", "dm": "Syed"},
    "7223 HULL ST T45": {"id": "TWGVA45", "dm": "Syed"},
    "CHESTER VA": {"id": "TWGVA64", "dm": "Syed"},
    "VA68 CHAMABERLAYNE": {"id": "TWGVA68", "dm": "Syed"},
    "VA 69 JUNCTION": {"id": "TWGVA69", "dm": "Pether"},
    "VA70 PLANK": {"id": "TWGVA70", "dm": "Pether"},
    "VA71 RIO": {"id": "TWGVA71", "dm": "Pether"},
    "VA72 W MAIN": {"id": "TWGVA72", "dm": "Pether"},
    "W BROAD ST T47": {"id": "TWGVA47", "dm": "Pether"},
    "BATTLEFIELD BLVD": {"id": "TWGVA59", "dm": "Tom"},
    "GEORGE W. VA T25": {"id": "TWGVA25", "dm": "Tom"},
    "KECOUGHTAN VA T26": {"id": "TWGVA26", "dm": "Ysimailyn"},
    "NORFOLK VA T27": {"id": "TWGVA27", "dm": "Ysimailyn"},
    "VIRGINIA BEACH T40": {"id": "TWGVA40", "dm": "Ysimailyn"},
    "GREAT NECK RD": {"id": "TWGVA60", "dm": "Ysimailyn"},
    "J CLYDE MORRIS": {"id": "TWGVA63", "dm": "Ysimailyn"},
    "NEWMARKET DR": {"id": "TWGVA62", "dm": "Ysimailyn"},
    "HIGH ST VA T24": {"id": "TWGVA24", "dm": "Ysimailyn"},
    "ABERDEEN VA T28": {"id": "TWGVA28", "dm": "Erika"},
    "WARWICK BLVD": {"id": "TWGVA61", "dm": "Erika"},
    "WEST MERCURY BLVD 2": {"id": "TWGVA58", "dm": "Erika"}
}

# ---------------- MATCH STORE ----------------
def normalize(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

def find_store(text):
    best = None
    score_best = 0

    for store in STORE_DATA:
        score = fuzz.partial_ratio(normalize(text), normalize(store))
        if score > score_best and score >= 70:
            score_best = score
            best = store

    return best

# ---------------- SMART PARSER ----------------
def parse_raw(raw_text):
    data = {}

    lines = raw_text.splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # extract time anywhere in line
        time_match = re.search(r'\d{1,2}:\d{2}\s?(AM|PM|am|pm)?', line)

        if time_match:
            time = time_match.group()

            store = re.sub(r'\d{1,2}:\d{2}\s?(AM|PM|am|pm)?', '', line)
            store = re.sub(r'[-|]', '', store).strip()

            if store:
                data[store] = time

    return data

# ---------------- UI ----------------
st.title("📊 TWG SMART MASTER DASHBOARD")

raw_data = st.text_area("📥 Paste Raw Data", height=250)

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    extracted = parse_raw(raw_data)

    results = []

    for store in STORE_DATA:

        matched = find_store(store)

        if matched:
            time_value = extracted.get(matched, "")
            sid = STORE_DATA[matched]["id"]
            dm = STORE_DATA[matched]["dm"]
        else:
            time_value = ""
            sid = ""
            dm = ""

        results.append({
            "Store Name": store,
            "Store ID": sid,
            "DM": dm,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Stores", len(df))
    col2.metric("Matched", len(df[df["Time"] != "❌ Missing"]))
    col3.metric("Missing", len(df[df["Time"] == "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode(),
        "twg_report.csv",
        "text/csv"
    )
