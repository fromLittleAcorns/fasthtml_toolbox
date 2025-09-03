# test_package.py - Complete package functionality test
"""
Test script to verify FastHTML-Auth package functionality
Run this before packaging to ensure everything works correctly.
"""

import os
import tempfile
import traceback
from datetime import datetime


def test_basic_imports():
    """Test that all imports work correctly"""
    print("🔍 Testing imports...")

    try:
        # Test individual components
        from fasthtml_auth.models import User, Session
        from fasthtml_auth.database import AuthDatabase
        from fasthtml_auth.repository import UserRepository
        from fasthtml_auth.middleware import AuthBeforeware
        from fasthtml_auth.routes import AuthRoutes
        print("  ✅ All component imports successful")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected import error: {e}")
        return False

def test_user_model():
    """Test User model functionality"""
    print("\n👤 Testing User model...")
    
    try:
        from fasthtml_auth.models import User
        
        # Test password hashing
        password = "testpassword123"
        user = User(
            id=None,
            username="testuser", 
            email="test@example.com",
            password=password,
            role="user"
        )
        
        # Check that password was hashed in __post_init__
        assert user.password != password, "Password should be hashed"
        assert User.is_hashed(user.password), "Password should be detected as hashed"
        print(f"  ✅ Password hashing works (hash starts with: {user.password[:10]}...)")
        
        # Test password verification
        assert User.verify_password(password, user.password), "Password verification should work"
        assert not User.verify_password("wrongpassword", user.password), "Wrong password should fail"
        print("  ✅ Password verification works")
        
        # Test timestamps
        assert user.created_at, "created_at should be set"
        assert user.last_login, "last_login should be set"
        print("  ✅ Timestamps set correctly")
        
        return True
        
    except Exception as e:
        print(f"  ❌ User model test failed: {e}")
        traceback.print_exc()
        return False

def test_auth_manager():
    """Test AuthManager initialization and basic functionality"""
    print("\n🔐 Testing AuthManager...")
    
    try:
        from fasthtml_auth.manager import AuthManager
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test.db")
        
        # Initialize auth manager
        config = {
            'allow_registration': True,
            'public_paths': ['/public', '/about']
        }
        
        auth = AuthManager(db_path=db_path, config=config)
        print("  ✅ AuthManager created")
        
        # Initialize database
        db = auth.initialize()
        assert db is not None, "Database should be initialized"
        assert auth.user_repo is not None, "UserRepository should be created"
        print("  ✅ Database initialized")
        
        # Check default admin was created
        admin_user = auth.get_user('admin')
        assert admin_user is not None, "Default admin should be created"
        assert admin_user.role == 'admin', "Admin should have admin role"
        print("  ✅ Default admin user created")
        
        # Clean up
        try:
            os.unlink(db_path)
            os.rmdir(temp_dir)
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"  ❌ AuthManager test failed: {e}")
        traceback.print_exc()
        return False

def test_user_operations():
    """Test user creation, authentication, and updates"""
    print("\n👥 Testing user operations...")
    
    try:
        from fasthtml_auth.manager import AuthManager
        from fasthtml_auth.models import User
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test.db")
        
        auth = AuthManager(db_path=db_path)
        db = auth.initialize()
        repo = auth.user_repo
        
        # Test user creation
        new_user = repo.create(
            username="newuser",
            email="new@example.com", 
            password="password123",
            role="user"
        )
        print(f"New User: {new_user}")
        assert new_user is not None, "User should be created"
        assert new_user.username == "newuser", "Username should be correct"
        print("  ✅ User creation works")
        
        # Test user retrieval
        found_user = repo.get_by_username("newuser")
        assert found_user is not None, "Should find created user"
        assert found_user.email == "new@example.com", "Email should match"
        print("  ✅ User retrieval works")
        
        # Test authentication
        auth_user = repo.authenticate("newuser", "password123")
        assert auth_user is not None, "Authentication should succeed"
        print("  ✅ User authentication works")
        
        # Test failed authentication
        failed_auth = repo.authenticate("newuser", "wrongpassword")
        assert failed_auth is None, "Wrong password should fail"
        print("  ✅ Failed authentication handled correctly")
        
        # Test user update
        success = repo.update(found_user.id, email="updated@example.com")
        assert success, "Update should succeed"
        
        updated_user = repo.get_by_username("newuser")
        assert updated_user.email == "updated@example.com", "Email should be updated"
        print("  ✅ User update works")
        
        # Test password update
        success = repo.update(found_user.id, password="newpassword123")
        assert success, "Password update should succeed"
        
        # Test authentication with new password
        auth_user = repo.authenticate("newuser", "newpassword123")
        assert auth_user is not None, "Authentication with new password should work"
        print("  ✅ Password update and authentication works")
        
        # Clean up
        try:
            os.unlink(db_path)
            os.rmdir(temp_dir)
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"  ❌ User operations test failed: {e}")
        traceback.print_exc()
        return False

