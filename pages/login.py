# pages/login.py
import streamlit as st
from db.database import get_db
from db import crud

def show_login():
    st.header("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        db = next(get_db())
        user = crud.verify_user(db, email, password)
        if user:
            st.success(f"Welcome {user.name or user.email}!")
            st.session_state["user_email"] = user.email
            st.session_state["user_id"] = user.id
            # ensure active tab set
            st.session_state["active_tab"] = "Enter Emissions"
            st.experimental_rerun()
        else:
            # differentiate not-found vs wrong password
            if not crud.get_user_by_email(db, email):
                st.info("No account found. Please register.")
            else:
                st.error("Incorrect password. Try again.")