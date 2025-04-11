# seed_data.py

from app.database import SessionLocal
from app import models

def seed_settings():
    db = SessionLocal()
    existing = db.query(models.Settings).first()
    if existing:
        print("Settings already exist. Skipping seeding.")
    else:
        new_setting = models.Settings(monthly_budget=10000.0)
        db.add(new_setting)
        db.commit()
        print("Seeded default settings.")
    db.close()

if __name__ == "__main__":
    seed_settings()
