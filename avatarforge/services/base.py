"""Base service class"""
from sqlalchemy.orm import Session


class BaseService:
    """
    Base service class that other services can inherit from
    Provides common patterns for business logic
    """

    def __init__(self, db: Session):
        self.db = db
