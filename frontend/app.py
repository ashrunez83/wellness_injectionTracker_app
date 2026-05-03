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
# LOGIN PAGE
# -------------------------------
def login_page():
    st.markdown("""
        <style>
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 75vh;
            }

            .login-card {
                width: 380px;
                padding: 40px 36px;
                border-radius: 20px;
                background: #FFFFFF;
                box-shadow: 0 12px 30px rgba(0,0,0,0.05);
                border: 1px solid #E8E1D5;
                text-align: center;
            }

            .login-brand {
                font-family: 'Playfair Display', serif;
                font-size: 1.8rem;
                margin-bottom: 6px;
                color: #2E2A26;
            }

            .login-subtitle {
                font-size: 0.9rem;
                color: #7A6F66;
                margin-bottom: 24px;
            }

            .stTextInput input {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-brand">Orelia ✨</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; margin-bottom:6px;">
            <div style="font-size:1rem; font-weight:600; color:#2E2A26;">
                Copper Rock Clinic
            </div>
            <div style="font-size:12px; color:#9A9A9A; margin-top:4px;">
                Secure access portal
            </div>
        </div>
        """, unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="
        position: fixed;
        bottom: 20px;
        right: 30px;
        text-align: right;
        font-family: 'Inter', sans-serif;
    ">
        <div style="font-size: 14px; font-weight: 500; color:#2E2A26;">
            Orelia ✨
        </div>
        <div style="font-size: 11px; color:#9A9A9A;">
            Clinic Management Systems
        </div>
    </div>
    """, unsafe_allow_html=True)
# -------------------------------
# MAIN APP FLOW
# -------------------------------
# -------------------------------
# LOGIN GATE
# ------------------------------
if not st.session_state["logged_in"]:
    login_page()
    st.stop()


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