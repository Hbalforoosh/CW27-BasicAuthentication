from os import name
from turtle import title
from django.shortcuts import render
from .serializer import ProjectSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .models import Project, Task
from django.db.models import Q

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

        return queryset


class TaskViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
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