def test_middleware():
    """Test middleware creation"""
    print("\n🛡️  Testing middleware...")
    
    try:
        from fasthtml_auth.manager import AuthManager
        
        auth = AuthManager(db_path=":memory:")  # In-memory database
        auth.initialize()
        
        # Test beforeware creation
        beforeware = auth.create_beforeware(additional_public_paths=['/api/test'])
        assert beforeware is not None, "Beforeware should be created"
        print("  ✅ Beforeware creation works")
        
        # Test decorators
        admin_decorator = auth.require_admin()
        role_decorator = auth.require_role('manager', 'admin')
        assert admin_decorator is not None, "Admin decorator should be created"
        assert role_decorator is not None, "Role decorator should be created"
        print("  ✅ Access decorators work")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Middleware test failed: {e}")
        traceback.print_exc()
        return False

def test_forms():
    """Test form generation"""
    print("\n📝 Testing forms...")
    
    try:
        from fasthtml_auth.forms import (
            create_login_form, 
            create_register_form, 
            create_forgot_password_form,
            create_profile_form
        )
        from fasthtml_auth.models import User
        
        # Test login form
        login_form = create_login_form()
        assert login_form is not None, "Login form should be created"
        print("  ✅ Login form creation works")
        
        # Test register form  
        register_form = create_register_form()
        assert register_form is not None, "Register form should be created"
        print("  ✅ Register form creation works")
        
        # Test forgot password form
        forgot_form = create_forgot_password_form()
        assert forgot_form is not None, "Forgot password form should be created"
        print("  ✅ Forgot password form creation works")
        
        # Test profile form with sample user
        sample_user = User(
            id=1,
            username="testuser",
            email="test@example.com", 
            password="hashedpassword",
            role="user",
            created_at=datetime.now().isoformat(),
            last_login=datetime.now().isoformat()
        )
        
        profile_form = create_profile_form(sample_user)
        assert profile_form is not None, "Profile form should be created"
        print("  ✅ Profile form creation works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Forms test failed: {e}")
        traceback.print_exc()
        return False

def test_dependencies():
    """Test that all required dependencies are available"""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ('bcrypt', '4.0.0'),
        ('fasthtml', '0.10.0'),  # python-fasthtml
        ('monsterui', '0.1.0'),
        ('fastlite', '0.0.1'),
    ]
    
    try:
        import bcrypt
        print(f"  ✅ bcrypt {bcrypt.__version__} available")
        
        import fasthtml
        # FastHTML might not have __version__, so try different approaches
        try:
            fh_version = fasthtml.__version__
        except AttributeError:
            fh_version = "installed"
        print(f"  ✅ fasthtml {fh_version} available")
        
        import monsterui
        try:
            mu_version = monsterui.__version__
        except AttributeError:
            mu_version = "installed"  
        print(f"  ✅ monsterui {mu_version} available")
        
        import fastlite
        try:
            fl_version = fastlite.__version__
        except AttributeError:
            fl_version = "installed"
        print(f"  ✅ fastlite {fl_version} available")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Dependency check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 FastHTML-Auth Package Test Suite")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_basic_imports,
        test_user_model,
        test_auth_manager,
        test_user_operations,
        test_middleware,
        test_forms,
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
        print(f"{i+1}. {test.__name__:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your package is ready for packaging.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before packaging.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)