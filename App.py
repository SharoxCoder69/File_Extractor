import streamlit as st
import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- MASTER STORE DATA ----------------
STORE_DATA = {
    # -------- GA --------
    "VICTORY DR GA T32": {"id": "TWGGA32", "dm": "-"},
    "MILGEN GA T34": {"id": "TWGGA34", "dm": "-"},
    "WOODRUFF GA T33": {"id": "TWGGA33", "dm": "-"},

    # -------- SC --------
    "LANCASTER SC T29": {"id": "TWGSC29", "dm": "Kindi"},
    "CHERRY T42": {"id": "TWGSC42", "dm": "Kindi"},
    "EASLEY SC T20": {"id": "TWGSC20", "dm": "Noaman"},
    "CEDAR LANE SC T18": {"id": "TWGSC18", "dm": "Ollivanza"},
    "LAURENS SC T31": {"id": "TWGSC31", "dm": "Ollivanza"},

    # -------- NC CORE --------
    "W FRANKLIN T42": {"id": "TWGNC41", "dm": "Kindi"},
    "CANNON": {"id": "TWGNC50", "dm": "Kindi"},
    "HICKORY": {"id": "TWGNC52", "dm": "Angie"},
    "HUNTERSVILLE": {"id": "TWGNC54", "dm": "Angie"},
    "LINCOLNTON NC T30": {"id": "TWGNC30", "dm": "Angie"},
    "MOORESVILLE": {"id": "TWGNC53", "dm": "Angie"},
    "MORGANTON": {"id": "TWGNC55", "dm": "Angie"},
    "ROXIE ST": {"id": "TWGNC51", "dm": "Angie"},
    "SALISBURY NC T17": {"id": "TWGNC17", "dm": "Angie"},

    # -------- NC FAY --------
    "OWEN NC T36": {"id": "TWGNC36", "dm": "Ollivanza"},
    "BONANZA NC T37": {"id": "TWGNC37", "dm": "Ollivanza"},
    "BRAGG BLVD": {"id": "TWGNC56", "dm": "Ollivanza"},
    "LUMBERTON NC": {"id": "TWGNC57", "dm": "Ollivanza"},
    "GOOD MIDDLING": {"id": "TWGNC74", "dm": "Ollivanza"},
    "N EASTERN BLVD": {"id": "TWGNC75", "dm": "Ollivanza"},
    "6916 CLIFFDALE RD": {"id": "TWGNC76", "dm": "Ollivanza"},
    "NC FAY DUNN": {"id": "TWGNC77", "dm": "Ollivanza"},
    "3620 RAMSEY ST": {"id": "TWGNC78", "dm": "Ollivanza"},
    "5135 RAEFORD RD": {"id": "TWGNC79", "dm": "Ollivanza"},
    "NC LAURINBURG": {"id": "TWGNC80", "dm": "Ollivanza"},

    # -------- NEW NC --------
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

    # -------- VA --------
    "LYNCHBURG VA T73": {"id": "TWGVA73", "dm": "Mekail"},
    "S LABURNUM T48": {"id": "TWGVA48", "dm": "Ollivanza"},
    "STAPLES MILL": {"id": "TWGVA??", "dm": "Ollivanza"},
    "NINE MILE": {"id": "TWGVA??", "dm": "Ollivanza"},
    "7223 HULL ST T45": {"id": "TWGVA45", "dm": "Ollivanza"},
    "CHESTER VA": {"id": "TWGVA??", "dm": "Ollivanza"},

    "VA CHAMABERLAYNE": {"id": "TWGVA??", "dm": "Ollivanza"},
    "VA JUNCTION": {"id": "TWGVA??", "dm": "Ollivanza"},
    "VA PLANK": {"id": "TWGVA??", "dm": "Ollivanza"},
    "VA RIO": {"id": "TWGVA??", "dm": "Ollivanza"},
    "VA W MAIN": {"id": "TWGVA??", "dm": "Ollivanza"},

    "BATTLEFIELD BLVD": {"id": "TWGVA??", "dm": "Ollivanza"},
    "GEORGE W VA T25": {"id": "TWGVA25", "dm": "Ollivanza"},
    "KECOUGHTAN VA T26": {"id": "TWGVA26", "dm": "Ollivanza"},
    "NORFOLK VA T27": {"id": "TWGVA27", "dm": "Ollivanza"},
    "VIRGINIA BEACH T40": {"id": "TWGVA40", "dm": "Ollivanza"},
}

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

store_embeddings = {k: model.encode(k) for k in STORE_DATA}

# ---------------- PARSER ----------------
def parse_raw(raw_text):
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

# ---------------- AI MATCH ----------------
def ai_match(text):
    text_emb = model.encode(text)

    best_store = None
    best_score = 0

    for store, emb in store_embeddings.items():
        score = util.cos_sim(text_emb, emb).item()
        if score > best_score:
            best_score = score
            best_store = store

    return best_store

# ---------------- UI ----------------
st.title("🤖 TWG AI SMART DASHBOARD")

raw_data = st.text_area("📥 Paste Raw Data", height=300)

if st.button("🚀 Generate Report"):

    parsed = parse_raw(raw_data)

    if not parsed:
        st.error("No data parsed")
        st.stop()

    results = []

    for raw_store, time in parsed:
        matched = ai_match(raw_store)

        sid = STORE_DATA.get(matched, {}).get("id", "")
        dm = STORE_DATA.get(matched, {}).get("dm", "")

        results.append({
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm,
            "Raw Store": raw_store,
            "Time": time
        })

    df = pd.DataFrame(results)

    st.metric("Total Records", len(df))
    st.metric("Matched Stores", len(df[df["Store Name"] != ""]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode(),
        "twg_ai_report.csv",
        "text/csv"
    )
