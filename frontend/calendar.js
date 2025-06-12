# Add at the top:
import json
from datetime import datetime

# Inside your if selected_services: block
available_dates_str = [d.strftime("%Y-%m-%d") for d in available_dates]

calendar_js = f"""
<div id="calendar-container"></div>
<script>
    const container = document.getElementById("calendar-container");
    const today = new Date();
    const available = {json.dumps(available_dates_str)};
    
    for (let i = 0; i < 30; i++) {{
        const date = new Date();
        date.setDate(today.getDate() + i);
        const dateStr = date.toISOString().slice(0, 10);
        const isAvailable = available.includes(dateStr);
        const div = document.createElement("div");
        div.textContent = dateStr;
        div.className = "calendar-day";
        div.style.backgroundColor = isAvailable ? "lightgreen" : "#f99";
        div.style.padding = "6px";
        div.style.margin = "4px";
        div.style.display = "inline-block";
        div.style.borderRadius = "6px";
        div.style.fontWeight = "bold";
        container.appendChild(div);
    }}
</script>
"""

components.html(calendar_js, height=350)
