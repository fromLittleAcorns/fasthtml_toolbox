# auth/database.py
from fasthtml.common import database
from pathlib import Path

class AuthDatabase:
    """Database manager owned by auth system"""

    def __init__(self, db_path="data/app.db"):
        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        # Create database connection
        self.db = database(db_path)
        self.db_path = db_path
        
        # Table references (will be populated)
        self.users = None
        self.sessions = None  # Optional session storage
        self.audit_log = None  # Optional security audit
    
    def initialize_auth_tables(self):
        """Initialize core auth tables"""
        from .models import User, Session
        
        # Users table (note fastlite will create the table if it does not exist, otherwise will return the current table)
        self.users = self.db.create(User, pk=User.pk)

        # Sessions table
        self.sessions = self.db.create(Session)
        
        return self.db
    
    def get_db(self):
        """Get database instance for app to add tables"""
        return self.db