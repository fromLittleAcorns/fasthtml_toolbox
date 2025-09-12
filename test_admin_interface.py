# test_admin_interface.py - Test the new admin interface functionality

import os
import tempfile
import traceback
from datetime import datetime

def test_admin_routes_import():
    """Test that AdminRoutes can be imported"""
    print("📦 Testing AdminRoutes import...")
    
    try:
        from fasthtml_auth.admin_routes import AdminRoutes
        print("  ✅ AdminRoutes imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Failed to import AdminRoutes: {e}")
        return False

def test_repository_delete():
    """Test the delete method in UserRepository"""
    print("\n🗑️ Testing user deletion...")
    
    try:
        from fasthtml_auth.manager import AuthManager
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test.db")
        
        auth = AuthManager(db_path=db_path)
        db = auth.initialize()
        repo = auth.user_repo
        
        # Create a test user
        test_user = repo.create(
            username="deletetest",
            email="delete@test.com",
            password="testpass123",
            role="user"
        )
        assert test_user is not None, "User should be created"
        user_id = test_user.id
        
        # Delete the user
        success = repo.delete(user_id)
        assert success, "Delete should return True"
        
        # Verify user is deleted
        deleted_user = repo.get_by_id(user_id)
        assert deleted_user is None, "User should be deleted"
        print("  ✅ User deletion works")
        
        # Test deleting non-existent user
        success = repo.delete(99999)
        assert not success, "Deleting non-existent user should return False"
        print("  ✅ Non-existent user deletion handled correctly")
        
        # Clean up
        try:
            os.unlink(db_path)
            os.rmdir(temp_dir)
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"  ❌ Delete test failed: {e}")
        traceback.print_exc()
        return False

def test_repository_count_by_role():
    """Test the count_by_role method"""
    print("\n📊 Testing user count by role...")
    
    try:
        from fasthtml_auth.manager import AuthManager
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test.db")
        
        auth = AuthManager(db_path=db_path)
        db = auth.initialize()
        repo = auth.user_repo
        
        # Create users with different roles
        repo.create("user1", "user1@test.com", "pass123", "user")
        repo.create("user2", "user2@test.com", "pass123", "user")
        repo.create("manager1", "manager1@test.com", "pass123", "manager")
        repo.create("admin2", "admin2@test.com", "pass123", "admin")
        
        # Get counts (remember default admin exists)
        counts = repo.count_by_role()
        
        assert counts['user'] == 2, f"Should have 2 users, got {counts['user']}"
        assert counts['manager'] == 1, f"Should have 1 manager, got {counts['manager']}"
        assert counts['admin'] == 2, f"Should have 2 admins (including default), got {counts['admin']}"
        
        print(f"  ✅ Role counts: {counts}")
        
        # Clean up
        try:
            os.unlink(db_path)
            os.rmdir(temp_dir)
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"  ❌ Count by role test failed: {e}")
        traceback.print_exc()
        return False

def test_admin_interface_registration():
    """Test that admin interface can be registered"""
    print("\n🎛️ Testing admin interface registration...")
    
    try:
        from fasthtml.common import FastHTML
        from fasthtml_auth.manager import AuthManager
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test.db")
        
        auth = AuthManager(db_path=db_path)
        db = auth.initialize()
        beforeware = auth.create_beforeware()
        
        # Create app
        app = FastHTML(
            before=beforeware,
            secret_key='test-secret'
        )
        
        # Register routes WITHOUT admin
        routes_basic = auth.register_routes(app, include_admin=False)
        basic_count = len(auth.route_handler.routes)
        print(f"  ✅ Basic routes registered: {basic_count} routes")
        
        # Create new app for admin test
        app2 = FastHTML(
            before=beforeware,
            secret_key='test-secret'
        )
        
        # Register routes WITH admin
        routes_admin = auth.register_routes(app2, include_admin=True)
        admin_count = len(auth.route_handler.routes)
        print(f"  ✅ Admin routes registered: {admin_count} routes")
        
        # Check that admin routes were added
        assert admin_count > basic_count, "Admin interface should add more routes"
        
        # Check for specific admin routes
        expected_admin_routes = [
            'admin_dashboard',
            'admin_users_list',
            'admin_user_create_form',
            'admin_user_create_submit',
            'admin_user_edit_form',
            'admin_user_edit_submit',
            'admin_user_delete_confirm',
            'admin_user_delete_submit'
        ]
        
        for route_name in expected_admin_routes:
            assert route_name in auth.route_handler.routes, f"Missing admin route: {route_name}"
        
        print(f"  ✅ All expected admin routes present")
        
        # Clean up
        try:
            os.unlink(db_path)
            os.rmdir(temp_dir)
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"  ❌ Admin interface registration test failed: {e}")
        traceback.print_exc()
        return False

