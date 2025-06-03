from models.members import Member
from models.database import get_db_session

def find_member_by_name(self):
    """Find member by name."""
    print("\n--- Find Member by Name ---")
    
    name = input("Enter member name to search (or 'q' to go back): ").strip()
    if name.lower() == 'q':
        return
    
    # Use like() instead of ilike() for better SQLite compatibility
    members = self.session.query(Member).filter(
        Member.name.like(f"%{name}%")
    ).all()
    
    # If no results with like(), try case-insensitive search manually
    if not members:
        members = self.session.query(Member).filter(
            Member.name.contains(name)
        ).all()
    
    # If still no results, try even more flexible search
    if not members:
        all_members = self.session.query(Member).all()
        members = [m for m in all_members if name.lower() in m.name.lower()]
    
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
    
    # Try exact match first
    member = self.session.query(Member).filter(
        Member.email == email
    ).first()
    
    # If no exact match, try partial match
    if not member:
        member = self.session.query(Member).filter(
            Member.email.like(f"%{email}%")
        ).first()
    
    # If still no match, try case-insensitive search
    if not member:
        all_members = self.session.query(Member).all()
        for m in all_members:
            if email.lower() in m.email.lower():
                member = m
                break
    
    if not member:
        print(f"No member found with email containing '{email}'")
        return
    
    print(f"\n{member}")
    if member.borrowed_books:
        print(f"Currently borrowed books: {len(member.borrowed_books)}")
        for book in member.borrowed_books:
            print(f"  - {book.title} by {book.author} (Due: {book.due_date})")