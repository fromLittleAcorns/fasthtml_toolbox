# example_with_admin.py - Example showing admin interface usage

from fasthtml.common import *
from monsterui.all import *
from dotenv import load_dotenv
load_dotenv('../.env')
import sys
sys.path.insert(0, '..')
from fasthtml_auth.manager import AuthManager
oauth_enabled = True if os.getenv('OAUTH_REDIRECT_URL', None) is not None else False

# Initialize auth system with admin interface enabled
auth = AuthManager(
    db_path="data/app.db",
    config={
        'login_path': '/auth/login',
        'public_paths': ['/about', '/pricing'],
        'allow_registration': True,
        'allow_password_reset': False,
        'oauth_redirect_url': os.getenv('OAUTH_REDIRECT_URL' if oauth_enabled else None)
    }
)

# Initialize database
db = auth.initialize()
print("✓ Database initialized")

# Create beforeware
beforeware = auth.create_beforeware()
print("✓ Beforeware created")

# Create app with auth beforeware
app = FastHTML(
    before=beforeware,
    secret_key='change-me-in-production',
    hdrs=Theme.blue.headers()
)

# Setup oauth before registering routes
auth.setup_oauth(app, auth.config['oauth_redirect_url'])

# Register auth routes WITH ADMIN INTERFACE
routes = auth.register_routes(app, include_admin=True)  # ← Enable admin interface
print(f"✓ Auth routes registered with admin interface")
print(f"  Admin routes available:")
print(f"    • /auth/admin - Admin dashboard")
print(f"    • /auth/admin/users - User management")
print(f"    • /auth/admin/users/create - Create new user")
print(f"    • /auth/admin/users/edit?id=N - Edit user")
print(f"    • /auth/admin/users/delete?id=N - Delete user")

# Your main application routes
@app.route("/")
def home(req):
    user = req.scope.get('user')
    if user:
        return Title("Dashboard"), Container(
            DivFullySpaced(
                H1(f"Welcome, {user.username}!"),
                Div(
                    A("Profile", href="/auth/profile", cls=ButtonT.secondary),
                    " ",
                    A("Admin Panel", href="/auth/admin", cls=ButtonT.primary) if user.role == 'admin' else None,
                    " ",
                    A("Logout", href="/auth/logout", cls=ButtonT.secondary)
                )
            ),
            
            Grid(
                Card(
                    CardHeader(H3("Account Information")),
                    CardBody(
                        P(Strong("Username: "), user.username),
                        P(Strong("Email: "), user.email),
                        P(Strong("Role: "), user.role.title()),
                        P(Strong("Status: "), "Active" if user.active else "Inactive")
                    )
                ),
                
                Card(
                    CardHeader(H3("Quick Links")),
                    CardBody(
                        Div(
                            # Show admin link only to admins
                            A("User Management", href="/auth/admin/users", 
                              cls=ButtonT.primary) if user.role == 'admin' else None,
                            " ",
                            A("Manager View", href="/manager", 
                              cls=ButtonT.secondary) if user.role in ['manager', 'admin'] else None,
                            " ",
                            A("About Page", href="/about", cls=ButtonT.secondary),
                            cls="space-x-2"
                        )
                    )
                ) if user.role != 'user' else None,
                
                cols=1, cols_md=2
            ),
            
            cls=ContainerT.xl
        )
    else:
        return RedirectResponse("/auth/login", status_code=303)

# Manager view (accessible by managers and admins)
@app.route("/manager")
@auth.require_role('manager', 'admin')
def manager_view(req):
    user = req.scope['user']
    return Title("Manager View"), Container(
        DivFullySpaced(
            H1("Manager Dashboard"),
            A("← Back", href="/", cls=ButtonT.secondary)
        ),
        Alert("This area is for managers and administrators.", cls=AlertT.info),
        Card(
            CardHeader(H3("Manager Tools")),
            CardBody(
                P(f"Welcome, {user.username}!"),
                P(f"Your role: {user.role.title()}"),
                Hr(cls="my-4"),
                P("Manager features would go here...")
            )
        ),
        cls=ContainerT.lg
    )

