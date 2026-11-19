
from app.database import engine, Base
from app import models

try:
    Base.metadata.create_all(bind=engine)
    print("All database tables created successfully!")

except Exception as error:
    print("Table creation failed:")
    print(error)
