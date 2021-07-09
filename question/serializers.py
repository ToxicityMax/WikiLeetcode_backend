from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'problem_name', 'problem_slug', 'difficulty', 'topic', 'related_topics', 'markdown']


class SolutionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    user = UserSerializer()

    class Meta:
        model = Solution
        fields = ['id', 'user', 'problem', 'solution']