# Public about page
@app.route("/about")
def about():
    return Title("About"), Container(
        DivFullySpaced(
            H1("About Our System"),
            A("← Home", href="/", cls=ButtonT.secondary)
        ),
        Card(
            CardHeader(H3("FastHTML-Auth Demo")),
            CardBody(
                P("This demonstrates the FastHTML-Auth package with admin interface."),
                Hr(cls="my-4"),
                H4("Features:", cls="font-semibold mb-2"),
                Ul(
                    Li("Complete user authentication"),
                    Li("Role-based access control"),
                    Li(Strong("Admin user management interface")),
                    Li("Beautiful MonsterUI components"),
                    Li("Session management"),
                    Li("Password hashing with bcrypt"),
                    cls="list-disc pl-6 space-y-1"
                ),
                Hr(cls="my-4"),
                H4("Test Accounts:", cls="font-semibold mb-2"),
                Table(
                    Thead(
                        Tr(Th("Username"), Th("Password"), Th("Role"))
                    ),
                    Tbody(
                        Tr(Td("admin"), Td("admin123"), Td("Admin")),
                        Tr(Td("manager"), Td("manager123"), Td("Manager")),
                        Tr(Td("user"), Td("user123"), Td("User"))
                    ),
                    cls="w-full"
                ),
                P("Note: Create these test accounts via the admin interface or registration.", 
                  cls="text-sm text-muted-foreground mt-2")
            )
        ),
        cls=ContainerT.lg
    )

# Pricing page (public)
@app.route("/pricing")
def pricing():
    return Title("Pricing"), Container(
        DivFullySpaced(
            H1("Pricing Plans"),
            A("← Home", href="/", cls=ButtonT.secondary)
        ),
        Grid(
            Card(
                CardHeader(H3("Basic")),
                CardBody(
                    H2("$9/mo", cls="text-3xl font-bold"),
                    P("For individual users"),
                    Hr(cls="my-4"),
                    Ul(
                        Li("Single user account"),
                        Li("Basic features"),
                        Li("Email support"),
                        cls="list-disc pl-6 space-y-1"
                    ),
                    A("Get Started", href="/auth/register", cls=ButtonT.primary + " w-full mt-4")
                )
            ),
            Card(
                CardHeader(H3("Team")),
                CardBody(
                    H2("$29/mo", cls="text-3xl font-bold"),
                    P("For small teams"),
                    Hr(cls="my-4"),
                    Ul(
                        Li("Up to 10 users"),
                        Li("Manager roles"),
                        Li("Priority support"),
                        cls="list-disc pl-6 space-y-1"
                    ),
                    A("Get Started", href="/auth/register", cls=ButtonT.primary + " w-full mt-4")
                )
            ),
            Card(
                CardHeader(H3("Enterprise")),
                CardBody(
                    H2("$99/mo", cls="text-3xl font-bold"),
                    P("For large organizations"),
                    Hr(cls="my-4"),
                    Ul(
                        Li("Unlimited users"),
                        Li("Admin dashboard"),
                        Li("24/7 support"),
                        cls="list-disc pl-6 space-y-1"
                    ),
                    A("Contact Sales", href="/about", cls=ButtonT.primary + " w-full mt-4")
                )
            ),
            cols=1, cols_md=3
        ),
        cls=ContainerT.xl
    )

if __name__ == "__main__":
    print("\n🚀 Starting FastHTML app with admin interface...")
    print("📝 Default admin: username='admin', password='admin123'")
    print("🌐 Visit: http://localhost:8000")
    print("\n📋 Available routes:")
    print("   • / (dashboard)")
    print("   • /auth/login")
    print("   • /auth/register")
    print("   • /auth/profile")
    print("   • /auth/admin (admin dashboard)")
    print("   • /auth/admin/users (user management)")
    print("   • /manager (manager+ only)")
    print("   • /about (public)")
    print("   • /pricing (public)")
    
    # Create some test users if they don't exist
    print("\n📦 Creating test users if needed...")
    
    # Create manager account if doesn't exist
    if not auth.user_repo.get_by_username('manager'):
        auth.user_repo.create(
            username='manager',
            email='manager@example.com',
            password='manager123',
            role='manager'
        )
        print("   ✓ Created manager account")
    
    # Create regular user account if doesn't exist
    if not auth.user_repo.get_by_username('user'):
        auth.user_repo.create(
            username='user',
            email='user@example.com',
            password='user123',
            role='user'
        )
        print("   ✓ Created user account")

    auth.setup_oauth(app, redirect_url=auth.config['oauth_redirect_url'])
    print("✓ oauth initialized")
    
    serve(port=8000)