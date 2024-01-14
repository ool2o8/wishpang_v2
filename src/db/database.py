from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, client_encoding="utf8", pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()