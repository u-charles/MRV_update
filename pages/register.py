# pages/register.py
import streamlit as st
from db.database import get_db
from db import crud

def show_register():
    st.header("Register")
    email = st.text_input("Email", key="reg_email")
    name = st.text_input("Full name", key="reg_name")
    password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register"):
        if not email or not password:
            st.error("Please provide email and password.")
            return
        db = next(get_db())
        existing = crud.get_user_by_email(db, email)
        if existing:
            st.warning("Account with that email already exists. Please log in.")
        else:
            crud.create_user(db, email, password, name)
            st.success("Registration successful. You can now log in.")
