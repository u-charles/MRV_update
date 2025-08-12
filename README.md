# EduMRV - Modular MRV app

Install:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Run:
streamlit run app.py

Notes:
- Register a user on Register page, then Login.
- Use Enter Emissions to input multiple categories at once.
- View Records shows breakdown and totals by Scope 1/2/3.
- Edit `data/emissions_factors.csv` or `calculator.py` to change factors.
- For production use, switch SQLite to Postgres in db/database.py and set connection string via Streamlit secrets.
