from fasthtml.common import *
from auth import AuthManager

# Initialize auth system
auth = AuthManager(
    db_path="data/app.db",
    config={
        'login_path': '/auth/login',
        'public_paths': ['/about', '/contact'],  # Additional public pages
        'allow_registration': True,  # Enable registration
        'allow_password_reset': False,  # Disable password reset for now
    }
)

# Initialize database
try:
    db = auth.initialize()
    print("✓ Database initialized successfully")
except Exception as e:
    print(f"✗ Database initialization failed: {e}")
    raise

# Create beforeware
try:
    beforeware = auth.create_beforeware(
        additional_public_paths=['/api/webhook', '/status']
    )
    print("✓ Beforeware created successfully")
except Exception as e:
    print(f"✗ Beforeware creation failed: {e}")
    raise

# Create app with auth beforeware
app = FastHTML(
    before=beforeware,
    secret_key='change-me-in-production'
)

# Register auth routes
try:
    routes = auth.register_routes(app)
    print(f"✓ Auth routes registered: {list(routes.keys())}")
except Exception as e:
    print(f"✗ Route registration failed: {e}")
    raise

# Test basic route
@app.route("/")
def home(req):
    user = req.scope.get('user')
    if user:
        return Title("Home"), Container(
            H1(f"Welcome, {user.username}!"),
            P(f"Role: {user.role}"),
            Div(
                A("Profile", href="/auth/profile", cls="btn"),
                " | ",
                A("Logout", href="/auth/logout", cls="btn")
            )
        )
    else:
        return Title("Home"), Container(
            H1("Welcome!"),
            P("Please ", A("login", href="/auth/login"), " to continue.")
        )

# Test admin route
@app.route("/admin")
@auth.require_admin()
def admin_panel(req):
    return Title("Admin Panel"), Container(
        H1("Admin Panel"),
        P("Admin only content"),
        A("← Back to Home", href="/")
    )

# Test manager route
@app.route("/manager") 
@auth.require_role('manager', 'admin')
def manager_view(req):
    user = req.scope['user']
    return Title("Manager View"), Container(
        H1("Manager View"),
        P(f"Welcome, {user.username}!"),
        P(f"Your role: {user.role}"),
        A("← Back to Home", href="/")
    )

# Public route for testing
@app.route("/about")
def about():
    return Title("About"), Container(
        H1("About"),
        P("This is a public page that doesn't require login."),
        A("Home", href="/")
    )

if __name__ == "__main__":
    print("\n🚀 Starting FastHTML app with authentication...")
    print("📝 Default admin user: username='admin', password='admin123'")
    print("🌐 Visit: http://localhost:5001")
    serve(port=5001)