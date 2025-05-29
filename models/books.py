from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date, timedelta
from .database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(150), nullable=False)
    isbn = Column(String(17), unique=True, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    borrowed_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    
    # Relationship with member
    borrower = relationship("Member", back_populates="borrowed_books")
    
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.member_id = None
        self.borrowed_date = None
        self.due_date = None
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value.strip()) < 1:
            raise ValueError("Title must be at least 1 character long")
        self._title = value.strip()
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        if not value or not value.strip():
            raise ValueError("Author cannot be empty")
        if len(value.strip()) < 2:
            raise ValueError("Author name must be at least 2 characters long")
        self._author = value.strip()
    
    @property
    def isbn(self):
        return self._isbn
    
    @isbn.setter
    def isbn(self, value):
        if not value or not value.strip():
            raise ValueError("ISBN cannot be empty")
        # Remove hyphens and spaces for validation
        cleaned_isbn = value.replace("-", "").replace(" ", "")
        if not cleaned_isbn.isdigit():
            raise ValueError("ISBN should contain only digits and hyphens")
        if len(cleaned_isbn) not in [10, 13]:
            raise ValueError("ISBN should be 10 or 13 digits long")
        self._isbn = cleaned_isbn
    
    def borrow_to_member(self, member_id, loan_days=14):
        """Loan this book to a member."""
        if not self.is_available:
            raise ValueError("Book is not available for borrowing")
        
        self.member_id = member_id
        self.is_available = False
        self.borrowed_date = date.today()
        self.due_date = date.today() + timedelta(days=loan_days)
    
    def return_book(self):
        """Return this book and make it available."""
        self.member_id = None
        self.is_available = True
        self.borrowed_date = None
        self.due_date = None
    
    def is_overdue(self):
        """Check if the book is overdue."""
        if self.due_date and not self.is_available:
            return date.today() > self.due_date
        return False
    
    def days_until_due(self):
        """Calculate days until due date."""
        if self.due_date and not self.is_available:
            delta = self.due_date - date.today()
            return delta.days
        return None
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', available={self.is_available})>"
    
    def __str__(self):
        status = "Available" if self.is_available else f"Borrowed (Due: {self.due_date})"
        return f"Book #{self.id}: '{self.title}' by {self.author} - ISBN: {self.isbn} - Status: {status}"