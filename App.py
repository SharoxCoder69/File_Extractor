import streamlit as st
import pandas as pd
import re

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="TWG SmartOps SaaS",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}
h1 {
    text-align: center;
    color: #38bdf8;
}
.stButton>button {
    background: linear-gradient(90deg, #0ea5e9, #3b82f6);
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: bold;
    border: none;
}
.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 30px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 TWG SmartOps Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user and pwd:
            st.session_state.logged_in = True
        else:
            st.error("Enter credentials")

    st.stop()

# ---------------- STORE DATABASE ----------------
STORE_DATA = {
    "HICKORY": {"id": "TWGNC52", "dm": "Angie"},
    "BRAGG BLVD": {"id": "TWGNC56", "dm": "Ollivanza"},
    "CANNON": {"id": "TWGNC50", "dm": "Kindi"},
    "MOORESVILLE": {"id": "TWGNC53", "dm": "Angie"},
    "ROXIE ST": {"id": "TWGNC51", "dm": "Angie"},
    "CHERRY T42": {"id": "TWGSC42", "dm": "Kindi"},
    "SALISBURY": {"id": "TWGNC17", "dm": "Angie"},
    "LINCOLNTON": {"id": "TWGNC30", "dm": "Kindi"},
    "GASTONIA": {"id": "TWGNC42", "dm": "Angie"},
    "BURLINGTON": {"id": "TWGNC13", "dm": "Ollivanza"},
    "DURHAM": {"id": "TWGNC22", "dm": "Angie"},
    "RALEIGH": {"id": "TWGNC25", "dm": "Ollivanza"},
    "CHARLOTTE": {"id": "TWGNC10", "dm": "Kindi"},

    "ASHLAND": {"id": "TWGVA69", "dm": "Mekail"},
    "HULL STREET": {"id": "TWGVA72", "dm": "Mekail"},
    "WEST BROAD": {"id": "TWGVA73", "dm": "Mekail"},
    "VIRGINIA BEACH": {"id": "TWGVA74", "dm": "Mekail"},
    "HAMPTON": {"id": "TWGVA75", "dm": "Mekail"},
    "NORFOLK": {"id": "TWGVA76", "dm": "Mekail"},

    "LANCASTER": {"id": "TWGSC29", "dm": "Kindi"},
    "ROCK HILL": {"id": "TWGSC31", "dm": "Kindi"},
    "CHARLESTON": {"id": "TWGSC33", "dm": "Kindi"},

    "MILGEN": {"id": "TWGGA34", "dm": "Ollivanza"},
    "WOODRUFF": {"id": "TWGGA33", "dm": "Ollivanza"},
    "VICTORY DR": {"id": "TWGGA32", "dm": "Ollivanza"},
}

# ---------------- CLEAN ----------------
def clean_text(text):
    text = str(text).upper()
    text = re.sub(r'\bNC\b|\bVA\b|\bGA\b|\bSC\b', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[^A-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------- MATCH ----------------
def match_store(text):
    text = clean_text(text)

    best_match = None
    best_score = 0

    for store in STORE_DATA.keys():
        s = clean_text(store)

        if s in text or text in s:
            return store

        score = len(set(text.split()) & set(s.split()))

        if score > best_score:
            best_score = score
            best_match = store

    if best_score >= 1:
        return best_match

    return "UNMATCHED"

# ---------------- EXTRACT ----------------
def extract_store_time(raw):
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        match = re.search(r'(.+?)\s+(\d{1,2}:\d{2}\s?(AM|PM|am|pm)?)', line)
        if match:
            result.append((match.group(1), match.group(2)))
            i += 1
            continue

        if i + 1 < len(lines):
            t = re.search(r'\d{1,2}:\d{2}', lines[i+1])
            if t:
                result.append((line, t.group()))
                i += 2
                continue

        i += 1

    return result

# ---------------- UI ----------------
st.markdown("<h1>🚀 TWG SmartOps SaaS Dashboard</h1>", unsafe_allow_html=True)

st.markdown("### 📥 Raw Data Input Only")
raw_data = st.text_area("Paste Raw Data", height=300)

# ---------------- PROCESS ----------------
if st.button("🚀 Run System"):

    final = []

    for store_raw, time in extract_store_time(raw_data):

        matched = match_store(store_raw)

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
            "Time": time
        })

    df = pd.DataFrame(final)

    st.success("Processing Completed 🚀")
    st.metric("Total Records", len(df))

    st.dataframe(df, use_container_width=True)

    # DOWNLOAD ONLY
    csv = df.to_csv(index=False).encode()

    st.download_button(
        "⬇ Download CSV",
        csv,
        "twg_report.csv",
        "text/csv"
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
<div class='footer'>
Created by <b>Totallywirelessgroup</b><br>
Managed by <b>Sharoz Javaid</b>
</div>
""", unsafe_allow_html=True)
