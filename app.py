import streamlit as st
from auth.login import login_user

st.set_page_config(page_title="DockMate Pro+", layout="wide")
login_user()
