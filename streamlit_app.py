import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta
import json
import streamlit.components.v1 as components 

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
    total_cost = 0
    st.subheader("Select Required Services (with pricing)")
    for vendor, info in vendors.items():
        label = f"{vendor} (${info['price']})"
        if st.checkbox(label, key=vendor):
            selected_services.append(vendor)
            total_cost += info['price']

    st.markdown(f"**Estimated Total Cost: ${total_cost:.2f}**")

    submitted = st.form_submit_button("Submit Service Request")

# Render calendar and date selection outside the form to make it always visible
available_dates = []
today = datetime.today()

if selected_services:
    available_dates = get_overlapping_dates(selected_services, today)
    st.subheader("Available Dates Calendar")
    selected = st.text_input("Selected Date (click a green date below)", key="selected_date")

    # Enhanced calendar rendering
    available_dates_str = [d.strftime("%Y-%m-%d") for d in available_dates]
    selected_date_str = selected or ""

    calendar_html = f"""
    <script>
    const available = {json.dumps(available_dates_str)};
    const selected = "{selected_date_str}";
    const today = new Date();
    const container = document.createElement('div');
    container.style.fontFamily = 'sans-serif';

    for (let i = 0; i < 30; i++) {{
        const day = new Date();
        day.setDate(today.getDate() + i);
        const dayStr = day.toISOString().slice(0, 10);

        const div = document.createElement('div');
        div.textContent = dayStr;
        div.style.padding = '8px';
        div.style.margin = '4px';
        div.style.display = 'inline-block';
        div.style.borderRadius = '8px';
        div.style.fontWeight = 'bold';
        div.style.cursor = available.includes(dayStr) ? 'pointer' : 'not-allowed';
        div.style.backgroundColor = dayStr === selected ? '#3cba54' : (available.includes(dayStr) ? 'lightgreen' : '#f99');
        div.style.color = available.includes(dayStr) ? '#000' : '#555';

        if (available.includes(dayStr)) {{
            div.onclick = () => {{
                const streamlitInput = window.parent.document.querySelectorAll('[data-testid="stTextInput"] input')[0];
                streamlitInput.value = dayStr;
                streamlitInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }};
        }}

        container.appendChild(div);
    }}

    document.body.appendChild(container);
    </script>
    """
    st.components.v1.html(calendar_html, height=400)

# Handle submission outside form block
selected_service_date = None
if st.session_state.get("selected_date"):
    try:
        selected_service_date = datetime.strptime(st.session_state.get("selected_date"), "%Y-%m-%d")
    except Exception:
        selected_service_date = None

if submitted:
    if not boat_name or not boat_length or not storage_type or not selected_services or not selected_service_date:
        st.error("Please complete all fields and ensure an available date is selected.")
    else:
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

