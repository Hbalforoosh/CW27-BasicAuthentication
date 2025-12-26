from django.shortcuts import render
from .serializer import AddMemberSerializer, ProjectSerializer, TaskSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .models import Project, Task, User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# from rest_framework import filters
# Create your views here.


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['name', 'title']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Project.objects.all()
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(
                description__icontains=search))
        owner = self.request.query_params.get("owner")
        if owner:
            queryset = queryset.filter(owner_id=owner)
        return queryset

    @action(detail=True, methods=['get', 'post'], serializer_class=AddMemberSerializer)
    def add_member(self, request, pk=None):
        project = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        user = get_object_or_404(User, id=user_id)
        project.members.add(user)
        return Response({'detail': 'member added'})


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)

    def get_queryset(self):
        queryset = Task.objects.all()
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(
                description__icontains=search))

        status = self.request.query_params.get("status")

        if status:
            queryset = queryset.filter(status=status)
        return queryset
