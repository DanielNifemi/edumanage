from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamViewSet, ExamResultViewSet, TestViewSet, 
    QuestionViewSet, AnswerViewSet, TestAttemptViewSet
)

router = DefaultRouter()
router.register(r'exams', ExamViewSet)
router.register(r'exam-results', ExamResultViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'test-attempts', TestAttemptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
