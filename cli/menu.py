from .member_cli import MemberCLI
from .book_cli import BookCLI
from utils import get_integer_input

class MainMenu:
    
    def __init__(self):
        self.member_cli = MemberCLI()
        self.book_cli = BookCLI()
    
    def display_welcome(self):
        """Display welcome message."""
        print("\n" + "="*60)
        print("🏛️  WELCOME TO LIBRARY MANAGEMENT SYSTEM  🏛️")
        print("="*60)
        print("Manage your library's books and members efficiently!")
        print("="*60)
    
    def display_main_menu(self):
        """Display and handle main menu."""
        while True:
            print("\n" + "="*50)
            print("MAIN MENU")
            print("="*50)
            print("1. 👥 Manage Members")
            print("2. 📚 Manage Books")
            print("3. 📊 Library Statistics")
            print("4. 🚪 Exit")
            print("-" * 50)
            
            choice = get_integer_input("Enter your choice (1-4): ", 1, 4)
            
            if choice is None:
                continue
            elif choice == 1:
                self.member_cli.display_member_menu()
            elif choice == 2:
                self.book_cli.display_book_menu()
            elif choice == 3:
                self.display_statistics()
            elif choice == 4:
                self.exit_application()
                break
    
    def display_statistics(self):
        """Display library statistics."""
        print("\n" + "="*50)
        print("📊 LIBRARY STATISTICS")
        print("="*50)
        
        try:
            from models import Member, Book, get_db_session
            session = get_db_session()
            
            # Get statistics
            total_members = session.query(Member).count()
            total_books = session.query(Book).count()
            available_books = session.query(Book).filter(Book.is_available == True).count()
            borrowed_books = session.query(Book).filter(Book.is_available == False).count()
            
            # Get overdue books
            from datetime import date
            overdue_books = session.query(Book).filter(
                Book.is_available == False,
                Book.due_date < date.today()
            ).count()
            
            # Display statistics
            print(f"👥 Total Members: {total_members}")
            print(f"📚 Total Books: {total_books}")
            print(f"✅ Available Books: {available_books}")
            print(f"📖 Borrowed Books: {borrowed_books}")
            
            if overdue_books > 0:
                print(f"⚠️  Overdue Books: {overdue_books}")
            else:
                print(f"✅ Overdue Books: {overdue_books}")
            
            # Calculate percentages
            if total_books > 0:
                borrowed_percentage = (borrowed_books / total_books) * 100
                print(f"\n📈 Books in circulation: {borrowed_percentage:.1f}%")
            
            # Show members with most books
            members_with_books = session.query(Member).join(Book).all()
            if members_with_books:
                print("\n🏆 Active borrowers:")
                member_book_count = {}
                for member in members_with_books:
                    if member.id not in member_book_count:
                        member_book_count[member.id] = {
                            'name': member.name,
                            'count': len(member.borrowed_books)
                        }
                
                # Sort by book count
                sorted_members = sorted(
                    member_book_count.values(),
                    key=lambda x: x['count'],
                    reverse=True
                )[:5]  # Top 5
                
                for i, member_info in enumerate(sorted_members, 1):
                    if member_info['count'] > 0:
                        print(f"  {i}. {member_info['name']}: {member_info['count']} book(s)")
            
            session.close()
            
        except Exception as e:
            print(f"Error retrieving statistics: {e}")
        
        input("\nPress Enter to continue...")
    
    def exit_application(self):
        """Handle application exit."""
        print("\n" + "="*50)
        print("Thank you for using Library Management System!")
        print("📚 Happy reading! 📚")
        print("="*50)
        
        # Clean up resources
        try:
            self.member_cli.__del__()
            self.book_cli.__del__()
        except:
            pass
    
    def run(self):
        """Run the main application."""
        try:
            self.display_welcome()
            self.display_main_menu()
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
            self.exit_application()
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please report this issue.")
            self.exit_application()