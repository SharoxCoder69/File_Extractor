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

# ---------------- STORE DATA (IMAGE FINAL LIST ONLY) ----------------
STORE_DATA = {
    "VICTORY DR GA T32": {"id": "", "dm": ""},
    "MILGEN GA T34": {"id": "", "dm": ""},
    "WOODRUFF GA T33": {"id": "", "dm": ""},

    "W FRANKLIN T42": {"id": "", "dm": ""},
    "CHERRY T42": {"id": "", "dm": ""},
    "LANCASTER SC T29": {"id": "", "dm": ""},

    "CANNON": {"id": "", "dm": ""},
    "HICKORY": {"id": "", "dm": ""},
    "HUNTERSVILLE": {"id": "", "dm": ""},
    "LINCOLNTON NC T30": {"id": "", "dm": ""},
    "MOORESVILLE": {"id": "", "dm": ""},
    "MORGANTON": {"id": "", "dm": ""},
    "ROXIE ST": {"id": "", "dm": ""},
    "SALISBURY NC T17": {"id": "", "dm": ""},

    "OWEN NC T36": {"id": "", "dm": ""},
    "BONANZA NC T37": {"id": "", "dm": ""},
    "BRAGG BLVD": {"id": "", "dm": ""},
    "LUMBERTON NC": {"id": "", "dm": ""},
    "GOOD MIDDLING": {"id": "", "dm": ""},
    "N EASTERN BLVD": {"id": "", "dm": ""},
    "6916 CLIFFDALE RD": {"id": "", "dm": ""},
    "NC FAY DUNN": {"id": "", "dm": ""},
    "3620 RAMSEY ST": {"id": "", "dm": ""},
    "5135 RAEFORD RD": {"id": "", "dm": ""},
    "NC LAURINBURG": {"id": "", "dm": ""},

    "AVONDALE NC T38": {"id": "TWGNC38", "dm": "Ben"},
    "GATE CITY NC T3": {"id": "TWGNC03", "dm": "Tom"},
    "COLISEUM NC T11": {"id": "", "dm": ""},
    "EAST CONE NC T12": {"id": "", "dm": ""},
    "EAST MARKET NC T1": {"id": "", "dm": ""},
    "WEST MARKET NC T2": {"id": "", "dm": ""},

    "ASHEBORO NC T10": {"id": "", "dm": ""},
    "EASTCHESTER NC T8": {"id": "", "dm": ""},
    "GREENSBORO NC T7": {"id": "", "dm": ""},
    "LEXINGTON NC T9": {"id": "", "dm": ""},
    "THOMASVILLE NC T6": {"id": "", "dm": ""},

    "WALKERTOWN NC T4": {"id": "", "dm": ""},
    "WAUGHTOWN NC T14": {"id": "", "dm": ""},
    "UNIVERSITY NC T16": {"id": "", "dm": ""},
    "REYNOLDA NC T15": {"id": "", "dm": ""},

    "ANDERSON MAIN ST": {"id": "", "dm": ""},
    "CEDAR LANE SC T18": {"id": "", "dm": ""},
    "EASLEY SC T20": {"id": "TWGSC20", "dm": "Noaman"},
    "LAURENS SC T31": {"id": "", "dm": ""},

    "VA73 LYNCHBURG": {"id": "TWGVA73", "dm": "Mekail"},
    "S LABURNUM T48": {"id": "", "dm": ""},
    "STAPLES MILL": {"id": "", "dm": ""},
    "NINE MILE": {"id": "", "dm": ""},
    "7223 HULL ST T45": {"id": "", "dm": ""},
    "CHESTER VA": {"id": "", "dm": ""},

    "VA68 CHAMABERLAYNE": {"id": "", "dm": ""},
    "VA 69 JUNCTION": {"id": "", "dm": ""},
    "VA70 PLANK": {"id": "", "dm": ""},
    "VA71 RIO": {"id": "", "dm": ""},
    "VA72 W MAIN": {"id": "", "dm": ""},

    "W BROAD ST T47": {"id": "", "dm": ""},
    "BATTLEFIELD BLVD": {"id": "", "dm": ""},
    "GEORGE W. VA T25": {"id": "", "dm": ""},
    "KECOUGHTAN VA T26": {"id": "", "dm": ""},
    "NORFOLK VA T27": {"id": "", "dm": ""},
    "VIRGINIA BEACH T40": {"id": "", "dm": ""},

    "GREAT NECK RD": {"id": "", "dm": ""},
    "J CLYDE MORRIS": {"id": "", "dm": ""},
    "NEWMARKET DR": {"id": "", "dm": ""},
    "HIGH ST VA T24": {"id": "", "dm": ""},
    "ABERDEEN VA T28": {"id": "", "dm": ""},
    "WARWICK BLVD": {"id": "", "dm": ""},
    "WEST MERCURY BLVD 2": {"id": "", "dm": ""},
}

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

store_embeddings = {
    store: model.encode(store)
    for store in STORE_DATA
}

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
            time_match = re.search(r'\d{1,2}:\d{2}\s?(AM|PM|am|pm)?', lines[i+1])

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

    if len(parsed) == 0:
        st.error("No data parsed. Check raw format.")
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
