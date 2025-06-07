from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, CourseEnrollment, CourseContent, Assignment
from students.models import Student
from teachers.models import Teacher, Subject
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Test courses API functionality by creating sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-sample',
            action='store_true',
            help='Create sample course data for testing',
        )

    def handle(self, *args, **options):
        if options['create_sample']:
            self.create_sample_data()
        else:
            self.test_api_functionality()

    def create_sample_data(self):
        """Create sample data for testing"""
        self.stdout.write(self.style.SUCCESS('Creating sample course data...'))
        
        # Get or create a subject
        subject, created = Subject.objects.get_or_create(
            code='CS101',
            defaults={'name': 'Introduction to Computer Science'}
        )
        
        # Get or create a teacher
        teacher_user, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'teacher@example.com'
            }
        )
        
        teacher, created = Teacher.objects.get_or_create(
            user=teacher_user,
            defaults={
                'teacher_id': 'T2025001',
                'qualification': 'PhD Computer Science',
                'department': 'Computer Science'
            }
        )
        
        # Create a sample course
        course, created = Course.objects.get_or_create(
            title='Introduction to Programming',
            subject=subject,
            instructor=teacher,
            defaults={
                'description': 'Learn the fundamentals of programming with Python',
                'difficulty_level': 'beginner',
                'status': 'published',
                'start_date': date.today(),
                'end_date': date.today() + timedelta(days=90),
                'max_students': 30,
                'credits': 3
            }
        )
        
        # Create course content
        content_items = [
            {
                'title': 'Welcome to Programming',
                'content_type': 'lecture',
                'description': 'Introduction to the course and programming concepts',
                'order': 1
            },
            {
                'title': 'Python Basics',
                'content_type': 'video',
                'description': 'Learn Python syntax and basic operations',
                'order': 2
            },
            {
                'title': 'First Programming Assignment',
                'content_type': 'assignment',
                'description': 'Write your first Python program',
                'order': 3
            }
        ]
        
        for item_data in content_items:
            content, created = CourseContent.objects.get_or_create(
                course=course,
                title=item_data['title'],
                defaults=item_data
            )
            
            # Create assignment if content type is assignment
            if item_data['content_type'] == 'assignment' and created:
                Assignment.objects.create(
                    content=content,
                    due_date=date.today() + timedelta(days=7),
                    total_points=100,
                    submission_type='text',
                    instructions='Write a Python program that prints "Hello, World!"'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created course: {course.title} with {course.contents.count()} content items'
            )
        )

    def test_api_functionality(self):
        """Test basic API functionality"""
        self.stdout.write(self.style.SUCCESS('Testing courses API functionality...'))
        
        # Test course creation and retrieval
        courses = Course.objects.all()
        self.stdout.write(f'Total courses: {courses.count()}')
        
        for course in courses[:5]:  # Show first 5 courses
            self.stdout.write(f'  - {course.title} ({course.subject.code})')
            self.stdout.write(f'    Instructor: {course.instructor.user.get_full_name()}')
            self.stdout.write(f'    Status: {course.status}')
            self.stdout.write(f'    Enrollments: {course.enrollment_count}')
            self.stdout.write(f'    Content items: {course.contents.count()}')
            
            # Test assignments
            assignments = Assignment.objects.filter(content__course=course)
            if assignments.exists():
                self.stdout.write(f'    Assignments: {assignments.count()}')
                for assignment in assignments:
                    submissions = assignment.submissions.count()
                    self.stdout.write(f'      - {assignment.content.title}: {submissions} submissions')
        
        # Test enrollment functionality
        enrollments = CourseEnrollment.objects.filter(is_active=True)
        self.stdout.write(f'Active enrollments: {enrollments.count()}')
        
        self.stdout.write(self.style.SUCCESS('API functionality test completed!'))
