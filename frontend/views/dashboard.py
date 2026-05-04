import streamlit as st
import datetime

from api.client import api_get
from utils.helpers import render_page_header

def parse_date_safe(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None
# -------------------------------
# DASHBOARD
# -------------------------------
def dashboard_page():
    render_page_header("Dashboard", "Clinic overview and upcoming tasks")

    # -------------------------------
    # SESSION STATE
    # -------------------------------
    st.session_state.setdefault("show_labs_due", False)
    st.session_state.setdefault("show_payments_due", False)

    # -------------------------------
    # FETCH DATA
    # -------------------------------
    all_patients = api_get("/patients", default=[])
    all_labs = api_get("/labs", default=[])
    all_payments = api_get("/payments", default=[])

    today = datetime.date.today()

    # -------------------------------
    # PATIENT MAP
    # -------------------------------
    patient_map = {
        str(p["patient_uuid"]): f"{p['first_name']} {p['last_name']}"
        for p in all_patients
    }

    # -------------------------------
    # LABS DUE
    # -------------------------------
    due_labs = []

    for lab in all_labs:
        next_due = lab.get("next_due_date")
        if next_due:
            try:
                due_date = datetime.datetime.strptime(next_due, "%Y-%m-%d").date()
                if due_date <= today + datetime.timedelta(days=7):
                    due_labs.append(lab)
            except:
                continue

    due_labs.sort(
        key=lambda lab: datetime.datetime.strptime(lab["next_due_date"], "%Y-%m-%d")
    )

    # -------------------------------
    # PAYMENTS DUE
    # -------------------------------
    due_payments = []

    for p in all_payments:
        next_due = p.get("next_payment_due")
        if next_due:
            try:
                due_date = datetime.datetime.strptime(next_due, "%Y-%m-%d").date()
                if due_date <= today + datetime.timedelta(days=7):

                    due_payments.append(p)
            except:
                continue

    due_payments.sort(
        key=lambda p: datetime.datetime.strptime(p["next_payment_due"], "%Y-%m-%d")
    )

    # -------------------------------
    # COUNTS
    # -------------------------------
    patient_count = len(all_patients)
    lab_count = len(due_labs)
    payment_count = len(due_payments)

    # -------------------------------
    # DASHBOARD CARDS
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    # PATIENTS
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Active Patients</div>
            <div class="metric-value">{patient_count}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Patients", key="dashboard_patients"):
            st.session_state["pending_page"] = "👤 Patients"
            st.rerun()

    # LABS
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Labs Due</div>
            <div class="metric-value">{lab_count}</div>
        </div>
        """, unsafe_allow_html=True)

        for lab in due_labs[:3]:
            patient_uuid = str(lab["patient_uuid"])
            name = patient_map.get(patient_uuid, "Unknown")

            due_date = datetime.datetime.strptime(lab["next_due_date"], "%Y-%m-%d").date()
            days_until = (due_date - today).days

            label = "🔴 Overdue" if days_until < 0 else f"🟡 {days_until}d"
            lab_type = lab.get("lab_type", "Lab")

            st.caption(f"• {name} — {lab_type} — {label}")

        if st.button("View Labs", key="dashboard_labs"):
            st.session_state["show_labs_due"] = not st.session_state["show_labs_due"]

    # PAYMENTS
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Payments Due</div>
            <div class="metric-value">{payment_count}</div>
        </div>
        """, unsafe_allow_html=True)

        for p in due_payments[:3]:
            patient_uuid = str(p["patient_uuid"])
            name = patient_map.get(patient_uuid, "Unknown")

            due_date = datetime.datetime.strptime(p["next_payment_due"], "%Y-%m-%d").date()
            days_until = (due_date - today).days

            label = "🔴 Overdue" if days_until < 0 else f"🟡 {days_until}d"
            payment_type = p.get("payment_type", "Payment")

            st.caption(f"• {name} — {payment_type} — {label}")

        if st.button("View Payments", key="dashboard_payments"):
            st.session_state["show_payments_due"] = not st.session_state["show_payments_due"]

    # -------------------------------
    # EXPANDED LISTS
    # -------------------------------
    st.markdown("---")

    # LAB LIST
    if st.session_state["show_labs_due"]:
        st.markdown("### 🧪 Patients with Labs Due")

        if not due_labs:
            st.success("No labs due 🎉")
        else:
            for i, lab in enumerate(due_labs):  # ✅ FIXED ENUMERATE
                patient_uuid = str(lab["patient_uuid"])
                name = patient_map.get(patient_uuid, "Unknown")

                due_date = datetime.datetime.strptime(lab["next_due_date"], "%Y-%m-%d").date()
                days_until = (due_date - today).days

                label = "🔴 Overdue" if days_until < 0 else f"🟡 {days_until} days"

                if st.button(
                    f"{name} • {lab.get('lab_type', 'Lab')} • {label}",
                    key=f"lab_{patient_uuid}_{i}"  # ✅ UNIQUE KEY
                ):
        
                
                    st.session_state["selected_patient"] = patient_uuid
                    st.session_state["pending_page"] = "👤 Patients"
                    st.rerun()

    # PAYMENT LIST
    if st.session_state["show_payments_due"]:
        st.markdown("### 💰 Patients with Payments Due")

        if not due_payments:
            st.success("No payments due 🎉")
        else:
            for i, p in enumerate(due_payments):  # ✅ FIXED ENUMERATE
                patient_uuid = str(p["patient_uuid"])
                name = patient_map.get(patient_uuid, "Unknown")

                due_date = datetime.datetime.strptime(p["next_payment_due"], "%Y-%m-%d").date()
                days_until = (due_date - today).days

                label = "🔴 Overdue" if days_until < 0 else f"🟡 {days_until} days"
                payment_type = p.get("payment_type", "Payment")

                if st.button(
                    f"{name} • {payment_type} • {label}",
                    key=f"payment_{patient_uuid}_{i}"  # ✅ UNIQUE KEY
                ):
                    st.session_state["selected_patient"] = patient_uuid
                    st.session_state["pending_page"] = "👤 Patients"
                    st.rerun()
