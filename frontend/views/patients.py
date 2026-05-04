import streamlit as st
import datetime

from api.client import api_get, api_post, api_put
from utils.helpers import (
    render_data_section,
    render_add_payment_form,
    render_add_injection_form,
    render_add_lab_form,
    render_add_treatment_form,
    render_page_header,
    format_date_display,
    render_payments_section,
    render_injection_history_section,
    render_labs_section,
    render_treatments_section,
    render_scans_section,
    render_lab_reminders_section,
    render_schedule_section

)

# -------------------------------
# PATIENT SEARCH
# -------------------------------
def patient_search_page():
    st.subheader("Patient Search")

    with st.form("patient_search_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")

        submitted = st.form_submit_button("Search")

    if submitted:
        patients = api_get(
            f"/search_patients?first_name={first_name}&last_name={last_name}",
            default=[]
        )
        st.session_state["patients"] = patients

    patients = st.session_state.get("patients", [])


    # -------------------------------
    # RESULTS AS CARDS
    # -------------------------------
    if patients:
        st.markdown("### Results")

        for p in patients:
            patient_label = f"{p['first_name']} {p['last_name']}"

            col1, col2 = st.columns([6, 1])

            with col1:
                st.markdown(f"""
                <div class="patient-card">
                    <div class="patient-name">{patient_label}</div>
                    <div class="patient-meta">
                        📞 {p.get('phone', 'N/A')} &nbsp;&nbsp; | &nbsp;&nbsp;
                        ✉️ {p.get('email', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button("View", key=f"view_{p['patient_uuid']}"):
                    st.session_state["selected_patient"] = p["patient_uuid"]
                    st.session_state["patients"] = []  # ✅ CLEAR RESULTS
                    st.rerun()

    elif submitted and not patients:
        st.warning("No patients found")

    # -------------------------------
    # SELECTED PATIENT
    # -------------------------------
    if st.session_state.get("selected_patient"):
        st.markdown(f"""
        <div class="selected-patient-banner">
            Viewing Patient Record
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Back to Results", key="clear_selected_patient"):
            del st.session_state["selected_patient"]
            st.rerun()

        selected_patient_record()


# -------------------------------
# ADD PATIENT
# -------------------------------
def add_patient_page():
    st.subheader("Add New Patient")

    with st.form("add_patient_form"):
        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input("First Name").strip()
            last_name = st.text_input("Last Name").strip()
            dob = st.date_input(
                "Date of Birth",
                value=datetime.date(1990, 1, 1),
                min_value=datetime.date(1940, 1, 1),
                max_value=datetime.date.today()
            )

        with col2:
            phone = st.text_input("Phone")
            email = st.text_input("Email")

        submitted = st.form_submit_button("Save Patient")

    # -------------------------------
    # HANDLE SUBMIT
    # -------------------------------
    if submitted:

        # ✅ Basic validation (prevents silent fails)
        if not first_name or not last_name:
            st.error("First and Last Name are required ❌")
            return

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": dob.strftime("%Y-%m-%d"),
            "phone": phone,
            "email": email
        }

        response, result = api_post("/add_patient", payload)

        if response and response.status_code == 200 and "error" not in result:

            # ✅ SUCCESS STATE
            st.session_state["success_msg"] = "Patient saved successfully ✅"

            # ✅ OPTIONAL UX IMPROVEMENT
            # clears any selected patient + search state
            # clear ALL search state
            st.session_state["selected_patient"] = None
            st.session_state["patients"] = []   # 🔥 THIS FIXES SEARCH BUG
            st.rerun()

        else:
            st.error(f"Failed to save patient: {result.get('error', 'Unknown error')}")

