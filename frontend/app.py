import streamlit as st

# -------------------------------
# SAFE IMPORTS (PREVENT CRASH)
# -------------------------------

# 🔹 TEMP (later from login / DB)
CLINIC_NAME = "Copper Rock Clinic"

# 🔹 Page Config
st.set_page_config(
    page_title=f"{CLINIC_NAME} | Orelia",
    page_icon="✨",
    layout="wide",
)

st.markdown("""
<style>
    body {
        background-color: #FAFAFA;
    }

    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        letter-spacing: -0.4px;
    }

    .stButton>button {
        border-radius: 12px;
        padding: 0.5rem 1.2rem;
        border: 1px solid #E5E5E5;
    }

    .stTextInput>div>div>input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE DEFAULTS
# -------------------------------
def init_session_state():
    defaults = {
        "logged_in": False,
        "sidebar_page": "🏠 Dashboard",
        "editing_patient": False,
        "selected_patient": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# -------------------------------
# LOGIN PAGE
# -------------------------------
def login_page():
    st.markdown("""
        <style>
            /* -------------------------------
               BASE LAYOUT
            -------------------------------- */
            .block-container {
                padding-top: 2rem !important;
            }

            header[data-testid="stHeader"] {
                display: none;
            }

            div[data-testid="stToolbar"],
            div[data-testid="stDecoration"],
            div[data-testid="stStatusWidget"] {
                display: none !important;
            }

            /* -------------------------------
               BACKGROUND (soft luxury)
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
               CENTERING
            -------------------------------- */
            div[data-testid="column"] {
                display: flex;
                justify-content: center;
            }

            /* -------------------------------
               LOGIN CARD
            -------------------------------- */
            .login-card {
                width: 100%;
                max-width: 380px;
                padding: 40px 36px;
                border-radius: 20px;
                background: rgba(255,255,255,0.85);
                backdrop-filter: blur(8px);
                border: 1px solid #E8E1D5;
                box-shadow: 0 10px 30px rgba(0,0,0,0.04);
                text-align: center;
            }

            /* -------------------------------
               TYPOGRAPHY
            -------------------------------- */
            .login-brand {
                font-family: 'Playfair Display', serif;
                font-size: 1.8rem;
                font-weight: 600;
                margin-bottom: 6px;
                color: #2E2A26;
            }

            .login-clinic {
                font-size: 1rem;
                font-weight: 600;
                color: #2E2A26;
            }

            .login-sub {
                font-size: 12px;
                color: #8A8178;
                margin-bottom: 22px;
            }

            /* -------------------------------
               FORM
            -------------------------------- */
            div[data-testid="stForm"] {
                max-width: 300px;
                margin: 0 auto;
            }

            .stTextInput input {
                border-radius: 10px !important;
                border: 1px solid #E3D8C8 !important;
                padding: 10px !important;
            }

            /* -------------------------------
               BUTTON
            -------------------------------- */
            .stFormSubmitButton > button {
                background-color: #B97A4B !important;
                color: white !important;
                border-radius: 10px !important;
                padding: 0.5rem 1.2rem !important;
                border: none !important;
                width: 100%;
                margin-top: 8px;
            }

            .stFormSubmitButton > button:hover {
                background-color: #9C643B !important;
            }

            /* -------------------------------
               FOOTER
            -------------------------------- */
            .footer {
                position: fixed;
                bottom: 24px;
                right: 32px;
                font-size: 11px;
                color: #8A8178;
                text-align: right;
            }
        </style>
    """, unsafe_allow_html=True)

    # Center layout
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-brand">Orelia ✨</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-clinic">Copper Rock Clinic</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Secure access portal</div>', unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")

        if submitted:
            if username == "admin" and password == "admin123":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            <div style="font-weight:500;">Orelia ✨</div>
            <div>Clinic Management Systems</div>
        </div>
    """, unsafe_allow_html=True)


#---------------------
# MAIN APP FLOW
# -------------------------------
# -------------------------------
# LOGIN GATE
# ------------------------------
if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# apply global styles 
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

#Imports
try:
    from api.client import api_get, api_post, api_put, api_delete
    from views.dashboard import dashboard_page
    from views.patients import patients_page
    from views.inventory import inventory_page
    from styles.css import GLOBAL_CSS
    from utils.helpers import render_page_header
    IMPORT_SUCCESS = True
except Exception as e:
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

# -------------------------------
# SIDEBAR (ONLY AFTER LOGIN)
# -------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-logo">Copper Rock</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Clinic Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    page_options = ["🏠 Dashboard", "👤 Patients", "📦 Inventory"]

    current_page = st.session_state.get("sidebar_page", "🏠 Dashboard")

    page = st.radio(
        "Navigation",
        page_options,
        index=page_options.index(current_page),
        label_visibility="collapsed"
    )

    st.session_state["sidebar_page"] = page

    st.markdown("""
    <div class="sidebar-status-card">
        <div class="sidebar-status-title">System Status</div>
        <div class="sidebar-status-line"><strong>Logged in as:</strong> Admin</div>
        <div class="sidebar-status-line"><strong>Clinic:</strong> Copper Rock</div>
        <div class="sidebar-status-line"><strong>Status:</strong> <span class="sidebar-online">● Online</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

# ✅ RESET selected patient when leaving Patients page
if page != "👤 Patients":
    st.session_state["selected_patient"] = None

if page == "🏠 Dashboard":
    dashboard_page()
elif page == "👤 Patients":
    patients_page()
elif page == "📦 Inventory":
    inventory_page()