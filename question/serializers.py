from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProblemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='problem_name')

    class Meta:
        model = Problem
        fields = ['id', 'name', 'problem_slug', 'difficulty', 'topic', 'related_topics', 'markdown']


class ProblemShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='problem_name')

    class Meta:
        model = Problem
        fields = ['id', 'name', 'difficulty']


class SolutionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    #user = UserSerializer()

    class Meta:
        model = Solution
        fields = ['id', 'problem', 'language', 'solution']
