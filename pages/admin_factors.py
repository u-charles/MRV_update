# pages/admin_factors.py
import streamlit as st
from db.database import get_db
from db import crud

def show_admin_factors():
    st.header("Manage Emission Factors (Admin)")

    db = next(get_db())
    factors = crud.get_latest_factors(db)
    st.write("Current active factors:")
    st.json(factors)

    st.write("---")
    st.subheader("Add / Update factor (creates new version)")
    category = st.text_input("Category (use underscore naming, e.g. electricity_kwh)")
    factor = st.number_input("Factor (kg CO2 per unit)", min_value=0.0, format="%.6f")
    unit = st.text_input("Unit (e.g. kWh, litre, km)")
    note = st.text_input("Note (optional)")
    if st.button("Save new factor version"):
        if not category or factor <= 0 or not unit:
            st.error("Provide category, factor (>0) and unit.")
        else:
            crud.insert_emission_factor(db, category.strip(), float(factor), unit.strip(), note.strip() or None)
            st.success(f"Saved factor for {category}. New version created.")
    db.close()
