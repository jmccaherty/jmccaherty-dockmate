import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import json

# --- Initialization ---
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# --- Vendor Setup with Pricing ---
vendors = {
    "Marina Launch Fee": {"price": 100, "available_days": [0, 1, 2, 3, 4]},
    "Trucking Co": {"price": 300, "available_days": [1, 2, 3, 4]},
    "Crane Co": {"price": 250, "available_days": [0, 2, 4]},
    "Marina Mast Fee": {"price": 25, "available_days": [0, 1, 2, 3, 4]},
    "Crane Mast Lift": {"price": 50, "available_days": [0, 2, 4]},
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
    for vendor, info in vendors.items():
        label = f"{vendor} (${info['price']})"
        if st.checkbox(label):
            selected_services.append(vendor)

    available_dates = []
    selected_service_date = None
    today = datetime.today()

    if selected_services:
        available_dates = get_overlapping_dates(selected_services, today)
        available_dates_str = [d.strftime("%Y-%m-%d") for d in available_dates]

        st.subheader("Available Dates Calendar")
        calendar_html = f"""
        <style>
        .calendar-day {{
            display:inline-block;
            width:120px;
            text-align:center;
            padding:8px;
            margin:4px;
            border-radius:8px;
            font-weight:bold;
            font-size:14px;
        }}
        </style>
        <div id='calendar-container'>
        """

        for i in range(30):
            day = today + timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            if day_str in available_dates_str:
