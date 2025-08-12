# db/crud.py
from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from passlib.hash import bcrypt

# ---------- User functions ----------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password_plain: str, name: str = None):
    password_hash = bcrypt.hash(password_plain)
    user = models.User(email=email, name=name, password_hash=password_hash, created_at=datetime.utcnow())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_user(db: Session, email: str, password_plain: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if bcrypt.verify(password_plain, user.password_hash):
        return user
    return None

# ---------- Emission factor functions ----------
def count_emission_factors(db: Session):
    return db.query(models.EmissionFactor).count()

def get_latest_factors(db: Session):
    """
    Return dict {category: {factor, unit, version, id, effective_date}} of latest active versions.
    """
    rows = db.query(models.EmissionFactor).filter(models.EmissionFactor.active == True).all()
    result = {}
    for r in rows:
        existing = result.get(r.category)
        if not existing or r.version > existing["version"]:
            result[r.category] = {
                "id": r.id,
                "factor": r.factor,
                "unit": r.unit,
                "version": r.version,
                "effective_date": r.effective_date,
                "note": r.note
            }
    return result

def insert_emission_factor(db: Session, category: str, factor: float, unit: str, note: str = None):
    # find max version
    maxv = db.query(models.EmissionFactor).filter(models.EmissionFactor.category == category).order_by(models.EmissionFactor.version.desc()).first()
    new_version = 1 if not maxv else maxv.version + 1
    # deactivate previous active versions for this category
    db.query(models.EmissionFactor).filter(models.EmissionFactor.category == category, models.EmissionFactor.active == True).update({"active": False})
    ef = models.EmissionFactor(category=category, factor=factor, unit=unit, version=new_version, effective_date=datetime.utcnow(), note=note, active=True)
    db.add(ef)
    db.commit()
    db.refresh(ef)
    return ef

def insert_emission_factor_if_empty(db: Session):
    """
    Insert the default initial set (only run if table empty).
    """
    defaults = [
        ("electricity_kwh", 0.47, "kWh", "Default"),
        ("diesel_litre", 2.68, "litre", "Default"),
        ("petrol_litre", 2.31, "litre", "Default"),
        ("lpg_litre", 1.51, "litre", "Default"),
        ("natural_gas_m3", 1.9, "m3", "Default"),
        ("water_litres", 0.0003, "litre", "Default"),
        ("waste_kg", 0.72, "kg", "Default"),
        ("petrol_car_km", 0.192, "km", "Default"),
        ("diesel_car_km", 0.171, "km", "Default"),
        ("ev_car_km", 0.075, "km", "Default"),
        ("bus_km", 0.089, "km", "Default"),
        ("motorcycle_km", 0.103, "km", "Default")
    ]
    for cat, factor, unit, note in defaults:
        insert_emission_factor(db, cat, factor, unit, note)

# ---------- Emission records ----------
def create_emission_record(db: Session, user_id: int, category: str, quantity: float, emission: float, scope: str = None, **kwargs):
    rec = models.EmissionRecord(
        user_id=user_id,
        category=category,
        quantity=quantity,
        emission=emission,
        scope=scope,
        reporting_period_start=kwargs.get("reporting_period_start"),
        reporting_period_end=kwargs.get("reporting_period_end"),
        location=kwargs.get("location"),
        data_source=kwargs.get("data_source"),
        is_verified=kwargs.get("is_verified", False),
        timestamp=datetime.utcnow()
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def get_user_emissions(db: Session, user_id: int):
    return db.query(models.EmissionRecord).filter(models.EmissionRecord.user_id == user_id).order_by(models.EmissionRecord.timestamp.desc()).all()
