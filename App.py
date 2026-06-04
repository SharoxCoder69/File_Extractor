import streamlit as st
import pandas as pd
import re

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG Store Intelligence",
    page_icon="📊",
    layout="wide"
)

# ---------------- USERS ----------------
USERS = {
    "admin": "1234",
    "twg": "password",
    "manager": "admin123"
}

# ---------------- STORE MAP ----------------
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
def login_page():
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
    login_page()

# ---------------- LOGOUT ----------------
st.sidebar.write(f"👤 {st.session_state.user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: white;
}
textarea {
    border-radius: 10px !important;
}
.stButton > button {
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    color: white;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📊 TWG Store Intelligence Dashboard")
st.markdown(f"Welcome **{st.session_state.user}**")

st.markdown("---")

# ---------------- INPUTS ----------------
raw_data = st.text_area("📥 Raw Data", height=250)

# ---------------- NORMALIZE FUNCTION (FIX) ----------------
def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# ---------------- PROCESS ----------------
if st.button("🚀 Generate Report"):

    if not raw_data:
        st.warning("Add raw data")
        st.stop()

    raw_lines = [r.strip() for r in raw_data.splitlines() if r.strip()]

    time_pattern = r'^\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)$'

    extracted = {}
    current = None

    for line in raw_lines:

        if re.match(time_pattern, line):
            if current:
                extracted[current.upper()] = line
            continue

        current = line

    results = []

    # 🔥 SMART MATCHING FIX
    for store_name, store_id in STORE_MAP.items():

        store_clean = normalize(store_name)
        time_value = ""

        for raw_store, t in extracted.items():

            if store_clean in normalize(raw_store):
                time_value = t
                break

        results.append({
            "Store Name": store_name,
            "Store ID": store_id,
            "Time": time_value if time_value else "❌ Missing"
        })

    df = pd.DataFrame(results)

    st.metric("Total Stores", len(df))
    st.metric("Matched", len(df[df["Time"] != "❌ Missing"]))

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "twg_report.csv",
        "text/csv"
    )
