# pages/emissions_input.py
import streamlit as st
import pandas as pd
from db.database import get_db
from db import crud
from calculator import calculate_bulk_from_db, get_scope_for_key

def show_input():
    st.header("Enter emissions quantities (multiple categories)")

    if "user_id" not in st.session_state:
        st.info("Please log in first.")
        return

    db = next(get_db())
    factors = crud.get_latest_factors(db)
    if not factors:
        st.error("No emission factors found. Ask admin to seed factors.")
        db.close()
        return

    keys = list(factors.keys())

    cols = st.columns(2)
    inputs = {}
    for i, k in enumerate(keys):
        col = cols[i % 2]
        label = k.replace("_", " ").title()
        inputs[k] = col.number_input(f"{label} ({factors[k]['unit']})", min_value=0.0, format="%.3f", key=f"inp_{k}")

    if st.button("Calculate & Save All"):
        details, total = calculate_bulk_from_db(db, inputs)
        if not details:
            st.info("No values entered.")
            db.close()
            return

        saved = 0
        for k, v in inputs.items():
            if v and float(v) > 0:
                emission = details.get(k)
                scope = get_scope_for_key(k)
                crud.create_emission_record(db, st.session_state["user_id"], k, float(v), float(emission), scope=scope)
                saved += 1

        st.success(f"Saved {saved} records. Total emissions: {total} kg CO₂e")
        st.table(pd.DataFrame([{"activity": k, "emission_kg": e} for k, e in details.items()]))
    db.close()
