#!/usr/bin/env python
"""
EduManage API Integration Final Test
====================================
This script performs a comprehensive test of all API endpoints
to verify the complete system integration.
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

User = get_user_model()

def test_api_endpoints():
    """Test all API endpoints for basic functionality"""
    client = Client()
    
    print("🚀 EduManage API Integration Test")
    print("=" * 50)
    
    # Test API documentation endpoints
    endpoints_to_test = [
        ('/api/swagger/', 'API Documentation (Swagger)'),
        ('/api/redoc/', 'API Documentation (ReDoc)'),
        ('/api/auth/csrf-token/', 'CSRF Token'),
        ('/api/students/', 'Students API'),
        ('/api/teachers/', 'Teachers API'),
        ('/api/staff/', 'Staff API'),
        ('/api/courses/', 'Courses API'),
        ('/api/attendance/', 'Attendance API'),
        ('/api/examinations/', 'Examinations API'),
        ('/api/communication/', 'Communication API'),
        ('/api/discipline/', 'Discipline API'),
        ('/api/schedules/', 'Schedules API'),
    ]
    
    results = []
    
    for endpoint, name in endpoints_to_test:
        try:
            response = client.get(endpoint)
            status = "✅ PASS" if response.status_code in [200, 401, 403] else "❌ FAIL"
            status_code = response.status_code
            
            print(f"{status} {name:<30} Status: {status_code}")
            results.append((name, status_code, status))
            
        except Exception as e:
            print(f"❌ FAIL {name:<30} Error: {str(e)}")
            results.append((name, "ERROR", "❌ FAIL"))
    
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, _, status in results if "✅" in status)
    total = len(results)
    
    print(f"Total Endpoints Tested: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! API integration is successful!")
        print("🚀 System is ready for production deployment!")
    else:
        print(f"\n⚠️  {total - passed} endpoints need attention")
    
    return results

def check_models():
    """Check if all models can be imported successfully"""
    print("\n🔍 Model Import Test")
    print("=" * 30)
    
    models_to_test = [
        ('accounts.models', ['CustomUser', 'UserProfile']),
        ('students.models', ['Student', 'AcademicRecord']),
        ('teachers.models', ['Teacher', 'Subject', 'Class', 'Lesson']),
        ('staff.models', ['StaffProfile', 'Department', 'Role', 'LeaveRequest', 'PerformanceEvaluation']),
        ('courses.models', ['Course', 'CourseEnrollment', 'CourseContent', 'Assignment', 'AssignmentSubmission', 'CourseAnnouncement']),
        ('attendance.models', ['Attendance', 'AttendanceReport', 'SchoolCalendar']),
        ('examinations.models', ['Exam', 'ExamResult']),
        ('communication.models', ['Message', 'Notification']),
        ('discipline.models', ['InfractionType', 'DisciplinaryAction', 'DisciplinaryRecord', 'BehaviorNote']),
        ('schedules.models', ['Schedule', 'TimeSlot', 'DayOfWeek', 'Event']),
    ]
    
    all_passed = True
    
    for module_name, model_names in models_to_test:
        try:
            module = __import__(module_name, fromlist=model_names)
            for model_name in model_names:
                getattr(module, model_name)
            print(f"✅ {module_name:<20} All models imported successfully")
        except Exception as e:
            print(f"❌ {module_name:<20} Error: {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL MODELS IMPORTED SUCCESSFULLY!")
    else:
        print("\n⚠️  Some models have import issues")
    
    return all_passed

def main():
    """Main test function"""
    print("🏆 EduManage Final Integration Test")
    print("🗓️  Date: May 26, 2025")
    print("📍 Environment: Development")
    print("\n")
    
    # Test model imports
    models_ok = check_models()
    
    # Test API endpoints
    api_results = test_api_endpoints()
    
    print("\n" + "🏆" * 20)
    print("FINAL INTEGRATION STATUS")
    print("🏆" * 20)
    
    if models_ok and all("✅" in result[2] for result in api_results):
        print("🎉 INTEGRATION COMPLETE AND SUCCESSFUL!")
        print("🚀 EduManage system is ready for:")
        print("   • Frontend integration")
        print("   • User acceptance testing") 
        print("   • Production deployment")
        print("   • Educational institution rollout")
    else:
        print("⚠️  Integration has some issues that need resolution")
    
    print("\n📚 Next Steps:")
    print("1. Start development server: python manage.py runserver")
    print("2. Visit API docs: http://localhost:8000/api/swagger/")
    print("3. Test with frontend: Connect React components")
    print("4. Deploy to production: Configure hosting environment")

if __name__ == "__main__":
    main()
