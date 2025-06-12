import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta

# --- Initialization ---
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# --- Vendor Setup ---
vendors = {
    "Marina Launch Team": {"service": "Dock Fee / Launch", "available_days": [0, 1, 2, 3, 4]},
    "Trucking Co": {"service": "Cradle Transport", "available_days": [1, 2, 3, 4]},
    "Crane Co": {"service": "Boat Lift", "available_days": [0, 2, 4]},
}

# --- Helper Functions ---
def is_available(vendor, date):
    return date.weekday() in vendors[vendor]["available_days"]

def get_overlapping_dates(selected_services, start_date, days_range=14):
    available_dates = []
    for i in range(days_range):
        check_date = start_date + timedelta(days=i)
        if all(is_available(v, check_date) for v in selected_services):
            available_dates.append(check_date)
    return available_dates

# --- Title ---
st.set_page_config(page_title="DockMate Demo", layout="centered")
st.title("DockMate: Marina Service Coordination")

# --- Form ---
st.header("Create a New Service Ticket")
with st.form("service_form"):
    boat_name = st.text_input("Boat Name")
    cradle_id = st.text_input("Cradle ID")

    selected_services = []
    st.subheader("Select Required Services")
    for vendor in vendors.keys():
        if st.checkbox(vendor):
            selected_services.append(vendor)

    available_dates = []
    selected_service_date = None

    if selected_services:
        today = datetime.today()
        available_dates = get_overlapping_dates(selected_services, today)

        if available_dates:
            selected_service_date = st.selectbox("Select Available Date", available_dates)
        else:
            st.warning("No overlapping dates available within the next 14 days for the selected services.")

    submitted = st.form_submit_button("Submit Service Request")

    if submitted:
        if not boat_name or not cradle_id or not selected_services or not selected_service_date:
            st.error("Please complete all fields and ensure an available date is selected.")
        else:
            ticket = {
                "Ticket ID": str(uuid.uuid4())[:8],
                "Boat Name": boat_name,
                "Cradle ID": cradle_id,
                "Service Date": selected_service_date.strftime("%Y-%m-%d"),
                "Vendors": selected_services,
                "Total Cost": f"${len(selected_services) * 200:.2f}",
                "Status": "Scheduled"
            }
            st.session_state.tickets.append(ticket)
            st.success("Service ticket created successfully!")

# --- Display Tickets ---
if st.session_state.tickets:
    st.header("Scheduled Service Tickets")
    df = pd.DataFrame(st.session_state.tickets)
    st.dataframe(df, use_container_width=True)

st.caption("This is a demo application. Payment integration and vendor portals would be added in full version.")
