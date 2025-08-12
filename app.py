# app.py
import streamlit as st
from db.database import init_db
from pages import login, register, emissions_input, view_results, admin_factors

# initialize DB and seed defaults if empty
init_db()

st.set_page_config(page_title="EduMRV — MRV Platform", layout="wide")
st.title("EduMRV — Measurement, Reporting & Verification")

# Setup session defaults
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Login"

# Show login/register when not logged in
if not st.session_state["user_id"]:
    # small nav for auth
    auth_choice = st.sidebar.selectbox("Auth", ["Login", "Register"])
    if auth_choice == "Login":
        login.show_login()
    else:
        register.show_register()
else:
    # show application tabs
    st.sidebar.success(f"Logged in as {st.session_state['user_email']}")
    if st.sidebar.button("Logout"):
        st.session_state["user_id"] = None
        st.session_state["user_email"] = None
        st.experimental_rerun()

    tabs = st.tabs(["Enter Emissions", "View Records", "Admin: Factors"])
    with tabs[0]:
        emissions_input.show_input()
    with tabs[1]:
        view_results.show_results()
    with tabs[2]:
        admin_factors.show_admin_factors()
