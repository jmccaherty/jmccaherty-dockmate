import streamlit.components.v1 as components
import json
from datetime import datetime, timedelta

def render_interactive_calendar(available_dates):
    available_dates_str = [d.strftime("%Y-%m-%d") for d in available_dates]

    calendar_html = f"""
    <script>
    const available = {json.dumps(available_dates_str)};
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
        div.style.cursor = 'pointer';
        div.style.backgroundColor = available.includes(dayStr) ? 'lightgreen' : '#f99';

        if (available.includes(dayStr)) {{
            div.onclick = () => {{
                const streamlitInput = window.parent.document.querySelectorAll('[data-testid=\"stTextInput\"] input')[0];
                streamlitInput.value = dayStr;
                streamlitInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }};
        }}

        container.appendChild(div);
    }}

    document.body.appendChild(container);
    </script>
    """

    components.html(calendar_html, height=400)

