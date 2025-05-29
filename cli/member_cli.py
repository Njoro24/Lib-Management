from models import Member, get_db_session
from utils import (
    validate_name, validate_email, validate_phone,
    get_valid_input, get_yes_no_input, get_integer_input
)
from sqlalchemy.exc import IntegrityError

class MemberCLI:
    
    def __init__(self):
        self.session = get_db_session()
    
    def display_member_menu(self):
        """Display member management menu."""
        while True:
            print("\n" + "="*50)
            print("MEMBER MANAGEMENT")
            print("="*50)
            print("1. Add new member")
            print("2. View all members")
            print("3. Find member by name")
            print("4. Find member by email")
            print("5. View member's borrowed books")
            print("6. Delete member")
            print("7. Back to main menu")
            
            choice = get_integer_input("Enter your choice (1-7): ", 1, 7)
            
            if choice is None:
                continue
            elif choice == 1:
                self.add_member()
            elif choice == 2:
                self.view_all_members()
            elif choice == 3:
                self.find_member_by_name()
            elif choice == 4:
                self.find_member_by_email()
            elif choice == 5:
                self.view_member_books()
            elif choice == 6:
                self.delete_member()
            elif choice == 7:
                break
    
    def add_member(self):
        """Add a new member to the database."""
        print("\n--- Add New Member ---")
        
        # Get member name
        name = get_valid_input(
            "Enter member name (or 'q' to go back): ",
            lambda x: validate_name(x, "Name"),
            "Name"
        )
        if name is None:
            return
        
        # Get member email
        email = get_valid_input(
            "Enter member email (or 'q' to go back): ",
            validate_email,
            "Email"
        )
        if email is None:
            return
        
        # Get member phone (optional)
        phone = get_valid_input(
            "Enter member phone (optional, or 'q' to go back): ",
            validate_phone,
            "Phone"
        )
        if phone is None:
            return
        
        # Handle empty phone
        if phone.strip() == "":
            phone = None
        
        try:
            # Create new member
            member = Member(name=name, email=email, phone=phone)
            self.session.add(member)
            self.session.commit()
            
            print(f"\n✓ Member '{name}' added successfully!")
            print(f"Member ID: {member.id}")
            print(f"Membership Date: {member.membership_date}")
            
        except IntegrityError:
            self.session.rollback()
            print(f"\n✗ Error: A member with email '{email}' already exists!")
        except ValueError as e:
            self.session.rollback()
            print(f"\n✗ Error: {e}")
        except Exception as e:
            self.session.rollback()
            print(f"\n✗ Unexpected error: {e}")
    
    def view_all_members(self):
        """Display all members."""
        print("\n--- All Members ---")
        
        members = self.session.query(Member).all()
        
        if not members:
            print("No members found.")
            return
        
        for member in members:
            print(f"\n{member}")
            if member.borrowed_books:
                print(f"  Currently borrowed books: {len(member.borrowed_books)}")
            else:
                print("  No books currently borrowed")
    
    def find_member_by_name(self):
        """Find member by name."""
        print("\n--- Find Member by Name ---")
        
        name = input("Enter member name to search (or 'q' to go back): ").strip()
        if name.lower() == 'q':
            return
        
        members = self.session.query(Member).filter(
            Member.name.ilike(f"%{name}%")
        ).all()
        
        if not members:
            print(f"No members found with name containing '{name}'")
            return
        
        print(f"\nFound {len(members)} member(s):")
        for member in members:
            print(f"\n{member}")
            if member.borrowed_books:
                print(f"  Currently borrowed books: {len(member.borrowed_books)}")
    
    def find_member_by_email(self):
        """Find member by email."""
        print("\n--- Find Member by Email ---")
        
        email = input("Enter member email to search (or 'q' to go back): ").strip()
        if email.lower() == 'q':
            return
        
        member = self.session.query(Member).filter(
            Member.email.ilike(f"%{email}%")
        ).first()
        
        if not member:
            print(f"No member found with email containing '{email}'")
            return
        
        print(f"\n{member}")
        if member.borrowed_books:
            print(f"Currently borrowed books: {len(member.borrowed_books)}")
            for book in member.borrowed_books:
                print(f"  - {book.title} by {book.author} (Due: {book.due_date})")
    
    def view_member_books(self):
        """View books borrowed by a specific member."""
        print("\n--- View Member's Borrowed Books ---")
        
        member_id = get_integer_input("Enter member ID (or 'q' to go back): ", 1)
        if member_id is None:
            return
        
        member = self.session.query(Member).filter(Member.id == member_id).first()
        
        if not member:
            print(f"No member found with ID {member_id}")
            return
        
        print(f"\nMember: {member.name} ({member.email})")
        
        if not member.borrowed_books:
            print("This member has no borrowed books.")
            return
        
        print(f"\nBorrowed Books ({len(member.borrowed_books)}):")
        for book in member.borrowed_books:
            status = "OVERDUE" if book.is_overdue() else f"Due in {book.days_until_due()} days"
            print(f"  - '{book.title}' by {book.author}")
            print(f"    ISBN: {book.isbn} | Borrowed: {book.borrowed_date} | {status}")
    
    def delete_member(self):
        """Delete a member from the database."""
        print("\n--- Delete Member ---")
        
        member_id = get_integer_input("Enter member ID to delete (or 'q' to go back): ", 1)
        if member_id is None:
            return
        
        member = self.session.query(Member).filter(Member.id == member_id).first()
        
        if not member:
            print(f"No member found with ID {member_id}")
            return
        
        # Check if member has borrowed books
        if member.borrowed_books:
            print(f"\n✗ Cannot delete member '{member.name}'")
            print(f"This member has {len(member.borrowed_books)} borrowed book(s).")
            print("Please return all books before deleting the member.")
            return
        
        print(f"\nMember to delete: {member}")
        
        if get_yes_no_input("Are you sure you want to delete this member?"):
            try:
                self.session.delete(member)
                self.session.commit()
                print(f"✓ Member '{member.name}' deleted successfully!")
            except Exception as e:
                self.session.rollback()
                print(f"✗ Error deleting member: {e}")
        else:
            print("Member deletion cancelled.")
    
    def __del__(self):
        """Close the database session."""
        if hasattr(self, 'session'):
            self.session.close()