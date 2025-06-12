import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# Store tickets
if "tickets" not in st.session_state:
    st.session_state.tickets = []

vendors = {
    "Marina Launch Team": {"service": "Dock Fee / Launch", "available_days": [0, 1, 2, 3, 4]},
    "Trucking Co": {"service": "Cradle Transport", "available_days": [1, 2, 3, 4]},
    "Crane Co": {"service": "Boat Lift", "available_days": [0, 2, 4]},
}

def is_available(vendor, date):
    return date.weekday() in vendors[vendor]["available_days"]

st.title("DockMate: Marine Service Made Easy")
st.header("Create a Service Ticket")
boat_name = st.text_input("Boat Name")
cradle_id = st.text_input("Cradle ID")
service_date = st.date_input("Requested Date", min_value=datetime.today())
selected_services = st.multiselect("Select Services Needed", list(vendors.keys()))

if st.button("Create Ticket"):
    unavailable = [v for v in selected_services if not is_available(v, service_date)]
    if unavailable:
        st.error(f"Unavailable vendors on {service_date}: {', '.join(unavailable)}")
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
        st.success("Ticket created!")

if st.session_state.tickets:
    st.header("Scheduled Tickets")
    df = pd.DataFrame(st.session_state.tickets)
    st.dataframe(df)

st.caption("Demo: Not connected to real vendors or payment processors.")
