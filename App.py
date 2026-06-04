import streamlit as st
import pandas as pd
import re

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Data Pipeline",
    page_icon="📊",
    layout="wide"
)

# ---------------- STORE DATA ----------------
STORE_DATA = {

    # ---------------- GA ----------------
    "VICTORY DR GA T32": {"id": "TWGGA32", "dm": "-"},
    "MILGEN GA T34": {"id": "TWGGA34", "dm": "-"},
    "WOODRUFF GA T33": {"id": "TWGGA33", "dm": "-"},

    # ---------------- SC ----------------
    "LANCASTER SC T29": {"id": "TWGSC29", "dm": "Kindi"},
    "CHERRY T42": {"id": "TWGSC42", "dm": "Kindi"},
    "MONITOR SC T21": {"id": "TWGSC21", "dm": "Ollivanza"},
    "SHOCKLEY SC T22": {"id": "TWGSC22", "dm": "Ollivanza"},
    "CEDAR LANE SC T18": {"id": "TWGSC18", "dm": "Ollivanza"},
    "EASLEY SC T20": {"id": "TWGSC20", "dm": "Noaman"},
    "LAURENS SC T31": {"id": "TWGSC31", "dm": "Ollivanza"},

    # ---------------- NC CORE ----------------
    "W FRANKLIN T42": {"id": "TWGNC41", "dm": "Kindi"},
    "CANNON": {"id": "TWGNC50", "dm": "Kindi"},
    "HICKORY": {"id": "TWGNC52", "dm": "Angie"},
    "HUNTERSVILLE": {"id": "TWGNC54", "dm": "Angie"},
    "LINCOLNTON NC T30": {"id": "TWGNC30", "dm": "Angie"},
    "MOORESVILLE": {"id": "TWGNC53", "dm": "Angie"},
    "MORGANTON": {"id": "TWGNC55", "dm": "Angie"},
    "ROXIE ST": {"id": "TWGNC51", "dm": "Angie"},
    "SALISBURY NC T17": {"id": "TWGNC17", "dm": "Angie"},

    # ---------------- FAYETTEVILLE ----------------
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

    # ---------------- NC OTHER ----------------
    "AVONDALE NC T38": {"id": "TWGNC38", "dm": "Ben"},
    "GATE CITY NC T3": {"id": "TWGNC03", "dm": "Tom"},
    "COLISEUM NC T11": {"id": "TWGNC11", "dm": "Ollivanza"},
    "EAST CONE NC T12": {"id": "TWGNC12", "dm": "Ollivanza"},
    "EAST MARKET NC T1": {"id": "TWGNC01", "dm": "Ollivanza"},
    "WEST MARKET NC T2": {"id": "TWGNC02", "dm": "Ollivanza"},
    "ASHEBORO NC T10": {"id": "TWGNC10", "dm": "Ollivanza"},
    "EASTCHESTER NC T8": {"id": "TWGNC08", "dm": "Ollivanza"},
    "GREENSBORO NC T7": {"id": "TWGNC07", "dm": "Ollivanza"},
    "LEXINGTON NC T9": {"id": "TWGNC09", "dm": "Ollivanza"},
    "THOMASVILLE NC T6": {"id": "TWGNC06", "dm": "Ollivanza"},
    "WALKERTOWN NC T4": {"id": "TWGNC04", "dm": "Ollivanza"},
    "WAUGHTOWN NC T14": {"id": "TWGNC14", "dm": "Ollivanza"},
    "UNIVERSITY NC T16": {"id": "TWGNC16", "dm": "Ollivanza"},
    "REYNOLDA NC T15": {"id": "TWGNC15", "dm": "Ollivanza"},

    # ---------------- VA ----------------
    "VA73 LYNCHBURG": {"id": "TWGVA73", "dm": "Mekail"},
    "S LABURNUM T48": {"id": "TWGVA48", "dm": "Ollivanza"},
    "STAPLES MILL": {"id": "TWGVA49", "dm": "Ollivanza"},
    "NINE MILE": {"id": "TWGVA50", "dm": "Ollivanza"},
    "7223 HULL ST T45": {"id": "TWGVA45", "dm": "Ollivanza"},
    "CHESTER VA": {"id": "TWGVA46", "dm": "Ollivanza"},
    "VA68 CHAMABERLAYNE": {"id": "TWGVA68", "dm": "Ollivanza"},
    "VA 69 JUNCTION": {"id": "TWGVA69", "dm": "Ollivanza"},
    "VA70 PLANK": {"id": "TWGVA70", "dm": "Ollivanza"},
    "VA71 RIO": {"id": "TWGVA71", "dm": "Ollivanza"},
    "VA72 W MAIN": {"id": "TWGVA72", "dm": "Ollivanza"},
    "W BROAD ST T47": {"id": "TWGVA47", "dm": "Ollivanza"},
    "GEORGE W VA T25": {"id": "TWGVA25", "dm": "Ollivanza"},
    "KECOUGHTAN VA T26": {"id": "TWGVA26", "dm": "Ollivanza"},
    "NORFOLK VA T27": {"id": "TWGVA27", "dm": "Ollivanza"},
    "VIRGINIA BEACH T40": {"id": "TWGVA40", "dm": "Ollivanza"},
}

# ---------------- CLEAN ----------------
def clean_text(text):
    text = str(text).upper()
    text = re.sub(r'[^A-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------- SMART MATCH ----------------
def ai_match(raw_text):

    cleaned_input = clean_text(raw_text)
    input_words = set(cleaned_input.split())

    best_match = None
    best_score = 0

    for store in STORE_DATA.keys():

        cleaned_store = clean_text(store)
        store_words = set(cleaned_store.split())

        # exact match
        if cleaned_store == cleaned_input:
            return store

        # contains match
        if cleaned_store in cleaned_input or cleaned_input in cleaned_store:
            return store

        # word overlap scoring
        common = input_words & store_words
        score = len(common)

        if any(char.isdigit() for char in cleaned_store):
            score += 1

        if score > best_score:
            best_score = score
            best_match = store

    if best_score >= 1:
        return best_match

    return "UNMATCHED"

# ---------------- PARSER ----------------
def extract_store_time(raw_text):
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    results = []
    i = 0

    while i < len(lines):

        line = lines[i]

        match = re.search(r'(.+?)\s+(\d{1,2}:\d{2}\s?(AM|PM|am|pm)?)', line)

        if match:
            results.append((match.group(1).strip(), match.group(2).strip()))
            i += 1
            continue

        if i + 1 < len(lines):
            time_match = re.search(r'\d{1,2}:\d{2}', lines[i+1])
            if time_match:
                results.append((line, time_match.group()))
                i += 2
                continue

        i += 1

    return results

# ---------------- UI ----------------
st.title("🤖 TWG DATA PIPELINE SYSTEM")

raw_data = st.text_area("📥 Paste Raw Data", height=400)

if st.button("🚀 Process Data"):

    extracted = extract_store_time(raw_data)

    final = []

    for store_raw, time in extracted:

        matched = ai_match(store_raw)

        if matched in STORE_DATA:
            sid = STORE_DATA[matched]["id"]
            dm = STORE_DATA[matched]["dm"]
        else:
            sid = ""
            dm = ""

        final.append({
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm,
            "Time": time,
            "Raw Store": store_raw
        })

    df = pd.DataFrame(final)

    df = df.sort_values(by=["Store Name"])

    st.metric("Total Records", len(df))
    st.metric("Matched Stores", len(df[df["Store Name"] != "UNMATCHED"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode(),
        "twg_pipeline.csv",
        "text/csv"
    )
