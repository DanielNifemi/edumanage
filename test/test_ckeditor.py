#!/usr/bin/env python
"""
Test script to verify django-ckeditor-5 is working properly
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

def test_ckeditor_5():
    try:
        # Test basic import
        import django_ckeditor_5
        print("✅ django_ckeditor_5 module imported successfully")
        
        # Test widget import
        from django_ckeditor_5.widgets import CKEditor5Widget
        print("✅ CKEditor5Widget imported successfully")
        
        # Test creating a widget instance
        widget = CKEditor5Widget()
        print("✅ CKEditor5Widget instance created successfully")
        
        print("\n🎉 All django-ckeditor-5 tests passed!")
        print("The 'ModuleNotFoundError: No module named 'django_ckeditor_5'' issue has been resolved!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_ckeditor_5()
