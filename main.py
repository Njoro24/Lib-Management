import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the Library Management System."""
    try:
        # Import required modules
        from models import init_database
        from cli import MainMenu
        
        print("Initializing Library Management System...")
        
        # Initialize database (create tables if they don't exist)
        init_database()
        print("✓ Database initialized successfully!")
        
        # Create and run the main menu
        app = MainMenu()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please make sure all required dependencies are installed.")
        print("Run: pipenv install")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
        print("The application encountered an unexpected error and will now exit.")
        sys.exit(1)

if __name__ == "__main__":
    main()