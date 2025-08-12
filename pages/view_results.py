# pages/view_results.py
import streamlit as st
import pandas as pd
import altair as alt
from db.database import get_db
from db import crud

def show_results():
    st.header("My Emission Records & Scope Summary")
    if "user_id" not in st.session_state:
        st.info("Please log in.")
        return
    db = next(get_db())
    records = crud.get_user_emissions(db, st.session_state["user_id"])
    if not records:
        st.info("No records yet.")
        db.close()
        return

    df = pd.DataFrame([{
        "Category": r.category,
        "Quantity": r.quantity,
        "Emission (kg CO₂e)": r.emission,
        "Scope": r.scope,
        "Timestamp": r.timestamp
    } for r in records])

    st.dataframe(df)

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Category:N", sort=None),
        y="Emission (kg CO₂e):Q",
        color="Scope:N",
        tooltip=["Category", "Emission (kg CO₂e)", "Quantity", "Scope", "Timestamp"]
    ).properties(title="Emissions by Category")

    st.altair_chart(chart, use_container_width=True)

    totals = df.groupby("Scope")["Emission (kg CO₂e)"].sum().reset_index()
    st.write("### Totals by Scope")
    st.dataframe(totals)
    db.close()
