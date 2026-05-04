
import streamlit as st
import pandas as pd
import datetime

from api.client import api_post, api_get, api_put, api_delete

# -------------------------------
# FORMATTER
# -------------------------------
def format_date_display(date_value):
    if not date_value:
        return "N/A"
    try:
        if isinstance(date_value, str):
            date_value = datetime.datetime.strptime(date_value[:10], "%Y-%m-%d")
        return date_value.strftime("%m/%d/%Y")
    except:
        return str(date_value)

# -------------------------------
# PAGE HEADER
# -------------------------------
def render_page_header(title, subtitle):
    st.markdown(f'<div class="brand-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="brand-subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)

# -------------------------------
# GENERIC DATA TABLE
# -------------------------------
def render_data_section(title, data):
    st.markdown(f"### {title}")
    if not data:
        st.info(f"No {title.lower()} found.")
        return
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# -------------------------------
# PAYMENTS
# -------------------------------
def render_payments_section(payments, patient_uuid, patient_name):
    import pandas as pd

    st.markdown("### Payments")

    # -------------------------------
    # SESSION STATE
    # -------------------------------
    if "editing_payment" not in st.session_state:
        st.session_state["editing_payment"] = None

    if "show_payment_form" not in st.session_state:
        st.session_state["show_payment_form"] = False

    # -------------------------------
    # SUCCESS MESSAGE
    # -------------------------------
    if "payment_success" in st.session_state:
        st.success(st.session_state["payment_success"])
        del st.session_state["payment_success"]

    # -------------------------------
    # LIST VIEW
    # -------------------------------
    if not st.session_state["editing_payment"]:

        if not payments:
            st.info("No payments found.")
        else:
            for i, payment in enumerate(payments):
                payment_id = payment.get("payment_id")

                col1, col2 = st.columns([6, 1])

                with col1:
                    st.markdown(f"""
                    <div class="content-card">
                        💵 ${payment.get('amount')}<br>
                        📅 {payment.get('payment_date')}<br>
                        📝 {payment.get('notes', '')}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    if st.button("✏️ Edit", key=f"edit_payment_{payment_id}_{i}"):
                        st.session_state["editing_payment"] = payment
                        st.rerun()

    # -------------------------------
    # EDIT MODE
    # -------------------------------
    else:
        payment = st.session_state["editing_payment"]
        payment_id = payment.get("payment_id")

        st.markdown("### ✏️ Edit Payment")

        with st.form(f"edit_payment_form_{payment_id}"):

            amount = st.number_input(
                "Amount",
                value=float(payment.get("amount", 0)),
                min_value=0.0
            )

            date_paid = st.date_input(
                "Date Paid",
                value=pd.to_datetime(payment.get("payment_date")).date()
            )

            notes = st.text_area(
                "Notes",
                value=payment.get("notes", "")
            )

            col1, col2 = st.columns(2)

            with col1:
                save = st.form_submit_button("Save Changes")

            with col2:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state["editing_payment"] = None
            st.rerun()

        if save:
            payload = {
                **payment,
                "amount": amount,
                "payment_date": str(date_paid),
                "notes": notes
            }

            response, result = api_put(
                f"/update_payment/{payment_id}",
                payload
            )

            if response and response.status_code == 200 and "error" not in result:
                st.session_state["payment_success"] = "Payment updated ✅"
                st.session_state["editing_payment"] = None
                st.rerun()
            else:
                st.error(result.get("error", "Update failed"))

    # -------------------------------
    # ADD PAYMENT BUTTON
    # -------------------------------
    if not st.session_state["editing_payment"]:
        col1, col2 = st.columns([1, 5])

        with col1:
            if st.button("➕ Add Payment"):
                st.session_state["show_payment_form"] = True
                st.rerun()

    # -------------------------------
    # SHOW ADD FORM ONLY WHEN CLICKED
    # -------------------------------
    if st.session_state["show_payment_form"]:
        st.markdown("---")
        render_add_payment_form(patient_uuid, patient_name)
# -------------------------------
# INJECTION HISTORY
# -------------------------------
def render_injection_history_section(injections, schedule, patient_uuid, patient_name):

    st.markdown("### Injection History")

    # -------------------------------
    # EMPTY STATE
    # -------------------------------
    if not injections:
        st.info("No injections found.")

    else:
        # -------------------------------
        # TABLE
        # -------------------------------
        table_rows = []

        for inj in injections:
            table_rows.append({
                "Injection ID": inj.get("injection_id"),
                "Medication": inj.get("drug_name"),
                "Dose": f"{inj.get('dose')} {inj.get('unit')}",
                "Date": format_date_display(inj.get("injection_date")),
                "Notes": inj.get("notes", "")
            })

        df = pd.DataFrame(table_rows)

        st.dataframe(df, use_container_width=True, hide_index=True)

        # -------------------------------
        # SELECT + ACTIONS
        # -------------------------------
        st.markdown("### Manage Injection")

        injection_map = {
            f"{inj['drug_name']} • {format_date_display(inj['injection_date'])}": inj
            for inj in injections
        }

        selected_label = st.selectbox(
            "Select Injection",
            ["Select an injection..."] + list(injection_map.keys()),
            key=f"injection_selector_{patient_uuid}"
        )

        if selected_label != "Select an injection...":
            selected_inj = injection_map[selected_label]

            col1, col2 = st.columns(2)

            # EDIT
            with col1:
                if st.button("✏️ Edit Injection", key=f"edit_inj_btn_{selected_inj['injection_id']}"):
                    st.session_state["editing_injection"] = selected_inj
                    st.rerun()

            # DELETE
            with col2:
                if st.button("🗑️ Delete Injection", key=f"delete_inj_btn_{selected_inj['injection_id']}"):
                    st.session_state["delete_injection_id"] = selected_inj["injection_id"]
                    st.rerun()

    # -------------------------------
    # DELETE CONFIRMATION (GLOBAL)
    # -------------------------------
    if st.session_state.get("delete_injection_id"):
        inj_id = st.session_state["delete_injection_id"]

        st.warning("Confirm delete this injection?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Confirm Delete", key="confirm_delete_injection"):
                response, result = api_delete(f"/delete_injection/{inj_id}")

                if response and response.status_code == 200 and "error" not in result:
                    st.success("Injection deleted ✅")
                    st.session_state["delete_injection_id"] = None
                    st.session_state["refresh_injections"] = True  # ✅ ADD THIS
                    st.rerun()
                else:
                    st.error(result.get("error"))

        with col2:
            if st.button("Cancel", key="cancel_delete_injection"):
                st.session_state["delete_injection_id"] = None
                st.rerun()

    # -------------------------------
    # EDIT FORM (GLOBAL)
    # -------------------------------
    if st.session_state.get("editing_injection"):

        inj = st.session_state["editing_injection"]
        inj_id = inj.get("injection_id")

        st.markdown("### ✏️ Edit Injection")

        with st.form(f"edit_injection_form_{inj_id}"):

            col1, col2 = st.columns(2)

            with col1:
                dose = st.number_input(
                    "Dose",
                    value=float(inj.get("dose", 0)),
                    min_value=0.0,
                    step=0.1
                )

                injection_date = st.date_input(
                    "Injection Date",
                    value=pd.to_datetime(inj.get("injection_date")).date()
                )

            with col2:
                notes = st.text_area(
                    "Notes",
                    value=inj.get("notes", "")
                )

            col_save, col_cancel = st.columns(2)

            with col_save:
                save = st.form_submit_button("Save Changes")

            with col_cancel:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state["editing_injection"] = None
            st.rerun()

        if save:
            payload = {
                **inj,
                "dose": dose,
                "injection_date": str(injection_date),
                "notes": notes
            }

            response, result = api_put(
                f"/update_injection/{inj_id}",
                payload
            )

            if response and response.status_code == 200 and "error" not in result:

                st.session_state["injection_success"] = "Injection updated ✅"

                # 🔥 THIS IS THE MISSING PIECE

                st.session_state["refresh_injections"] = True

                st.session_state["editing_injection"] = None

                st.rerun()
            else:
                st.error(result.get("error"))

    # -------------------------------
    # ADD BUTTON + FORM (ALWAYS AVAILABLE)
    # -------------------------------
    if "show_injection_form" not in st.session_state:
        st.session_state["show_injection_form"] = False

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("➕ Log Injection", key=f"log_injection_{patient_uuid}"):
            st.session_state["show_injection_form"] = True
            st.rerun()

    if st.session_state["show_injection_form"]:
        st.markdown("---")
        render_add_injection_form(patient_uuid, patient_name)

# -------------------------------
# ADD INJECTION
# -------------------------------
def render_add_injection_form(patient_uuid, patient_name):
    import datetime

    inventory = api_get("/inventory", default=[])

    if not inventory:
        st.warning("No inventory available.")
        return

    med_options = {
        f"{i['item_name']} • {i['lot_number']}": i for i in inventory
    }

    # ✅ UNIQUE FORM KEY (fixes duplicate form bugs)
    form_key = f"injection_form_{patient_uuid}"

    with st.form(form_key):

        st.markdown("### Log Injection")

        # -------------------------------
        # MED SELECTION
        # -------------------------------
        selected_label = st.selectbox("Medication", list(med_options.keys()))
        selected = med_options[selected_label]

        # -------------------------------
        # BASIC INPUTS
        # -------------------------------
        col1, col2 = st.columns(2)

        with col1:
            dose = st.number_input("Dose (mL)", min_value=0.0, step=0.1, value=0.5)

        with col2:
            # ✅ NEW FIELD
            use_anastrozole = st.checkbox("Include Anastrozole")
            anastrozole_mg = None
            if use_anastrozole:
                anastrozole_mg = st.number_input(
                    "Anastrozole (mg)",
                    min_value=0.0,
                    step=0.25,
                    value=0.25

                )

        submitted = st.form_submit_button("Save Injection")

    # -------------------------------
    # SUBMIT LOGIC
    # -------------------------------
    if submitted:

        if dose <= 0:
            st.error("Dose must be greater than 0 ❌")
            return

        payload = {
            "patient_uuid": patient_uuid,
            "drug_name": selected["item_name"],
            "lot_number": selected["lot_number"],
            "dose": dose,
            "unit": "mL",
            "anastrozole_mg": anastrozole_mg  # ✅ NEW
        }

        response, result = api_post("/add_injection", payload)

        if response and response.status_code == 200 and "error" not in result:

            st.session_state["injection_success"] = "Injection saved ✅"

            st.rerun()

        else:

            st.error(result.get("error", "Failed to save injection"))
# -------------------------------
# LABS
# -------------------------------
def render_labs_section(labs, reminders, patient_uuid):

    st.markdown("### 🧪 Labs")

    if "editing_lab" not in st.session_state:
        st.session_state["editing_lab"] = None

    # -------------------------------
    # LIST VIEW
    # -------------------------------
    if not st.session_state["editing_lab"]:

        if not labs:
            st.info("No lab records found.")

        else:
            for i, lab in enumerate(labs):
                lab_id = lab.get("lab_id")

                col1, col2 = st.columns([6, 1])

                with col1:
                    st.markdown(f"""
                    <div class="content-card">
                        🧪 {lab.get('lab_type')}<br>
                        📅 Due: {lab.get('next_due_date', 'N/A')}<br>
                        📌 Status: {lab.get('results_status', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    if st.button("✏️ Edit", key=f"edit_lab_{lab_id}_{i}"):
                        st.session_state["editing_lab"] = lab
                        st.rerun()

    # -------------------------------
    # EDIT MODE
    # -------------------------------
    else:
        lab = st.session_state["editing_lab"]
        lab_id = lab.get("lab_id")

        st.markdown("### ✏️ Edit Lab")

        with st.form(f"edit_lab_form_{lab_id}"):

            col1, col2 = st.columns(2)

            with col1:
                lab_type = st.text_input("Lab Type", value=lab.get("lab_type", ""))
                ordered_date = st.date_input(
                    "Ordered Date",
                    value=pd.to_datetime(lab.get("ordered_date")).date()
                    if lab.get("ordered_date") else datetime.date.today()
                )

            with col2:
                completed_date = st.date_input(
                    "Completed Date",
                    value=pd.to_datetime(lab.get("completed_date")).date()
                    if lab.get("completed_date") else datetime.date.today()
                )

                next_due_date = st.date_input(
                    "Next Due Date",
                    value=pd.to_datetime(lab.get("next_due_date")).date()
                    if lab.get("next_due_date") else datetime.date.today()
                )

            results_status = st.selectbox(
                "Status",
                ["Ordered", "Completed", "Pending Results"],
                index=["Ordered", "Completed", "Pending Results"].index(
                    lab.get("results_status", "Ordered")
                ) if lab.get("results_status") in ["Ordered", "Completed", "Pending Results"] else 0
            )

            notes = st.text_area("Notes", value=lab.get("notes", ""))

            col_save, col_cancel = st.columns(2)

            with col_save:
                save = st.form_submit_button("Save Changes")

            with col_cancel:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state["editing_lab"] = None
            st.rerun()

        if save:
            payload = {
                "patient_uuid": patient_uuid,
                "lab_type": lab_type,
                "ordered_date": ordered_date.isoformat() if ordered_date else None,
                "completed_date": str(completed_date),
                "results_status": results_status,
                "next_due_date": str(next_due_date),
                "notes": notes
            }

            response, result = api_put(
                f"/update_lab/{lab_id}",
                payload
            )

            if response and response.status_code == 200 and "error" not in result:
                st.success("Lab updated ✅")
                st.session_state["editing_lab"] = None
                st.rerun()
            else:
                st.error(result.get("error", "Update failed"))

    # -------------------------------
    # ADD BUTTON
    # -------------------------------
    if "show_lab_form" not in st.session_state:
        st.session_state["show_lab_form"] = False

    if not st.session_state["editing_lab"]:
        if st.button("➕ Add Lab"):
            st.session_state["show_lab_form"] = True
            st.rerun()

    if st.session_state["show_lab_form"]:
        render_add_lab_form(patient_uuid)

def render_add_lab_form(patient_uuid):

    with st.form(f"lab_form_{patient_uuid}"):

        st.markdown("### Add Lab Record")

        col1, col2 = st.columns(2)

        with col1:
            lab_type = st.text_input("Lab Type")
            ordered_date = st.date_input("Ordered Date")

        with col2:
            completed_date = st.date_input("Completed Date")
            next_due_date = st.date_input("Next Due Date")

        results_status = st.selectbox(
            "Status",
            ["Ordered", "Completed", "Pending Results"]
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Lab")

    # -------------------------------
    # SUBMIT LOGIC
    # -------------------------------
    if submitted:

        if not lab_type.strip():
            st.error("Lab Type is required ❌")
            return

        payload = {
            "patient_uuid": str(patient_uuid),  # ✅ FIX
            "lab_type": lab_type,
            "ordered_date": ordered_date.isoformat() if ordered_date else None,
            "completed_date": completed_date.isoformat() if completed_date else None,
            "results_status": results_status,
            "next_due_date": next_due_date.isoformat() if next_due_date else None,
            "notes": notes
        }

        response, result = api_post("/add_lab", payload)

        if response and response.status_code == 200 and "error" not in result:
            st.success("Lab added ✅")
            st.session_state["show_lab_form"] = False
            st.rerun()
        else:
            st.error(result.get("error", "Failed to add lab"))

# -------------------------------
# TREATMENTS
# -------------------------------
def render_treatments_section(treatments, patient_uuid):
    render_data_section("Treatments", treatments)
    render_add_treatment_form(patient_uuid)

def render_add_treatment_form(patient_uuid):

    with st.form(f"treatment_form_{patient_uuid}_{datetime.datetime.now().timestamp()}"):
        name = st.text_input("Treatment Name")
        submitted = st.form_submit_button("Save")

    if submitted:
        if not name.strip():
            st.error("Treatment name is required")
            return

        response, result = api_post("/add_treatment", {
            "patient_uuid": patient_uuid,
            "treatment_name": name.strip()
        })

        if response and response.status_code == 200 and "error" not in result:
            st.success("Treatment added ✅")
            st.rerun()
        else:
            st.error(result.get("error", "Failed to add treatment"))

# -------------------------------
# PAYMENTS FORM
# -------------------------------
def render_add_payment_form(patient_uuid, patient_name):

    st.markdown("### Add Payment")

    with st.form(f"payment_form_{patient_uuid}"):

        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input("Amount", min_value=0.0, step=1.0)
            payment_date = st.date_input("Payment Date")

            autopay = st.selectbox(
                "Autopay",
                ["No", "Yes", "3 Months"]
            )

        with col2:
            payment_type = st.selectbox(
                "Payment Type",
                ["Standard", "Testosterone Plan"]
            )

            lab_package = None

            if payment_type == "Testosterone Plan":
                lab_package = st.selectbox(
                    "Lab Package",
                    ["No Labs ($165)", "Labs $110", "Labs $190"]
                )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Payment")

    if submitted:

        # -------------------------------
        # AUTO PRICING LOGIC
        # -------------------------------
        if payment_type == "Testosterone Plan":
            if lab_package == "No Labs ($165)":
                amount = 165
            elif lab_package == "Labs $110":
                amount = 110
            elif lab_package == "Labs $190":
                amount = 190

        payload = {
            "patient_uuid": str(patient_uuid),
            "amount": amount,
            "payment_date": str(payment_date),
            "autopay": autopay,
            "payment_type": payment_type,
            "lab_package": lab_package,
            "notes": notes
        }

        response, result = api_post("/add_payment", payload)

        if response and response.status_code == 200 and "error" not in result:
            st.session_state["payment_success"] = f"Payment added for {patient_name} ✅"
            st.session_state["show_payment_form"] = False
            st.rerun()
        else:
            st.error(result.get("error", "Failed to add payment"))

# -------------------------------
# SCANS
# -------------------------------
def render_scans_section(scans, patient_uuid):

    import datetime

    st.markdown("### Body Scans")

    # -------------------------------
    # DISPLAY EXISTING
    # -------------------------------
    if not scans:
        st.info("No scans found.")
    else:
        df = pd.DataFrame(scans)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # -------------------------------
    # STATE
    # -------------------------------
    if "show_scan_form" not in st.session_state:
        st.session_state["show_scan_form"] = False

    # -------------------------------
    # ADD BUTTON
    # -------------------------------
    if st.button("➕ Add Body Scan"):
        st.session_state["show_scan_form"] = True
        st.rerun()

    # -------------------------------
    # FORM
    # -------------------------------
    if st.session_state["show_scan_form"]:

        st.markdown("---")

        with st.form(f"scan_form_{patient_uuid}"):

            st.markdown("### Add Body Scan")

            scan_completed = st.radio(
                "Scan Completed?",
                ["No", "Yes"]
            )

            scan_date = None

            if scan_completed == "Yes":
                scan_date = st.date_input(
                    "Date Completed",
                    value=datetime.date.today()
                )

            notes = st.text_area("Notes")

            col1, col2 = st.columns(2)

            with col1:
                submitted = st.form_submit_button("Save")

            with col2:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state["show_scan_form"] = False
            st.rerun()

        if submitted:

            payload = {
                "patient_uuid": patient_uuid,
                "scan_completed": True if scan_completed == "Yes" else False,
                "scan_date": str(scan_date) if scan_date else None,
                "notes": notes
            }

            response, result = api_post("/add_body_scan", payload)

            if response and response.status_code == 200 and "error" not in result:
                st.success("Scan added ✅")
                st.session_state["show_scan_form"] = False
                st.rerun()
            else:
                st.error(result.get("error", "Failed to add scan"))
# -------------------------------
# LAB REMINDERS
# -------------------------------
def render_lab_reminders_section(reminders):
    render_data_section("Lab Reminders", reminders)

# -------------------------------
# SCHEDULE
# -------------------------------
def render_schedule_section(schedule):
    render_data_section("Injection Schedule", schedule)
