from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InfractionTypeViewSet, DisciplinaryActionViewSet, 
    DisciplinaryRecordViewSet, BehaviorNoteViewSet
)

router = DefaultRouter()
router.register(r'infraction-types', InfractionTypeViewSet)
router.register(r'actions', DisciplinaryActionViewSet)
router.register(r'records', DisciplinaryRecordViewSet)
router.register(r'behavior-notes', BehaviorNoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
