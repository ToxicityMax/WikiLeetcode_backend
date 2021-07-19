from django.contrib.auth.models import User
from django.db import models

difficulty = [
    ('E', 'easy'),
    ('M', 'medium'),
    ('H', 'hard'),
]

lang = ['C++', 'Java', 'Python', 'Python3', 'C', 'C#', 'JavaScript', 'Ruby', 'Swift', 'Go', 'Scala', 'Kotlin', 'Rust',
        'PHP', 'TypeScript', 'Racket']
langSlug = ['cpp', 'java', 'python', 'python3', 'c', 'csharp', 'javascript', 'ruby', 'swift', 'golang', 'scala',
            'kotlin', 'rust', 'php', 'typescript', 'racket']


class Problem(models.Model):
    problem_name = models.CharField(max_length=64, null=True, blank=True, unique=True)
    problem_slug = models.SlugField(max_length=64, null=True, blank=True, unique=True)
    difficulty = models.CharField(max_length=4, choices=difficulty, default='NULL')
    topic = models.CharField(max_length=24, null=True, blank=True)
    related_topics = models.JSONField(null=True, blank=True)
    markdown = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.problem_name


# class LCAuth(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     lc_user = models.CharField(max_length=64)
#     lc_pass = models.CharField(max_length=64)
#
#     def __str__(self):
#         return self.user.name + " Lc username: " + self.lc_user


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # LCuser = models.ForeignKey(LCAuth, on_delete=models.CASCADE, blank=True, null=True)
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, default="")
    solution = models.TextField()
    language = models.CharField(max_length=12, null=True, blank=False)

    def __str__(self):
        return self.user.username + " Q: " + self.problem.problem_name


class ProblemFile(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    markdownFile = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.markdownFile.name
