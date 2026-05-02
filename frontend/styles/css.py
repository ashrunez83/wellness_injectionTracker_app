

# -------------------------------
# GLOBAL STYLING
# -------------------------------
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');



/* 🔥 HIDE STREAMLIT DEFAULT MULTIPAGE NAV */
section[data-testid="stSidebarNav"] {
    display: none !important;
}
/* App background */
[data-testid="stAppViewContainer"] {
    background-color: #F7F3E8;
}

/* Main content */
.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100% !important;
}

/* Typography */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #2E2A26;
    margin-bottom: 0.25rem;
}

.brand-subtitle {
    font-size: 1rem;
    color: #6F655C;
    margin-bottom: 0.8rem;
}

.accent-line {
    width: 60px;
    height: 3px;
    background-color: #B97A4B;
    border-radius: 10px;
    margin-bottom: 1.5rem;
}

/* Inputs */
.stTextInput input, 
.stDateInput input, 
.stTextArea textarea,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
    border: 1px solid #D8CCBB !important;
    background-color: #FFFFFF !important;
    color: #2E2A26 !important;
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    background-color: #B97A4B !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.2rem !important;
    font-weight: 600 !important;
    width: 100%;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: #9C643B !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #A86A3E 0%, #8D5633 100%) !important;
    width: 270px !important;
    min-width: 270px !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.2rem;
}

.sidebar-subtitle {
    font-size: 0.95rem;
    color: #F4EDE6;
    margin-bottom: 1.2rem;
}

.sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,0.12);
    margin: 1rem 0 1.2rem 0;
}

/* Sidebar radio */
div[role="radiogroup"] label {
    background-color: transparent !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
    border: 1px solid transparent !important;
}

div[role="radiogroup"] label:hover {
    background-color: rgba(255,255,255,0.10) !important;
}

div[role="radiogroup"] label[data-selected="true"] {
    background-color: rgba(255,255,255,0.18) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

div[role="radiogroup"] input[type="radio"] {
    display: none !important;
}

/* Sidebar status */
.sidebar-status-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 16px 14px;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.10);
}

.sidebar-status-title {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #F6EDE6;
    margin-bottom: 0.75rem;
    font-weight: 700;
}

.sidebar-status-line {
    font-size: 0.96rem;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
}

.sidebar-online {
    color: #A5F3A5 !important;
    font-weight: 700;
}

/* Dashboard cards */
.metric-card {
    background: #FDFBF6;
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #DDD3C4;
    box-shadow: 0 10px 24px rgba(0,0,0,0.05);
    min-height: 220px;
    margin-bottom: 1rem;
}

.metric-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #2E2A26;
    margin-bottom: 0.8rem;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #B97A4B;
    margin-bottom: 0.75rem;
}

.metric-subtext {
    font-size: 0.95rem;
    color: #7A6F66;
}

/* Patient cards */
.profile-card,
.content-card {
    background: #FDFBF6;
    border: 1px solid #DDD3C4;
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.04);
    margin-bottom: 1.2rem;
}

.section-title {
    font-size: 1.45rem;
    font-weight: 700;
    color: #2E2A26;
    margin-bottom: 1rem;
}

/* -------------------------------
   PATIENT SEARCH CARDS
-------------------------------- */
.patient-card {
    background: #FFFFFF;
    border: 1px solid #DDD3C4;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.15s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.04);
}

.patient-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(0,0,0,0.08);
    border-color: #C9B8A4;
}

.patient-name {
    font-weight: 700;
    font-size: 1.05rem;
    color: #2E2A26;
}

.patient-meta {
    font-size: 0.9rem;
    color: #7A6F66;
    margin-top: 4px;
}

/* Selected patient highlight */
.selected-patient-banner {
    background: linear-gradient(90deg, #B97A4B 0%, #A5693C 100%);
    color: white;
    padding: 14px 18px;
    border-radius: 14px;
    margin-bottom: 1.2rem;
    font-weight: 600;
}

/* Quick cards */
.quick-card {
    background: #FCFAF6;
    border: 1px solid #DDD3C4;
    border-radius: 18px;
    padding: 18px 20px;
    margin-bottom: 0.45rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    min-height: 118px;
    color: #2E2A26;
    transition: all 0.18s ease;
}

.quick-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.08);
    border-color: #CDBDAA;
}

.quick-card h4 {
    margin: 0 0 0.55rem 0;
    color: #7F4E2D;
    font-size: 1.08rem;
    font-weight: 700;
}

.quick-card p {
    margin: 0;
    color: #6E645C;
    font-size: 0.95rem;
    line-height: 1.45;
}

/* Action area spacing */
.action-button-wrap {
    margin-bottom: 1.15rem;
}

.action-button-wrap .stButton > button {
    width: auto !important;
    min-width: 160px;
    padding: 0.55rem 1rem !important;
    border-radius: 10px !important;
    background-color: #B97A4B !important;
    font-size: 0.95rem !important;
    box-shadow: none !important;
}

