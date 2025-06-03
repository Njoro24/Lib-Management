from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date
from .database import Base

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column("name", String(100), nullable=False)
    _email = Column("email", String(150), unique=True, nullable=False)
    _phone = Column("phone", String(20), nullable=True)
    membership_date = Column(Date, nullable=False, default=date.today)
    
    borrowed_books = relationship("Book", back_populates="borrower")

    def __init__(self, name, email, phone=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.membership_date = date.today()

    # Hybrid property for name
    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        self._name = value.strip()

    # Hybrid property for email
    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or not value.strip():
            raise ValueError("Email cannot be empty")
        if "@" not in value or "." not in value:
            raise ValueError("Please enter a valid email address")
        self._email = value.strip().lower()

    # Hybrid property for phone
    @hybrid_property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if value is not None:
            cleaned_phone = value.replace(" ", "").replace("-", "")
            if cleaned_phone and not cleaned_phone.isdigit():
                raise ValueError("Phone number should contain only digits")
            self._phone = cleaned_phone if cleaned_phone else None
        else:
            self._phone = None

    def can_borrow_books(self):
        return len(self.borrowed_books) < 5

    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.name}', email='{self.email}')>"

    def __str__(self):
        phone_str = f", Phone: {self.phone}" if self.phone else ""
        return f"Member #{self.id}: {self.name} ({self.email}){phone_str} - Joined: {self.membership_date}"