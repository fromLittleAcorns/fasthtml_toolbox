### Example login and database connection using Beforeware

from fasthtml.common import *
from monsterui.all import *
from config import DB_CONFIG, APP_CONFIG
import logging
from datetime import datetime

from models.database import db
from auth import AuthManager, User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"category_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Base_app_devel")

# Note that database access is managed by fastlite, which is a part of fastHTML

# Create instance of AuthManager class to handle users and authentication
auth = AuthManager(db=bd, config=)
# Check and setup user table if necessary
users = db.create(Users)
initialize_users_table()

def create_app():
    """Create and configure the FastHTML application"""
    
    print("🔧 Creating FastHTML application...")
    
    # Initialize app with MonsterUI theme and configuration
    app = FastHTML(
        hdrs=Theme.blue.headers(),
        before=create_beforeware(),
        debug=APP_CONFIG.get("debug", True),
        
        # Session configuration
        secret_key=APP_CONFIG.get("secret_key", "your-long-random-secret-key-here"),
        session_cookie=APP_CONFIG.get("session_cookie", "parts_mgmt_session"),
        sess_https_only=APP_CONFIG.get("sess_https_only", False),
        
        static_path=APP_CONFIG.get("static_path", "static"),
        title="Parts Management System"
    )
    
    print("🔧 Setting up routes...")
    
    # Setup routes with error handling
    try:
        print("   - Setting up auth routes...")
        setup_auth_routes(app)
        
        print("   - Setting up dashboard routes...")
        setup_dashboard_routes(app)
        
        print("   - Setting up parts routes...")
        setup_parts_routes(app)
        
        print("   - Setting up upload routes...")
        setup_upload_routes(app)
        
        print("✅ All routes setup complete!")
        
    except Exception as e:
        print(f"❌ Error setting up routes: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    return app