/* Optional section polish */
.patient-actions-heading {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2E2A26;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}
/* Inventory */
.summary-box {
    background: linear-gradient(180deg, #B77745 0%, #A5693C 100%);
    border-radius: 16px;
    padding: 18px;
    color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 18px;
}

.summary-title {
    font-size: 0.9rem;
    opacity: 0.85;
    margin-bottom: 4px;
}

.summary-value {
    font-size: 1.7rem;
    font-weight: 700;
}

.toolbar-box {
    background: #FDFBF6;
    border: 1px solid #DDD3C4;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

.section-card {
    background: #FDFBF6;
    border: 1px solid #DDD3C4;
    border-radius: 16px;
    padding: 18px;
    margin-top: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

/* Opened patient detail section */
.open-section-card {
    background: #FCFAF6;
    border: 1px solid #DDD3C4;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    margin-top: 1.5rem;
}

/* Patient workspace section */
.patient-workspace-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #2E2A26;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* Slightly smaller metric cards inside patient overview */
.metric-card {
    min-height: 180px;
}

/* Hide top header */
header[data-testid="stHeader"] {
    background: transparent;
}

    /* -------------------------------
       TABS - make Streamlit tabs visible
    -------------------------------- */
    button[data-baseweb="tab"] {
        background: #EFE7DA !important;
        border: 1px solid #D8CCBB !important;
        border-bottom: none !important;
        border-radius: 14px 14px 0 0 !important;
        padding: 0.75rem 1.2rem !important;
        margin-right: 0.35rem !important;
        color: #5F544C !important;
        font-weight: 600 !important;
        min-height: 48px !important;
    }

    button[data-baseweb="tab"]:hover {
        background: #F6EFE3 !important;
        color: #2E2A26 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        color: #B97A4B !important;
        border: 1px solid #D8CCBB !important;
        border-bottom: 3px solid #B97A4B !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.04);
    }

    div[data-baseweb="tab-list"] {
        gap: 0.25rem !important;
        border-bottom: 1px solid #DDD3C4 !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0 !important;
    }

    /* Payment form / workspace form polish */
    div[data-testid="stForm"] {
        background: #FCFAF6;
        border: 1px solid #DDD3C4;
        border-radius: 18px;
        padding: 18px 20px 8px 20px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    div[data-baseweb="tab-panel"] {
        padding-top: 0.5rem !important;
    }

    /* Inventory premium cards */
.inventory-stat-card {
    background: linear-gradient(180deg, #C4844A 0%, #B97743 100%);
    padding: 22px 18px;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}

.inventory-stat-label {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.92);
    margin-bottom: 0.45rem;
    font-weight: 500;
}

.inventory-stat-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: white;
}

.inventory-toolbar-card {
    background: #FCFAF6;
    border: 1px solid #DDD3C4;
    border-radius: 18px;
    padding: 18px 20px 8px 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    margin-bottom: 1.2rem;
}

.inventory-form-card {
    background: #FCFAF6;
    border: 1px solid #E1D7C9;
    border-radius: 18px;
    padding: 18px 20px 10px 20px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.04);
}

/* Inventory detail card */
.inventory-detail-card {
    background: #FCFAF6;
    border: 1px solid #DDD3C4;
    border-radius: 20px;
    padding: 22px 22px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    margin-bottom: 1.2rem;
}

.inventory-detail-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1.2rem;
}

.inventory-detail-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2E2A26;
    margin-bottom: 0.2rem;
}

.inventory-detail-subtitle {
    font-size: 0.95rem;
    color: #7B7066;
}

.inventory-detail-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
    color: #4B433D;
    font-size: 0.98rem;
}

.inventory-badge-low {
    background: #FFF0EA;
    color: #B5542E;
    border: 1px solid #F0C8B7;
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    white-space: nowrap;
}

.inventory-badge-ok {
    background: #EEF8F1;
    color: #2E7D32;
    border: 1px solid #CDE6D1;
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    white-space: nowrap;
}

.inventory-detail-card {
    margin-bottom: 1rem;
}

.inventory-form-card {
    margin-top: 0.5rem;
}

.inventory-badge-ok,
.inventory-badge-low {
    min-width: 90px;
    text-align: center;
}

/* Unified workspace shell */
.workspace-shell {
    background: #FDFBF6;
    border: 1px solid #DDD3C4;
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.04);
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}

/* Better inventory detail card */
.inventory-detail-card {
    background: #FFFFFF;
    border: 1px solid #E3D8C8;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    margin-bottom: 1.5rem;
}

/* Inventory tabs feel more premium */
button[data-baseweb="tab"] {
    border-radius: 12px 12px 0 0 !important;
    background: #F3EEE5 !important;
    color: #4B433D !important;
    padding: 10px 18px !important;
    font-weight: 600 !important;
    border: 1px solid #DDD3C4 !important;
    margin-right: 6px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: #FFFFFF !important;
    color: #B97A4B !important;
    border-bottom: 2px solid #B97A4B !important;
}

/* Better form card spacing */
.inventory-form-card {
    background: #FFFFFF;
    border: 1px solid #E3D8C8;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.03);
    margin-top: 1rem;
}

/* Make selectboxes feel clickable like real SaaS dropdowns */
div[data-baseweb="select"] {
    cursor: pointer !important;
}

div[data-baseweb="select"] * {
    cursor: pointer !important;
}

/* Dropdown value area */
div[data-baseweb="select"] > div {
    cursor: pointer !important;
}

/* Fix weird text-cursor behavior inside select labels/values */
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] div {
    cursor: pointer !important;
}

/* Empty state card */
.empty-state-card {
    background: #FDFBF6;
    border: 1px dashed #D8CCBB;
    border-radius: 18px;
    padding: 28px 24px;
    text-align: center;
    margin-top: 1rem;
    color: #6F655C;
}

.empty-state-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #2E2A26;
    margin-bottom: 0.4rem;
}

.empty-state-text {
    font-size: 0.95rem;
    color: #7A6F66;
}
</style>
"""

