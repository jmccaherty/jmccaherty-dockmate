import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# --- Initialization ---
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# --- Vendor Setup with Pricing ---
vendors = {
    "Marina Launch Fee ($100)": {"service": "Dock Fee / Launch", "price": 100, "available_days": [0, 1, 2, 3, 4]},
    "Trucking Co ($300)": {"service": "Cradle Transport", "price": 300, "available_days": [1, 2, 3, 4]},
    "Crane Co ($250)": {"service": "Boat Lift", "price": 250, "available_days": [0, 2, 4]},
    "Marina Mast Fee ($25)": {"service": "Mast Fee", "price": 25, "available_days": [0, 1, 2, 3, 4]},
    "Crane Mast Lift ($50)": {"service": "Mast Lift", "price": 50, "available_days": [0, 2, 4]},
}

# --- Helper Functions ---
def is_available(vendor, date):
    return date.weekday() in vendors[vendor]["available_days"]

def get_overlapping_dates(selected_services, start_date, days_range=30):
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
    boat_length = st.text_input("Boat Length (ft)")
    storage_type = st.radio("Stored On:", ["Cradle", "Trailer"])

    selected_services = []
    st.subheader("Select Required Services (with pricing)")
    for vendor in vendors.keys():
        if st.checkbox(vendor):
            selected_services.append(vendor)

    available_dates = []
    selected_service_date = None
    today = datetime.today()

    if selected_services:
        available_dates = get_overlapping_dates(selected_services, today)

        # --- Calendar UI ---
        st.subheader("Available Dates Calendar")
        calendar_html = "<style>.calendar-day{display:inline-block;width:120px;text-align:center;padding:8px;margin:4px;border-radius:8px;font-weight:bold;font-size:14px;}</style><div>"
        for i in range(30):
            day = today + timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            if day in available_dates:
                calendar_html += f'<div class="calendar-day" style="background-color:lightgreen;">{day_str}</div>'
            else:
                calendar_html += f'<div class="calendar-day" style="background-color:#f99;">{day_str}</div>'
        calendar_html += "</div><br>"
        components.html(calendar_html, height=350)

        if available_dates:
            selected_service_date = st.selectbox("Select Available Date", available_dates)
        else:
            st.warning("No overlapping dates available within the next 30 days for the selected services.")

    submitted = st.form_submit_button("Submit Service Request")

    if submitted:
        if not boat_name or not boat_length or not storage_type or not selected_services or not selected_service_date:
            st.error("Please complete all fields and ensure an available date is selected.")
        else:
            total_cost = sum(vendors[v]["price"] for v in selected_services)
            ticket = {
                "Ticket ID": str(uuid.uuid4())[:8],
                "Boat Name": boat_name,
                "Length": boat_length,
                "Storage Type": storage_type,
                "Service Date": selected_service_date.strftime("%Y-%m-%d"),
                "Vendors": selected_services,
                "Total Cost": f"${total_cost:.2f}",
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



