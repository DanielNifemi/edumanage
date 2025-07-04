#!/usr/bin/env python3
"""
Script to create test assessments (exams and tests) for demonstration
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.utils import timezone
from examinations.models import Exam, Test, Question, Answer
from courses.models import Course
from teachers.models import Teacher
from accounts.models import CustomUser

def create_test_data():
    print("Creating test assessment data...")
    
    # Get or create a test teacher
    try:
        teacher_user = CustomUser.objects.filter(user_type='teacher').first()
        if not teacher_user:
            # Create a test teacher
            teacher_user = CustomUser.objects.create_user(
                username='testteacher',
                email='teacher@test.com',
                password='testpass123',
                first_name='Test',
                last_name='Teacher',
                user_type='teacher'
            )
        
        teacher = Teacher.objects.get_or_create(
            user=teacher_user,
            defaults={
                'employee_id': 'T001',
                'department': 'Computer Science'
            }
        )[0]
        print(f"Using teacher: {teacher}")
    except Exception as e:
        print(f"Error creating teacher: {e}")
        return
    
    # Get or create test courses
    courses_data = [
        {'title': 'Introduction to Programming', 'description': 'Basic programming concepts'},
        {'title': 'Database Systems', 'description': 'Database design and management'},
        {'title': 'Web Development', 'description': 'Frontend and backend web development'},
    ]
    
    courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults={
                'description': course_data['description'],
                'instructor': teacher,
                'status': 'published'
            }
        )
        courses.append(course)
        print(f"{'Created' if created else 'Found'} course: {course.title}")
    
    # Create test exams
    exam_data = [
        {
            'title': 'Programming Final Exam',
            'description': 'Comprehensive final exam covering all programming topics',
            'course': courses[0],
            'exam_date': (timezone.now() + timedelta(days=30)).date(),
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'duration': 180,
            'total_marks': 100,
            'passing_marks': 60,
            'is_published': True
        },
        {
            'title': 'Database Midterm',
            'description': 'Midterm exam on database design',
            'course': courses[1],
            'exam_date': (timezone.now() + timedelta(days=15)).date(),
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'duration': 120,
            'total_marks': 75,
            'passing_marks': 45,
            'is_published': False
        }
    ]
    
    for exam_info in exam_data:
        exam, created = Exam.objects.get_or_create(
            title=exam_info['title'],
            course=exam_info['course'],
            defaults={
                'description': exam_info['description'],
                'created_by': teacher,
                'date': exam_info['exam_date'],
                'start_time': exam_info['start_time'],
                'end_time': exam_info['end_time'],
                'duration_minutes': exam_info['duration'],
                'max_marks': Decimal(str(exam_info['total_marks'])),
                'passing_marks': Decimal(str(exam_info['passing_marks'])),
                'status': 'published' if exam_info['is_published'] else 'draft',
                'instructions': 'Please read all questions carefully before answering.'
            }
        )
        print(f"{'Created' if created else 'Found'} exam: {exam.title}")
    
    # Create test tests/quizzes
    test_data = [
        {
            'title': 'JavaScript Fundamentals Quiz',
            'description': 'Quick quiz on JavaScript basics',
            'course': courses[2],
            'duration': 30,
            'total_marks': 25,
            'passing_marks': 15,
            'max_attempts': 2,
            'is_published': True
        },
        {
            'title': 'SQL Practice Test',
            'description': 'Practice test for SQL queries',
            'course': courses[1],
            'duration': 45,
            'total_marks': 40,
            'passing_marks': 24,
            'max_attempts': 1,
            'is_published': True
        }
    ]
    
    for test_info in test_data:
        available_from = timezone.now()
        available_until = timezone.now() + timedelta(days=30)
        
        test, created = Test.objects.get_or_create(
            title=test_info['title'],
            course=test_info['course'],
            defaults={
                'description': test_info['description'],
                'created_by': teacher,
                'available_from': available_from,
                'available_until': available_until,
                'time_limit_minutes': test_info['duration'],
                'total_points': Decimal(str(test_info['total_marks'])),
                'passing_score': Decimal(str(test_info['passing_marks'])),
                'max_attempts': test_info['max_attempts'],
                'is_published': test_info['is_published']
            }
        )
        print(f"{'Created' if created else 'Found'} test: {test.title}")
        
        # Add some sample questions to the first test
        if created and test.title == 'JavaScript Fundamentals Quiz':
            questions_data = [
                {
                    'question_text': 'What is the correct way to declare a variable in JavaScript?',
                    'question_type': 'multiple_choice',
                    'points': 5,
                    'answers': [
                        ('var x = 5;', True),
                        ('variable x = 5;', False),
                        ('v x = 5;', False),
                        ('declare x = 5;', False)
                    ]
                },
                {
                    'question_text': 'JavaScript is a compiled language.',
                    'question_type': 'true_false',
                    'points': 5,
                    'answers': [
                        ('True', False),
                        ('False', True)
                    ]
                }
            ]
            
            for i, q_data in enumerate(questions_data):
                question = Question.objects.create(
                    test=test,
                    question_text=q_data['question_text'],
                    question_type=q_data['question_type'],
                    points=Decimal(str(q_data['points'])),
                    order=i + 1
                )
                
                for j, (answer_text, is_correct) in enumerate(q_data['answers']):
                    Answer.objects.create(
                        question=question,
                        answer_text=answer_text,
                        is_correct=is_correct,
                        order=j + 1
                    )
                
                print(f"  Created question: {question.question_text[:50]}...")
    
    print("\n✅ Test assessment data created successfully!")
    print("You can now test the frontend integration at http://localhost:3000")

if __name__ == '__main__':
    create_test_data()
