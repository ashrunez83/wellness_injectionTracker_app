import streamlit as st

# -------------------------------
# CONFIG
# -------------------------------
CLINIC_NAME = "Copper Rock Clinic"

st.set_page_config(
    page_title=f"{CLINIC_NAME} | Orelia",
    page_icon="✨",
    layout="wide",
)

# -------------------------------
# SESSION STATE
# -------------------------------
def init_session_state():
    defaults = {
        "logged_in": False,
        "sidebar_page": "🏠 Dashboard",
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

/* Remove Streamlit junk */
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    display: none !important;
}

/* 🔥 SINGLE SOURCE OF TRUTH FOR SPACING */
.block-container {
    padding-top: 0 !important;
}

/* Remove hidden wrapper spacing */
section.main > div {
    padding-top: 0 !important;
}

/* Kill phantom top space */
div[data-testid="stAppViewContainer"] > div:first-child {
    margin-top: -20px;
}

/* Background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(
        circle at 50% 30%,
        #FFFFFF 0%,
        #F6F1E8 60%,
        #EFE7DA 100%
    );
}

/* Center layout */
div[data-testid="column"] {
    display: flex;
    justify-content: center;
}

/* LOGIN CARD */
.login-card {
    width: 100%;
    max-width: 360px;
    padding: 32px 28px;
    border-radius: 18px;
    background: rgba(255,255,255,0.95);
    border: 1px solid #E8E1D5;
    box-shadow: 0 20px 50px rgba(0,0,0,0.06);
    backdrop-filter: blur(6px);
}

/* Titles */
.login-clinic {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2E2A26;
    margin-bottom: 2px;
}

.login-sub {
    font-size: 12px;
    color: #9A9A9A;
    margin-bottom: 20px;
}

/* Inputs */
.stTextInput input {
    height: 38px !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    border: 1px solid #E3D8C8 !important;
    padding: 6px 10px !important;
}

/* Button */
.stFormSubmitButton > button {
    background-color: #B97A4B !important;
    color: white !important;
    border-radius: 10px !important;
    width: 120px !important;
    height: 36px;
    font-size: 14px;
    border: none !important;
}

.stFormSubmitButton > button:hover {
    background-color: #9C643B !important;
}

/* Footer */
.footer {
    position: fixed;
    bottom: 20px;
    right: 30px;
    font-size: 12px;
    color: #9A9A9A;
    text-align: right;
}

</style>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown(f'<div class="login-clinic">{CLINIC_NAME}</div>', unsafe_allow_html=True)
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

    st.markdown("""
        <div class="footer">
            <div style="font-weight:500;">Powered by Orelia ✨</div>
            <div>Clinic Management Systems</div>
        </div>
    """, unsafe_allow_html=True)

# -------------------------------
# LOGIN GATE
# -------------------------------
if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# -------------------------------
# AFTER LOGIN (APP LOADS HERE)
# -------------------------------

# ✅ ONLY NOW apply global styling
from styles.css import GLOBAL_CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# -------------------------------
# IMPORT APP PAGES
# -------------------------------
from views.dashboard import dashboard_page
from views.patients import patients_page
from views.inventory import inventory_page

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.markdown("### Copper Rock")
    
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "👤 Patients", "📦 Inventory"],
        label_visibility="collapsed"
    )

    if st.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

# -------------------------------
# ROUTING
# -------------------------------
if page == "🏠 Dashboard":
    dashboard_page()
elif page == "👤 Patients":
    patients_page()
elif page == "📦 Inventory":
    inventory_page()