def test_admin_forms():
    """Test that admin forms can be created"""
    print("\n📝 Testing admin forms...")
    
    try:
        from fasthtml_auth.admin_routes import AdminRoutes
        from fasthtml_auth.manager import AuthManager
        from fasthtml_auth.models import User
        
        # Create a mock auth manager
        auth = AuthManager(db_path=":memory:")
        auth.initialize()
        
        admin_routes = AdminRoutes(auth)
        
        # Test user list header
        header = admin_routes._create_user_list_header()
        assert header is not None, "Header should be created"
        print("  ✅ User list header created")
        
        # Test filters section
        filters = admin_routes._create_filters_section("", "", "", "/auth/admin")
        assert filters is not None, "Filters should be created"
        print("  ✅ Filters section created")
        
        # Test empty users table
        empty_table = admin_routes._create_users_table([], "/auth/admin")
        assert empty_table is not None, "Empty table should be created"
        print("  ✅ Empty users table created")
        
        # Test users table with data
        test_users = [
            User(id=1, username="test1", email="test1@example.com", 
                 password="hash", role="user", active=True),
            User(id=2, username="test2", email="test2@example.com", 
                 password="hash", role="manager", active=False)
        ]
        
        users_table = admin_routes._create_users_table(test_users, "/auth/admin")
        assert users_table is not None, "Users table should be created"
        print("  ✅ Users table with data created")
        
        # Test create user form
        create_form = admin_routes._create_user_form("/auth/admin/users/create")
        assert create_form is not None, "Create form should be created"
        print("  ✅ Create user form created")
        
        # Test edit user form
        test_user = User(id=1, username="edituser", email="edit@example.com",
                        password="hash", role="admin", active=True)
        edit_form = admin_routes._create_edit_user_form(test_user, "/auth/admin/users/1/edit")
        assert edit_form is not None, "Edit form should be created"
        print("  ✅ Edit user form created")
        
        # Test delete confirmation
        delete_confirm = admin_routes._create_delete_confirmation(test_user, "/auth/admin")
        assert delete_confirm is not None, "Delete confirmation should be created"
        print("  ✅ Delete confirmation created")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Admin forms test failed: {e}")
        traceback.print_exc()
        return False

def test_filter_users():
    """Test user filtering functionality"""
    print("\n🔍 Testing user filtering...")
    
    try:
        from fasthtml_auth.admin_routes import AdminRoutes
        from fasthtml_auth.manager import AuthManager
        from fasthtml_auth.models import User
        
        auth = AuthManager(db_path=":memory:")
        admin_routes = AdminRoutes(auth)
        
        # Create test users
        users = [
            User(id=1, username="alice", email="alice@example.com", 
                 password="hash", role="admin", active=True),
            User(id=2, username="bob", email="bob@example.com", 
                 password="hash", role="manager", active=True),
            User(id=3, username="charlie", email="charlie@test.com", 
                 password="hash", role="user", active=False),
            User(id=4, username="david", email="david@example.com", 
                 password="hash", role="user", active=True),
        ]
        
        # Test search filter
        filtered = admin_routes._filter_users(users, "alice", "", "")
        assert len(filtered) == 1, "Should find 1 user named alice"
        assert filtered[0].username == "alice"
        print("  ✅ Search by username works")
        
        # Test email search
        filtered = admin_routes._filter_users(users, "test.com", "", "")
        assert len(filtered) == 1, "Should find 1 user with test.com email"
        assert filtered[0].username == "charlie"
        print("  ✅ Search by email works")
        
        # Test role filter
        filtered = admin_routes._filter_users(users, "", "user", "")
        assert len(filtered) == 2, "Should find 2 users with 'user' role"
        print("  ✅ Role filter works")
        
        # Test status filter
        filtered = admin_routes._filter_users(users, "", "", "inactive")
        assert len(filtered) == 1, "Should find 1 inactive user"
        assert filtered[0].username == "charlie"
        print("  ✅ Status filter works")
        
        # Test combined filters
        filtered = admin_routes._filter_users(users, "", "user", "active")
        assert len(filtered) == 1, "Should find 1 active user"
        assert filtered[0].username == "david"
        print("  ✅ Combined filters work")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Filter users test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all admin interface tests"""
    print("🚀 FastHTML-Auth Admin Interface Test Suite")
    print("=" * 50)
    
    tests = [
        test_admin_routes_import,
        test_repository_delete,
        test_repository_count_by_role,
        test_admin_interface_registration,
        test_admin_forms,
        test_filter_users,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__:<35} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All admin interface tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Please fix issues before release.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)