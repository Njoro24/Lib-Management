from models import Book, Member, get_db_session
from utils import (
    validate_name, validate_isbn,
    get_valid_input, get_yes_no_input, get_integer_input
)
from sqlalchemy.exc import IntegrityError

class BookCLI:
    
    def __init__(self):
        self.session = get_db_session()
    
    def display_book_menu(self):
        """Display book management menu."""
        while True:
            print("\n" + "="*50)
            print("BOOK MANAGEMENT")
            print("="*50)
            print("1. Add new book")
            print("2. View all books")
            print("3. View available books only")
            print("4. Find book by title")
            print("5. Find book by author")
            print("6. Find book by ISBN")
            print("7. Loan book to member")
            print("8. Return book")
            print("9. Delete book")
            print("10. Back to main menu")
            
            choice = get_integer_input("Enter your choice (1-10): ", 1, 10)
            
            if choice is None:
                continue
            elif choice == 1:
                self.add_book()
            elif choice == 2:
                self.view_all_books()
            elif choice == 3:
                self.view_available_books()
            elif choice == 4:
                self.find_book_by_title()
            elif choice == 5:
                self.find_book_by_author()
            elif choice == 6:
                self.find_book_by_isbn()
            elif choice == 7:
                self.loan_book()
            elif choice == 8:
                self.return_book()
            elif choice == 9:
                self.delete_book()
            elif choice == 10:
                break
    
    def add_book(self):
        """Add a new book to the database."""
        print("\n--- Add New Book ---")
        
        # Get book title
        title = get_valid_input(
            "Enter book title (or 'q' to go back): ",
            lambda x: validate_name(x, "Title"),
            "Title"
        )
        if title is None:
            return
        
        # Get book author
        author = get_valid_input(
            "Enter book author (or 'q' to go back): ",
            lambda x: validate_name(x, "Author"),
            "Author"
        )
        if author is None:
            return
        
        # Get book ISBN
        isbn = get_valid_input(
            "Enter book ISBN (or 'q' to go back): ",
            validate_isbn,
            "ISBN"
        )
        if isbn is None:
            return
        
        try:
            # Create new book
            book = Book(title=title, author=author, isbn=isbn)
            self.session.add(book)
            self.session.commit()
            
            print(f"\n✓ Book '{title}' by {author} added successfully!")
            print(f"Book ID: {book.id}")
            print(f"ISBN: {book.isbn}")
            
        except IntegrityError:
            self.session.rollback()
            print(f"\n✗ Error: A book with ISBN '{isbn}' already exists!")
        except ValueError as e:
            self.session.rollback()
            print(f"\n✗ Error: {e}")
        except Exception as e:
            self.session.rollback()
            print(f"\n✗ Unexpected error: {e}")
    
    def view_all_books(self):
        """Display all books."""
        print("\n--- All Books ---")
        
        books = self.session.query(Book).all()
        
        if not books:
            print("No books found.")
            return
        
        print(f"\nTotal books: {len(books)}")
        for book in books:
            print(f"\n{book}")
            if not book.is_available and book.borrower:
                print(f"  Borrowed by: {book.borrower.name} ({book.borrower.email})")
                if book.is_overdue():
                    print(f"  ⚠️  OVERDUE by {abs(book.days_until_due())} days!")
    
    def view_available_books(self):
        """Display only available books."""
        print("\n--- Available Books ---")
        
        available_books = self.session.query(Book).filter(Book.is_available == True).all()
        
        if not available_books:
            print("No books currently available.")
            return
        
        print(f"\nAvailable books: {len(available_books)}")
        for book in available_books:
            print(f"\n{book}")
    
    def find_book_by_title(self):
        """Find book by title."""
        print("\n--- Find Book by Title ---")
        
        title = input("Enter book title to search (or 'q' to go back): ").strip()
        if title.lower() == 'q':
            return
        
        books = self.session.query(Book).filter(
            Book.title.ilike(f"%{title}%")
        ).all()
        
        if not books:
            print(f"No books found with title containing '{title}'")
            return
        
        print(f"\nFound {len(books)} book(s):")
        for book in books:
            print(f"\n{book}")
            if not book.is_available and book.borrower:
                print(f"  Borrowed by: {book.borrower.name}")
    
    def find_book_by_author(self):
        """Find book by author."""
        print("\n--- Find Book by Author ---")
        
        author = input("Enter author name to search (or 'q' to go back): ").strip()
        if author.lower() == 'q':
            return
        
        books = self.session.query(Book).filter(
            Book.author.ilike(f"%{author}%")
        ).all()
        
        if not books:
            print(f"No books found by author containing '{author}'")
            return
        
        print(f"\nFound {len(books)} book(s):")
        for book in books:
            print(f"\n{book}")
            if not book.is_available and book.borrower:
                print(f"  Borrowed by: {book.borrower.name}")
    
    def find_book_by_isbn(self):
        """Find book by ISBN."""
        print("\n--- Find Book by ISBN ---")
        
        isbn = input("Enter ISBN to search (or 'q' to go back): ").strip()
        if isbn.lower() == 'q':
            return
        
        # Remove hyphens and spaces for search
        cleaned_isbn = isbn.replace("-", "").replace(" ", "")
        
        book = self.session.query(Book).filter(Book.isbn == cleaned_isbn).first()
        
        if not book:
            print(f"No book found with ISBN '{isbn}'")
            return
        
        print(f"\n{book}")
        if not book.is_available and book.borrower:
            print(f"Borrowed by: {book.borrower.name} ({book.borrower.email})")
            print(f"Borrowed on: {book.borrowed_date}")
            if book.is_overdue():
                print(f"⚠️  OVERDUE by {abs(book.days_until_due())} days!")
    
    def loan_book(self):
        """Loan a book to a member."""
        print("\n--- Loan Book to Member ---")
        
        # Get book ID
        book_id = get_integer_input("Enter book ID to loan (or 'q' to go back): ", 1)
        if book_id is None:
            return
        
        book = self.session.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            print(f"No book found with ID {book_id}")
            return
        
        if not book.is_available:
            print(f"✗ Book '{book.title}' is not available for loan")
            if book.borrower:
                print(f"Currently borrowed by: {book.borrower.name}")
                print(f"Due date: {book.due_date}")
            return
        
        # Get member ID
        member_id = get_integer_input("Enter member ID (or 'q' to go back): ", 1)
        if member_id is None:
            return
        
        member = self.session.query(Member).filter(Member.id == member_id).first()
        
        if not member:
            print(f"No member found with ID {member_id}")
            return
        
        # Check if member can borrow more books
        if not member.can_borrow_books():
            print(f"✗ Member '{member.name}' has reached the maximum limit of 5 borrowed books")
            return
        
        print(f"\nBook: '{book.title}' by {book.author}")
        print(f"Member: {member.name} ({member.email})")
        
        if get_yes_no_input("Confirm loan?"):
            try:
                book.borrow_to_member(member_id)
                self.session.commit()
                print(f"✓ Book loaned successfully!")
                print(f"Due date: {book.due_date}")
            except Exception as e:
                self.session.rollback()
                print(f"✗ Error loaning book: {e}")
        else:
            print("Loan cancelled.")
    
    def return_book(self):
        """Return a borrowed book."""
        print("\n--- Return Book ---")
        
        book_id = get_integer_input("Enter book ID to return (or 'q' to go back): ", 1)
        if book_id is None:
            return
        
        book = self.session.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            print(f"No book found with ID {book_id}")
            return
        
        if book.is_available:
            print(f"✗ Book '{book.title}' is not currently borrowed")
            return
        
        print(f"\nBook: '{book.title}' by {book.author}")
        if book.borrower:
            print(f"Borrowed by: {book.borrower.name} ({book.borrower.email})")
            print(f"Borrowed on: {book.borrowed_date}")
            print(f"Due date: {book.due_date}")
            
            if book.is_overdue():
                print(f"⚠️  This book is OVERDUE by {abs(book.days_until_due())} days!")
        
        if get_yes_no_input("Confirm return?"):
            try:
                book.return_book()
                self.session.commit()
                print(f"✓ Book returned successfully!")
            except Exception as e:
                self.session.rollback()
                print(f"✗ Error returning book: {e}")
        else:
            print("Return cancelled.")
    
    def delete_book(self):
        """Delete a book from the database."""
        print("\n--- Delete Book ---")
        
        book_id = get_integer_input("Enter book ID to delete (or 'q' to go back): ", 1)
        if book_id is None:
            return
        
        book = self.session.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            print(f"No book found with ID {book_id}")
            return
        
        if not book.is_available:
            print(f"\n✗ Cannot delete book '{book.title}'")
            print("This book is currently borrowed. Please return it first.")
            return
        
        print(f"\nBook to delete: {book}")
        
        if get_yes_no_input("Are you sure you want to delete this book?"):
            try:
                self.session.delete(book)
                self.session.commit()
                print(f"✓ Book '{book.title}' deleted successfully!")
            except Exception as e:
                self.session.rollback()
                print(f"✗ Error deleting book: {e}")
        else:
            print("Book deletion cancelled.")
    
    def __del__(self):
        """Close the database session."""
        if hasattr(self, 'session'):
            self.session.close()