# -------------------------------
# LOG INJECTION
# -------------------------------
def add_injection_page():
    st.subheader("Log Injection / Treatment")

    # -------------------------------
    # LOAD PATIENTS
    # -------------------------------
    patients = api_get("/patients", default=[])

    if not patients:
        st.info("No patients found.")
        return

    patient_options = {
        f"{p['first_name']} {p['last_name']}": p["patient_uuid"]
        for p in patients
    }

    patient_name = st.selectbox("Select Patient", list(patient_options.keys()))
    patient_uuid = patient_options[patient_name]

    # -------------------------------
    # LOAD INVENTORY
    # -------------------------------
    inventory = api_get("/inventory", default=[])

    if not inventory:
        st.warning("No inventory available.")
        return

    med_options = {
        f"{item['item_name']} • Lot {item['lot_number']}": item
        for item in inventory
    }

    selected_label = st.selectbox(
        "Select Medication",
        ["-- Select Medication --"] + list(med_options.keys())
    )

    if selected_label == "-- Select Medication --":
        st.info("Select a medication to continue")
        return

    selected_med = med_options[selected_label]

    # -------------------------------
    # SAFE VARIABLES (FIXES ALL ERRORS)
    # -------------------------------
    drug_name = selected_med.get("item_name")
    lot_number = selected_med.get("lot_number")
    available_qty = float(selected_med.get("quantity", 0))
    ml_per_vial = selected_med.get("ml_per_vial") or 1
    mg_per_ml = selected_med.get("mg_per_ml") or 0
    dose_unit_key = f"injection_unit_{patient_uuid}_{lot_number}"

    # -------------------------------
    # DISPLAY CARD
    # -------------------------------
    st.markdown(f"""
    <div style="
        background:#F8F6F2;
        border:1px solid #E5DED3;
        border-radius:14px;
        padding:14px;
        margin-bottom:12px;
    ">
    <strong>{drug_name}</strong><br>
    Lot: {lot_number}<br>
    Available: {available_qty} vials<br>
    Vial Size: {ml_per_vial} mL
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # FORM
    # -------------------------------
    with st.form("injection_form_main"):

        col1, col2 = st.columns(2)

        with col1:
            unit = st.selectbox("Dose Unit", ["mL", "units"], key=dose_unit_key)
            if unit == "units":
                dose = st.number_input(
                    "Dose (units)",
                    min_value=0.0,
                    step=1.0,
                    value=25.0,
                    format="%.2f",
                    key=f"injection_dose_units_{patient_uuid}_{lot_number}"
                )
                dose_ml = dose / 100
            else:
                dose = st.number_input(
                    "Dose (mL)",
                    min_value=0.0,
                    step=0.01,
                    value=0.25,
                    format="%.2f",
                    key=f"injection_dose_ml_{patient_uuid}_{lot_number}"
                )
                dose_ml = dose
            injection_date = st.date_input("Injection Date")

        with col2:
            notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Injection")

    # -------------------------------
    # LIVE PREVIEW
    # -------------------------------
    if dose > 0 and ml_per_vial:
        vial_usage = dose_ml / ml_per_vial
        remaining = available_qty - vial_usage

        st.markdown(f"""
        <div style="
            background:#FFFFFF;
            border:1px solid #E5DED3;
            border-radius:12px;
            padding:12px;
            margin-top:8px;
        ">
        <strong>After Injection:</strong><br>
        Dose: {dose:g} {unit} ({dose_ml:.2f} mL)<br>
        Used: {vial_usage:.3f} vial(s)<br>
        Remaining: <span style="color:#B97A4B;font-weight:700;">
            {max(remaining, 0):.3f} vials
        </span>
        </div>
        """, unsafe_allow_html=True)

        if vial_usage > available_qty:
            st.error("Dose exceeds inventory ❌")

    # -------------------------------
    # SUBMIT
    # -------------------------------
    if submitted:

        if dose <= 0:
            st.error("Dose must be greater than 0 ❌")
            return

        payload = {
            "patient_uuid": patient_uuid,
            "drug_name": drug_name,
            "lot_number": lot_number,
            "dose": dose,
            "unit": unit,
            "injection_date": str(injection_date),
            "frequency_days": None,
            "date_paid": None,
            "labs_done": False,
            "lab_date": None,
            "weight": None,
            "notes": notes
        }

        response, result = api_post("/add_injection", payload)

        if response and response.status_code == 200 and "error" not in result:
            st.session_state["injection_success"] = "Injection saved ✅"
            st.rerun()
        else:
            st.error(result.get("error"))
# -------------------------------
# SELECTED PATIENT RECORD
# -------------------------------
def selected_patient_record():

    if "selected_patient" not in st.session_state:
        return

    patient_uuid = st.session_state["selected_patient"]

    for key in [
        "patient_update_success",
        "injection_success",
        "lab_success",
        "treatment_success",
        "scan_success",
    ]:
        if key in st.session_state:
            st.success(st.session_state[key])
            del st.session_state[key]

    # -------------------------------
    # LOAD ALL DATA (FIXES EVERYTHING)
    # -------------------------------
    patient_info = api_get(f"/patient_detail/{patient_uuid}", default=[])

    if st.session_state.get("refresh_injections"):

        st.session_state["refresh_injections"] = False

    injections = api_get("/injection_history", default=[])
    injection_schedule = api_get("/injection_schedule", default=[])
    treatments = api_get("/treatments", default=[])
    labs = api_get("/labs", default=[])
    lab_reminders = api_get("/lab_reminders", default=[])
    payments = api_get("/payments", default=[])
    scans = api_get("/body_scans", default=[])

    # -------------------------------
    # FILTER BY PATIENT
    # -------------------------------
    injections = [
        i for i in injections
        if str(i.get("patient_uuid")) == str(patient_uuid)
    ]

    injection_schedule = [i for i in injection_schedule if i["patient_uuid"] == patient_uuid]
    treatments = [t for t in treatments if t["patient_uuid"] == patient_uuid]
    labs = [l for l in labs if l["patient_uuid"] == patient_uuid]
    lab_reminders = [l for l in lab_reminders if l["patient_uuid"] == patient_uuid]
    payments = [p for p in payments if p["patient_uuid"] == patient_uuid]
    scans = [s for s in scans if s["patient_uuid"] == patient_uuid]

    if not patient_info:
        st.warning("Patient not found")
        return

    p = patient_info[0]

    patient_name = f"{p['first_name']} {p['last_name']}"

    # -------------------------------
    # ALERT LOGIC
    # -------------------------------
    today = datetime.datetime.now()

    lab_alert = None
    for lab in labs:
        if lab.get("next_due_date"):
            due = datetime.datetime.fromisoformat(lab["next_due_date"])
            days = (due - today).days

            if days < 0:
                lab_alert = "⚠️ Lab Overdue"
            elif days <= 7:
                lab_alert = f"🧪 Lab due in {days} days"

    payment_alert = None
    for pay in payments:
        if pay.get("next_payment_due"):
            due = datetime.datetime.fromisoformat(pay["next_payment_due"])
            days = (due - today).days

            if days < 0:
                payment_alert = "💰 Payment Overdue"
            elif days <= 7:
                payment_alert = f"💰 Payment due in {days} days"

    # -------------------------------
    # HEADER
    # -------------------------------
    st.markdown(f"## {patient_name}")

    if lab_alert:
        st.warning(lab_alert)

    if payment_alert:
        st.warning(payment_alert)

    # -------------------------------
    # TESTOSTERONE TRACKING (FIXED)
    # -------------------------------
    pre_lab_date_value = None
    testosterone_value = 0.0

    if p.get("pre_lab_date"):
        try:
            pre_lab_date_value = datetime.datetime.strptime(
                p["pre_lab_date"], "%Y-%m-%d"
            ).date()
        except:
            pass

    if p.get("testosterone_level"):
        testosterone_value = float(p["testosterone_level"])

    st.markdown("### 🧪 Testosterone Tracking")

    col1, col2 = st.columns(2)

    with col1:
        pre_lab_date = st.date_input(
            "Pre-Lab Date",
            value=pre_lab_date_value
        )

    with col2:
        testosterone_level = st.number_input(
            "Testosterone Level",
            value=testosterone_value,
            min_value=0.0
        )

    if st.button("💾 Save Testosterone Data"):
        payload = {
            "first_name": p["first_name"],
            "last_name": p["last_name"],
            "date_of_birth": p["date_of_birth"],
            "phone": p["phone"],
            "email": p["email"],
            "pre_lab_date": str(pre_lab_date),
            "testosterone_level": testosterone_level
        }

        response, result = api_put(f"/update_patient/{patient_uuid}", payload)

        if response and response.status_code == 200 and "error" not in result:
            st.session_state["patient_update_success"] = "Patient data saved ✅"
            st.rerun()
        else:
            st.error(result.get("error"))

    # -------------------------------
    # TABS (ALL VARIABLES NOW EXIST)
    # -------------------------------
    tabs = st.tabs([
        "Injections",
        "Payments",
        "Labs",
        "Treatments",
        "Scans"
    ])

    # -------------------------------
    # INJECTIONS TAB
    # -------------------------------
    with tabs[0]:
        render_injection_history_section(
            injections,
            injection_schedule,
            patient_uuid,
            patient_name
        )

    # -------------------------------
    # PAYMENTS TAB
    # -------------------------------
    with tabs[1]:
        render_payments_section(
            payments,
            patient_uuid,
            patient_name
        )

    # -------------------------------
    # LABS TAB
    # -------------------------------
    with tabs[2]:
        render_labs_section(
            labs,
            lab_reminders,
            patient_uuid
        )

    # -------------------------------
    # TREATMENTS TAB
    # -------------------------------
    with tabs[3]:
        render_treatments_section(
            treatments,
            patient_uuid
        )

    # -------------------------------
    # SCANS TAB
    # -------------------------------
    with tabs[4]:
        render_scans_section(scans,patient_uuid)
# -------------------------------
# PATIENTS PAGE
# -------------------------------
def patients_page():
    render_page_header("Patient Management", "Search records, add patients, and log treatments")

    for key in ["success_msg", "injection_success"]:
        if key in st.session_state:
            st.success(st.session_state[key])
            del st.session_state[key]

    tab1, tab2, tab3 = st.tabs([
        "🔎 Patient Search",
        "➕ Add Patient",
        "💉 Log Injection",
    ])

    with tab1:
        patient_search_page()

    with tab2:
        add_patient_page()

    with tab3:
        add_injection_page()
