from rest_framework import serializers
from .models import User, Project, Task


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description',
                  'owner', 'members', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
