st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: #e5e7eb;
}

/* HEADER */
.header {
    text-align: center;
    padding: 18px;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* TITLE */
.title {
    font-size: 32px;
    font-weight: 800;
}

/* ---------------- 4D INPUT BOX STYLE ---------------- */
textarea {
    border-radius: 14px !important;
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.10) !important;

    /* 3D SHADOW EFFECT */
    box-shadow:
        0 10px 25px rgba(0,0,0,0.4),
        inset 0 0 10px rgba(255,255,255,0.03);

    transition: all 0.3s ease-in-out;
}

/* HOVER = FLOAT EFFECT */
textarea:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow:
        0 18px 35px rgba(0,0,0,0.6),
        0 0 20px rgba(37,99,235,0.2);
}

/* FOCUS = GLOW EFFECT */
textarea:focus {
    outline: none !important;
    border: 1px solid #06b6d4 !important;
    box-shadow:
        0 0 25px rgba(6,182,212,0.4),
        inset 0 0 10px rgba(255,255,255,0.05);
}

/* BUTTON 3D */
.stButton > button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    color: white;
    font-weight: 700;

    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 15px 35px rgba(37,99,235,0.4);
}

</style>
""", unsafe_allow_html=True)
