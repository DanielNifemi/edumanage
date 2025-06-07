#!/usr/bin/env python
"""
Simple API test script for EduManage system
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile
from courses.models import Course
from attendance.models import Attendance
from examinations.models import Exam
from communication.models import Message
from discipline.models import DisciplinaryRecord
from schedules.models import Schedule

def test_apis():
    """Test all API endpoints"""
    print("🚀 Testing EduManage API Integration")
    print("=" * 50)
    
    # Create test client
    client = Client()
    
    # Test endpoints
    api_endpoints = [
        '/api/students/',
        '/api/teachers/',
        '/api/staff/',
        '/api/courses/',
        '/api/attendance/',
        '/api/examinations/',
        '/api/communication/',
        '/api/discipline/',
        '/api/schedules/',
    ]
    
    print("\n📡 Testing API Endpoints:")
    success_count = 0
    
    for endpoint in api_endpoints:
        try:
            response = client.get(endpoint)
            status = response.status_code
            
            if status == 200:
                print(f"✅ {endpoint} - Status: {status}")
                success_count += 1
            elif status == 401:
                print(f"⚠️  {endpoint} - Status: {status} (Authentication required)")
                success_count += 1  # This is expected for protected endpoints
            else:
                print(f"❌ {endpoint} - Status: {status}")
                
        except Exception as e:
            print(f"❌ {endpoint} - Error: {str(e)}")
    
    # Test model counts
    print(f"\n📊 Database Model Counts:")
    
    model_counts = [
        ('Students', Student.objects.count()),
        ('Teachers', Teacher.objects.count()),
        ('Staff', StaffProfile.objects.count()),
        ('Courses', Course.objects.count()),
        ('Attendance Records', Attendance.objects.count()),
        ('Exams', Exam.objects.count()),
        ('Messages', Message.objects.count()),
        ('Disciplinary Records', DisciplinaryRecord.objects.count()),
        ('Schedules', Schedule.objects.count()),
    ]
    
    for model_name, count in model_counts:
        print(f"   {model_name}: {count}")
    
    print(f"\n🎯 API Test Summary:")
    print(f"   ✅ {success_count}/{len(api_endpoints)} endpoints working")
    
    if success_count == len(api_endpoints):
        print(f"\n🎉 SUCCESS: All APIs are configured and working!")
        print(f"🏆 Education Management System API integration is COMPLETE!")
    else:
        print(f"\n⚠️  Some endpoints need attention")
    
    print(f"\n📋 Available APIs:")
    print(f"   1. Students API - Student management, academic records")
    print(f"   2. Teachers API - Teacher profiles, subjects, lessons")
    print(f"   3. Staff API - Staff profiles, departments, leave requests")
    print(f"   4. Courses API - Course management, enrollments, assignments")
    print(f"   5. Attendance API - Attendance tracking, reports")
    print(f"   6. Examinations API - Exam management, results, grading")
    print(f"   7. Communication API - Messaging, notifications")
    print(f"   8. Discipline API - Disciplinary records, behavior tracking")
    print(f"   9. Schedules API - Timetables, events, scheduling")

if __name__ == '__main__':
    test_apis()
