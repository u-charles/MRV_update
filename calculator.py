# calculator.py
from typing import Dict, Tuple
from db import crud

# Scope mapping independent from factor table
SCOPE_MAPPING = {
    "electricity_kwh": "Scope 2",
    "diesel_litre": "Scope 1",
    "petrol_litre": "Scope 1",
    "lpg_litre": "Scope 1",
    "natural_gas_m3": "Scope 1",
    "water_litres": "Scope 3",
    "waste_kg": "Scope 3",
    "petrol_car_km": "Scope 1",
    "diesel_car_km": "Scope 1",
    "ev_car_km": "Scope 2",
    "bus_km": "Scope 3",
    "motorcycle_km": "Scope 3"
}

def calculate_bulk_from_db(db_session, inputs: Dict[str, float]) -> Tuple[Dict[str, float], float]:
    """
    Calculate using latest factors stored in DB. Returns (details, total).
    """
    factors = crud.get_latest_factors(db_session)
    details = {}
    total = 0.0
    for k, val in inputs.items():
        if val is None or float(val) <= 0:
            continue
        f = factors.get(k)
        if not f:
            # skip unknown categories
            continue
        emission = float(val) * float(f["factor"])
        details[k] = round(emission, 6)
        total += emission
    return details, round(total, 6)

def get_scope_for_key(key: str) -> str:
    return SCOPE_MAPPING.get(key, "Scope 3")
