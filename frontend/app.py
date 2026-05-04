import streamlit as st
from styles.css import GLOBAL_CSS

# -------------------------------
# SAFE IMPORTS (PREVENT CRASH)
# -------------------------------
st.write("TOP OF FILE")

# 🔹 TEMP (later from login / DB)
CLINIC_NAME = "Copper Rock Clinic"

# 🔹 Page Config
st.set_page_config(
    page_title=f"{CLINIC_NAME} | Orelia",
    page_icon="✨",
    layout="wide",
)

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

    st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
    st.markdown('<div class="login-root">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Copper Rock Clinic</div>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            <div style="font-weight:500;">Powered By Orelia ✨</div>
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

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

#Imports=
try:
    from api.client import api_get, api_post, api_put, api_delete
    from views.dashboard import dashboard_page
    from views.patients import patients_page
    from views.inventory import inventory_page
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