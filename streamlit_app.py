import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

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

# --- Title ---
st.set_page_config(page_title="DockMate Demo", layout="centered")
st.title("DockMate: Marina Service Coordination")

# --- Form ---
st.header("Create a New Service Ticket")
with st.form("service_form"):
    boat_name = st.text_input("Boat Name")
    cradle_id = st.text_input("Cradle ID")
    service_date = st.date_input("Requested Service Date", min_value=datetime.today())
    selected_services = st.multiselect("Select Required Services", list(vendors.keys()))
    submitted = st.form_submit_button("Submit Service Request")

    if submitted:
        if not boat_name or not cradle_id or not selected_services:
            st.error("Please fill out all fields and select at least one service.")
        else:
            unavailable = [v for v in selected_services if not is_available(v, service_date)]
            if unavailable:
                st.warning(f"The following vendors are unavailable on {service_date}: {', '.join(unavailable)}")
            else:
                ticket = {
                    "Ticket ID": str(uuid.uuid4())[:8],
                    "Boat Name": boat_name,
                    "Cradle ID": cradle_id,
                    "Service Date": service_date.strftime("%Y-%m-%d"),
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
