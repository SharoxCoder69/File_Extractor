import streamlit as st
import pandas as pd
import re
from rapidfuzz import fuzz

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Store Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- USERS ----------------
USERS = {
    "admin": "1234",
    "twg": "password",
    "manager": "admin123"
}

# ---------------- FULL STORE MAP (COMPLETE RESTORED) ----------------
STORE_MAP = {
    "VICTORY DR GA T32": "TWGGA32",
    "MILGEN GA T34": "TWGGA34",
    "WOODRUFF GA T33": "TWGGA33",
    "W FRANKLIN T42": "TWGNC41",
    "CHERRY T42": "TWGSC42",
    "LANCASTER SC T29": "TWGSC29",
    "CANNON": "TWGNC50",
    "HICKORY": "TWGNC52",
    "HUNTERSVILLE": "TWGNC54",
    "LINCOLNTON NC T30": "TWGNC30",
    "MOORESVILLE": "TWGNC53",
    "MORGANTON": "TWGNC55",
    "ROXIE ST": "TWGNC51",
    "SALISBURY NC T17": "TWGNC17",
    "OWEN NC T36": "TWGNC36",
    "BONANZA NC T37": "TWGNC37",
    "HOPE MILLS T39": "TWGNC39",
    "BRAGG BLVD": "TWGNC56",
    "LUMBERTON NC": "TWGNC57",
    "GOOD MIDDLING": "TWGNC74",
    "N EASTERN BLVD": "TWGNC75",
    "6916 CLIFFDALE RD": "TWGNC76",
    "NC FAY DUNN": "TWGNC77",
    "3620 RAMSEY ST": "TWGNC78",
    "5135 RAEFORD RD": "TWGNC79",
    "NC LAURINBURG": "TWGNC80",
    "AVONDALE NC T38": "TWGNC38",
    "GATE CITY NC T3": "TWGNC03",
    "COLISEUM NC T11": "TWGNC11",
    "EAST CONE NC T12": "TWGNC12",
    "EAST MARKET NC T1": "TWGNC01",
    "WEST MARKET NC T2": "TWGNC02",
    "RAMADA NC T13": "TWGNC13",
    "ASHEBORO NC T10": "TWGNC10",
    "EASTCHESTER NC T8": "TWGNC08",
    "GREENSBORO NC T7": "TWGNC07",
    "LEXINGTON NC T9": "TWGNC09",
    "THOMASVILLE NC T6": "TWGNC06",
    "HANES MALL NC T5": "TWGNC05",
    "WALKERTOWN NC T4": "TWGNC04",
    "WAUGHTOWN NC T14": "TWGNC14",
    "UNIVERSITY NC T16": "TWGNC16",
    "REYNOLDA NC T15": "TWGNC15",
    "MONITOR SC T21": "TWGSC21",
    "SHOCKLEY SC T22": "TWGSC22",
    "ANDERSON MAIN ST": "TWGSC66",
    "CEDAR LANE SC T18": "TWGSC18",
    "EASLEY SC T20": "TWGSC20",
    "LAURENS SC T31": "TWGSC31",
    "VA73 LYNCHBURG": "TWGVA73",
    "S LABURNUM T48": "TWGVA48",
    "STAPLES MILL": "TWGVA67",
    "NINE MILE": "TWGVA65",
    "7223 HULL ST T45": "TWGVA45",
    "CHESTER VA": "TWGVA64",
    "VA68 CHAMABERLAYNE": "TWGVA68",
    "VA 69 JUNCTION": "TWGVA69",
    "VA70 PLANK": "TWGVA70",
    "VA71 RIO": "TWGVA71",
    "VA72 W MAIN": "TWGVA72",
    "W BROAD ST T47": "TWGVA47",
    "BATTLEFIELD BLVD": "TWGVA59",
    "GEORGE W. VA T25": "TWGVA25",
    "KECOUGHTAN VA T26": "TWGVA26",
    "NORFOLK VA T27": "TWGVA27",
    "VIRGINIA BEACH T40": "TWGVA40",
    "GREAT NECK RD": "TWGVA60",
    "J CLYDE MORRIS": "TWGVA63",
    "NEWMARKET DR": "TWGVA62",
    "HIGH ST VA T24": "TWGVA24",
    "ABERDEEN VA T28": "TWGVA28",
    "WARWICK BLVD": "TWGVA61",
    "WEST MERCURY BLVD 2": "TWGVA58"
}

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 TWG Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u] == p:
            st.session_state.logged_in = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Wrong credentials")

    st.stop()

if not st.session_state.logged_in:
    login()

# ---------------- LOGOUT ----------------
st.sidebar.write(f"👤 {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top,#0b1220,#020617);
    color:white;
}
div.stButton > button {
    background: linear-gradient(90deg,#00ffcc,#3b82f6);
    color:black;
    font-weight:bold;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📊 TWG Store Dashboard")

raw_data = st.text_area("📥 Paste Raw Data", height=250)

# ---------------- FUNCTIONS ----------------
def normalize(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

def match(store, data):
    best = ""
    best_score = 0

    for r, t in data.items():
        score = fuzz.partial_ratio(normalize(store), normalize(r))
        if score > best_score and score >= 70:
            best_score = score
            best = t

    return best

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not raw_data:
        st.warning("Please paste raw data")
        st.stop()

    lines = raw_data.splitlines()

    extracted = {}
    current = None

    time_pattern = r'^\d{1,2}:\d{2}\s?(AM|PM|am|pm)?$'

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if re.match(time_pattern, line):
            if current:
                extracted[current] = line
            continue

        current = line

    results = []

    for store, sid in STORE_MAP.items():
        t = match(store, extracted)

        results.append({
            "Store Name": store,
            "Store ID": sid,
            "Time": t if t else "❌ Missing"
        })

    df = pd.DataFrame(results)

    col1, col2 = st.columns(2)
    col1.metric("Total Stores", len(df))
    col2.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode(),
        "twg_report.csv",
        "text/csv"
    )
