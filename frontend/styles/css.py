

GLOBAL_CSS = """
<style>

/* -------------------------------
   FONTS
-------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@300;400;500;600&display=swap');

/* -------------------------------
   APP BACKGROUND (match login)
-------------------------------- */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(
        circle at 50% 30%,
        #FFFFFF 0%,
        #F6F1E8 60%,
        #EFE7DA 100%
    );
}

/* -------------------------------
   GLOBAL SPACING (tight + clean)
-------------------------------- */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* -------------------------------
   TYPOGRAPHY
-------------------------------- */
html, body {
    font-family: 'Inter', sans-serif;
    color: #2E2A26;
}

h1, h2, h3 {
    letter-spacing: -0.3px;
    font-weight: 600;
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
}

/* -------------------------------
   CARDS (SOFT LUXURY CORE)
-------------------------------- */
.metric-card,
.content-card,
.profile-card,
.section-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(6px);
    border: 1px solid #E8E1D5;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    transition: all 0.15s ease;
}

.metric-card:hover,
.content-card:hover,
.profile-card:hover {
    transform: translateY(-2px);
}

/* -------------------------------
   BUTTONS (refined)
-------------------------------- */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #B97A4B !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #9C643B !important;
}

/* -------------------------------
   INPUTS (clean + premium)
-------------------------------- */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #E3D8C8 !important;
    padding: 8px !important;
}

/* -------------------------------
   SIDEBAR (luxury tone)
-------------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #B97A4B 0%, #8F5A36 100%);
    border-right: none;
}

section[data-testid="stSidebar"] * {
    color: #F8F6F2 !important;
}

.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
}

/* -------------------------------
   METRIC VALUES
-------------------------------- */
.metric-value {
    font-size: 2rem;
    font-weight: 600;
    color: #2E2A26;
}

/* -------------------------------
   DIVIDERS
-------------------------------- */
hr {
    border: none;
    border-top: 1px solid #E8E1D5;
}

/* -------------------------------
   TABLES / DATA
-------------------------------- */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #E8E1D5;
    overflow: hidden;
}

/* -------------------------------
   TABS (minimal premium)
-------------------------------- */
button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #7A6F66 !important;
    font-weight: 500 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #B97A4B !important;
    border-bottom: 2px solid #B97A4B !important;
}

/* -------------------------------
   REMOVE STREAMLIT CLUTTER
-------------------------------- */
header[data-testid="stHeader"] {
    display: none;
}

div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    display: none !important;
}

</style>
"""