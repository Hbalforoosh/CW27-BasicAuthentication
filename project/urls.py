from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tasks', TaskViewSet, basename='tasks')
urlpatterns = router.urls + [
    path('api/token/', obtain_auth_token),
]
