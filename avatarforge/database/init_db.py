"""
Database initialization script

Run this to create all database tables
"""
from sqlalchemy import create_engine
from avatarforge.database.base import Base
from avatarforge.core.config import settings
from avatarforge.models.uploaded_file import UploadedFile
from avatarforge.models.generation import Generation


def init_db():
    """Initialize database with all tables"""
    engine = create_engine(settings.DATABASE_URL, echo=True)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("✓ Database tables created successfully!")
    print(f"  - uploaded_files")
    print(f"  - generations")


if __name__ == "__main__":
    init_db()
