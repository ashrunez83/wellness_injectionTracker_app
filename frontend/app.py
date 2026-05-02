import streamlit as st

# -------------------------------
# SAFE IMPORTS (PREVENT CRASH)
# -------------------------------
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

# 🔹 TEMP (later from login / DB)
CLINIC_NAME = "Copper Rock Clinic"

# 🔹 Page Config
st.set_page_config(
    page_title=f"{CLINIC_NAME} | Orelia",
    page_icon="✨",
    layout="wide",
)

st.title("Orelia ✨")
st.subheader("Copper Rock Wellness Dashboard")
st.success("App is live")
# 🔹 Luxury Header
st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding: 12px 0;
    ">
        <div>
            <h1 style="margin:0; font-weight:600; letter-spacing:-0.5px;">
                {CLINIC_NAME}
            </h1>
            <p style="margin:0; color:#9A9A9A; font-size:14px;">
                Patient Management Dashboard
            </p>
        </div>
        <div style="text-align:right;">
            <p style="margin:0; font-size:12px; color:#B0B0B0;">
                Powered by
            </p>
            <p style="margin:0; font-size:20px; font-weight:500; letter-spacing:0.5px;">
                Orelia
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

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
# SESSION STATE
# -------------------------------
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
    # Add controlled vertical spacing (clean + predictable)
    st.markdown("<div style='margin-top: 4vh;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        render_page_header("Copper Rock Clinic", "Patient Tracking System")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")

        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if username == "admin" and password == "admin123":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid credentials")

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