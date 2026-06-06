import streamlit as st
import pandas as pd
import re

# ---------------- PAGE ----------------
st.set_page_config(page_title="TWG SmartOps PRO", layout="wide")

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

# ---------------- ALIASES (GAME CHANGER) ----------------
STORE_ALIASES = {
    "VA 69 JUNCTION": "ASHLAND",
    "W FRANKLIN T42": "GASTONIA",
    "WOODRUFF GA": "WOODRUFF",
    "MILGEN GA": "MILGEN",
    "LANCASTER SC": "LANCASTER",
    "ROXIE STREET": "ROXIE ST",
}

# ---------------- CLEAN FUNCTION ----------------
def clean_text(text):
    text = str(text).upper()

    text = re.sub(r'\bNC\b|\bVA\b|\bGA\b|\bSC\b', ' ', text)
    text = re.sub(r'\bSTORE\b|\bSHIFT\b|\bCLOCK\b|\bIN\b|\bOUT\b', ' ', text)
    text = re.sub(r'\d+', ' ', text)

    text = re.sub(r'[^A-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# ---------------- MATCH FUNCTION (FINAL LOGIC) ----------------
def match_store(text):
    text = clean_text(text)

    # 1. ALIAS CHECK (MOST IMPORTANT)
    for alias, real_store in STORE_ALIASES.items():
        if alias in text:
            return real_store

    best_match = "UNMATCHED"
    best_score = 0

    for store in STORE_DATA:

        s = clean_text(store)

        # 2. DIRECT MATCH
        if s in text:
            return store

        # 3. WORD MATCH
        score = len(set(text.split()) & set(s.split()))

        # BOOST for first word match
        if s.split() and s.split()[0] in text:
            score += 2

        if score > best_score:
            best_score = score
            best_match = store

    # LOW THRESHOLD (important)
    if best_score >= 1:
        return best_match

    return "UNMATCHED"

# ---------------- UI ----------------
st.title("🚀 TWG SmartOps PRO SYSTEM")

st.markdown("## 📥 Paste Raw Data")

raw_data = st.text_area("Raw Input", height=300)

# ---------------- PROCESS ----------------
if st.button("🚀 RUN SYSTEM"):

    lines = [l.strip() for l in raw_data.splitlines() if l.strip()]

    final = []

    for line in lines:

        matched = match_store(line)

        if matched in STORE_DATA:
            sid = STORE_DATA[matched]["id"]
            dm = STORE_DATA[matched]["dm"]
        else:
            sid = ""
            dm = ""

        final.append({
            "Input": line,
            "Store Name": matched,
            "Store ID": sid,
            "DM": dm
        })

    df = pd.DataFrame(final)

    st.success("Processing Completed 🚀")

    st.metric("Total Records", len(df))

    st.dataframe(df, use_container_width=True)

    # DOWNLOAD
    csv = df.to_csv(index=False).encode()

    st.download_button(
        "⬇ Download Report",
        csv,
        "twg_final_report.csv",
        "text/csv"
    )
