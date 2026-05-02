

GLOBAL_CSS = """
<style>

/* -------------------------------
   FONTS
-------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@300;400;500;600&display=swap');

/* -------------------------------
   BACKGROUND (lighter + airy)
-------------------------------- */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FCFAF6 0%, #F4EFE6 100%);
}

/* -------------------------------
   GLOBAL SPACING
-------------------------------- */
.block-container {
    padding-top: 3rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* -------------------------------
   TYPOGRAPHY (luxury feel)
-------------------------------- */
html, body {
    font-family: 'Inter', sans-serif;
    color: #2E2A26;
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 600;
    letter-spacing: -0.5px;
}

.brand-subtitle {
    color: #7A6F66;
    font-size: 0.95rem;
}

/* -------------------------------
   CARDS (lighter + softer)
-------------------------------- */
.metric-card,
.content-card,
.profile-card {
    background: #FFFFFF;
    border: 1px solid #E7DED0;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.03);
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
    width: auto !important;
    min-width: 140px;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #9C643B !important;
}

/* -------------------------------
   INPUTS (clean)
-------------------------------- */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #E3D8C8 !important;
}

/* -------------------------------
   SIDEBAR (more elegant gradient)
-------------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #B97A4B 0%, #8F5A36 100%);
    border-right: none;
}

.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 600;
}

/* -------------------------------
   METRIC VALUES (less aggressive)
-------------------------------- */
.metric-value {
    font-size: 2.2rem;
    font-weight: 600;
    color: #2E2A26;
}

/* -------------------------------
   REMOVE VISUAL CLUTTER
-------------------------------- */
header[data-testid="stHeader"] {
    background: transparent;
}

/* -------------------------------
   SUBTLE DIVIDERS
-------------------------------- */
hr {
    border: none;
    border-top: 1px solid #E8E1D5;
}

/* -------------------------------
   TABS (minimal + premium)
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

</style>
"""