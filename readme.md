# FastHTML-Auth

**Complete authentication system for FastHTML applications with built-in admin interface**

Drop-in authentication with beautiful UI, role-based access control, and a powerful admin dashboard for user management. No configuration required – just install and go!

```bash
pip install fasthtml-auth
```

[![PyPI version](https://badge.fury.io/py/fasthtml-auth.svg)](https://badge.fury.io/py/fasthtml-auth)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## ⭐ Key Features

- 🔐 **Complete Authentication** - Login, logout, registration with secure bcrypt hashing
- 👑 **Built-in Admin Interface** - Full user management dashboard (NEW!)
- 🎨 **Beautiful UI** - Responsive MonsterUI components, zero custom CSS needed
- 🛡️ **Role-Based Access** - User, Manager, Admin roles with decorators
- 📱 **Mobile Ready** - Works perfectly on all devices
- ⚡ **Zero Config** - Works out of the box, customize as needed

---

## 🚀 Quick Start

### Basic Authentication

```python
from fasthtml.common import *
from monsterui.all import *
from fasthtml_auth import AuthManager

# Initialize auth system
auth = AuthManager(db_path="data/app.db")
db = auth.initialize()
beforeware = auth.create_beforeware()

# Create app
app = FastHTML(before=beforeware, hdrs=Theme.blue.headers())
auth.register_routes(app)

@app.route("/")
def dashboard(req):
    user = req.scope['user']  # Automatically available
    return H1(f"Welcome, {user.username}!")

@app.route("/admin")
@auth.require_admin()
def admin_only(req):
    return H1("Admin Area")

serve()
```

**That's it!** Your app now has:
- Login/logout at `/auth/login` and `/auth/logout`
- User registration at `/auth/register`
- Profile management at `/auth/profile`
- Role-based access control
- Default admin account: `admin` / `admin123`

---

## 👑 Built-in Admin Interface

Enable powerful user management with one parameter:

```python
# Add this one parameter to get a complete admin dashboard
auth.register_routes(app, include_admin=True)
```

**Instantly adds:**

| Feature | Route | Description |
|---------|-------|-------------|
| 📊 **Admin Dashboard** | `/auth/admin` | User statistics and quick actions |
| 👥 **User Management** | `/auth/admin/users` | List, search, filter all users |
| ➕ **Create Users** | `/auth/admin/users/create` | Add users with role assignment |
| ✏️ **Edit Users** | `/auth/admin/users/{id}/edit` | Modify details, roles, status |
| 🗑️ **Delete Users** | `/auth/admin/users/{id}/delete` | Remove users (with protection) |

### Admin Interface Features

- **🔍 Search & Filter** - Find users by username, email, role, or status
- **📄 Pagination** - Handle thousands of users efficiently  
- **🛡️ Safety Features** - Prevent self-deletion and last admin removal
- **📊 Statistics Dashboard** - User counts by role and status
- **🎨 Beautiful UI** - Consistent MonsterUI design throughout

---

## 📖 Real-World Example

See **FastHTML-Auth** in action with a complete todo application:

**[📝 FastHTML Todo App](https://github.com/fromLittleAcorns/fasthtml_todo)**

This real-world example shows:
- User authentication and registration
- Role-based task management
- Admin interface for user management
- Database integration patterns
- Production deployment setup

---

## ⚙️ Configuration

```python
config = {
    'allow_registration': True,              # Enable user registration
    'public_paths': ['/about', '/api'],      # Routes that skip authentication  
    'login_path': '/auth/login',             # Custom login URL
}

auth = AuthManager(db_path="data/app.db", config=config)
```

## 🔐 Role-Based Access Control

### Built-in Roles
- **`user`** - Basic authenticated access
- **`manager`** - Manager privileges + user access
- **`admin`** - Full system access + admin interface

### Route Protection
```python
# Require specific roles
@app.route("/manager-area")
@auth.require_role('manager', 'admin')
def manager_view(req):
    return H1("Manager+ Only")

# Admin only (shortcut)
@app.route("/admin")
@auth.require_admin()
def admin_panel(req):
    return H1("Admin Only")

# Check roles in templates
@app.route("/dashboard")
def dashboard(req):
    user = req.scope['user']
    
    admin_link = A("Admin Panel", href="/auth/admin") if user.role == 'admin' else None
    return Div(admin_link)
```

## 📊 User Object

In protected routes, access user data via `req.scope['user']`:

```python
user.id          # Unique user ID  
user.username    # Username
user.email       # Email address
user.role        # 'user', 'manager', or 'admin'
user.active      # Boolean - account status
user.created_at  # Account creation timestamp
user.last_login  # Last login timestamp
```

## 🎨 Styling & Themes

FastHTML-Auth uses [MonsterUI](https://github.com/answerdotai/monsterui) for beautiful, responsive components:

```python
# Choose your theme
app = FastHTML(
    before=beforeware,
    hdrs=Theme.blue.headers()    # or red, green, slate, etc.
)
```

All forms include professional styling, validation, error handling, and mobile optimization.

## 🛠️ API Reference

### AuthManager
```python
auth = AuthManager(db_path="data/app.db", config={})
auth.initialize()                                    # Set up database
auth.register_routes(app, include_admin=True)        # Add all routes
auth.create_beforeware()                             # Create middleware

@auth.require_admin()                                # Admin-only decorator
@auth.require_role('manager', 'admin')               # Role-based decorator
```

### Available Routes

**Authentication Routes:**
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - Logout and redirect  
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/profile` - Profile management

**Admin Routes** (when `include_admin=True`):
- `GET /auth/admin` - Admin dashboard
- `GET /auth/admin/users` - User management
- `GET/POST /auth/admin/users/create` - Create user
- `GET/POST /auth/admin/users/{id}/edit` - Edit user
- `GET/POST /auth/admin/users/{id}/delete` - Delete user

## 📁 Examples

For complete examples, see the `/examples` directory:

- [`basic_app.py`](examples/basic_app.py) - Simple authentication setup
- [`example_with_admin.py`](examples/example_with_admin.py) - Full admin interface demo
- [**FastHTML Todo App**](https://github.com/fromLittleAcorns/fasthtml_todo) - Real-world application

## 🔒 Security Features

- **Bcrypt password hashing** - Industry standard security
- **Session management** - Secure session handling with FastHTML
- **Remember me functionality** - Optional persistent sessions
- **Role-based protection** - Automatic route access control
- **Admin safety** - Prevent self-deletion and last admin removal
- **Input validation** - Server-side validation for all forms

## 📦 Installation & Dependencies

```bash
pip install fasthtml-auth
```

**Dependencies:**
- `python-fasthtml>=0.12.0` - Web framework
- `monsterui>=1.0.20` - UI components  
- `fastlite>=0.2.0` - Database ORM
- `bcrypt>=4.0.0` - Password hashing

## 🤝 Contributing

We welcome contributions! Areas for contribution:

- Password reset functionality
- Two-factor authentication  
- OAuth integration (Google, GitHub)
- Email verification
- Bulk user operations
- Custom user fields

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📝 Changelog

### v0.2.0 (Current Release)
- ✅ Built-in admin interface for user management
- ✅ User CRUD operations with beautiful UI
- ✅ Dashboard with user statistics
- ✅ Search, filter, and pagination
- ✅ Safety features for admin operations

### v0.1.2
- ✅ "Remember me" functionality
- ✅ Terms acceptance validation
- ✅ Improved form styling

### v0.1.0
- ✅ Initial release with core authentication
- ✅ Role-based access control
- ✅ MonsterUI integration

---

**FastHTML-Auth** - Authentication made simple for FastHTML applications.

For questions and support: [GitHub Issues](https://github.com/fromlittleacorns/fasthtml-auth/issues)