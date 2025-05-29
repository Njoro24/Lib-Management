# Library Management System
A command-line interface (CLI) application for managing a small library's books and members. This system allows librarians to track book loans, returns, and member information using a SQLite database with SQLAlchemy ORM.

## Features
Member Management: Add, view, search, and delete library members
Book Management: Add, view, search, and delete books from the catalog
Book Operations: Loan books to members and process returns
Data Validation: Input validation and error handling throughout the application
Database Integration: SQLAlchemy ORM with SQLite database

## Database Schema
The application uses two main entities with a one-to-many relationship:

Members: Library members who can borrow books
Books: Library catalog with borrowing status tracking
One member can borrow multiple books (one-to-many relationship).

## Installation
Clone this repository
Install dependencies using Pipenv:
bashpipenv install
Activate the virtual environment:
bashpipenv shell


## Usage
Run the application:
bashpython main.py

## Main Menu Options
### Manage Members
Add new member
View all members
Find member by name or email
View member's borrowed books
Delete member


### Manage Books
Add new book
View all books
Find book by title, author, or ISBN
View available books only
Delete book


### Book Operations
Loan book to member
Return book



## Data Models
### Member
ID (Primary Key)
Name (Required)
Email (Required, Unique)
Phone (Optional)
Membership Date (Auto-set)

### Book
ID (Primary Key)
Title (Required)
Author (Required)
ISBN (Required, Unique)
Availability Status
Member ID (Foreign Key, nullable)

### Technical Requirements
Python 3.8+
SQLAlchemy for ORM operations
SQLite database (automatically created)

## Project Structure
library_management/
├── main.py              # Application entry point
├── models/              # Database models
├── cli/                 # CLI interface modules
└── utils/               # Utility functions