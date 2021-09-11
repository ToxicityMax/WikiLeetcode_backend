from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .utility import *


@api_view(['GET', 'POST'])
@authentication_classes([BearerAuthentication])
@permission_classes([IsAuthenticated])
def getProblems(request, format=None):
    if request.method == 'GET':
        problems = []
        user = User.objects.get(username=request.user)
        solution = Solution.objects.filter(user=user)
        for sol in solution:
            print(sol.problem)
            problems.append(sol.problem)
        serializer = ProblemSerializer(problems, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        slug = request.POST['problem_slug']
        problem = createProblem(slug)
        serializer = ProblemSerializer(problem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET'])
# @authentication_classes([BearerAuthentication])
# @permission_classes([IsAuthenticated])
# def getProblem(request, slug, format=None):
#     try:
#         problem = Problem.objects.get(problem_slug=slug)
#     except Problem.DoesNotExist:
#         problem = createProblem(slug)
#     serializer = ProblemSerializer(problem)
#     print(serializer)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST', 'GET'])
@authentication_classes([BearerAuthentication])
@permission_classes([IsAuthenticated])
def solution(request, format=None):
    if request.method == 'POST':
        slug = request.data["problem_slug"]
        try:
            problem = Problem.objects.get(problem_slug=slug)
        except Problem.DoesNotExist:
            problem = createProblem(slug)
        user = User.objects.get(username=request.user)
        try:
             solution = Solution.objects.get(user=user,problem=problem)
             solution.language = request.data["language"]
             solution.solution = request.data["solution"]
        except:
            solution = Solution(problem=problem, user=user, solution=request.data["solution"],
                                language=request.data["language"])
        solution.save()
        print(str(request.user) + ' question ' + str(slug) + ' solution ' + solution.language)
        solution = SolutionSerializer(solution)
        print(solution.data)
        return Response(solution.data, status=status.HTTP_201_CREATED)
    else:
        user = User.objects.get(username=request.user)
        solutions = Solution.objects.filter(user=user)
        solution = SolutionSerializer(solutions, many=True)
        return Response(solution.data)


@api_view(['PUT'])
@authentication_classes([BearerAuthentication])
@permission_classes([IsAuthenticated])
def updateSolution(request, format=None):
    slug = request.data["problem_slug"]
    solution = Solution.objects.get(user=request.user, problem__problem_slug=slug)
    solution.solution = request.data["solution"]
    solution.save()
    solution = SolutionSerializer(solution)
    return Response(solution.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([BearerAuthentication])
@permission_classes([IsAuthenticated])
def getProblemsSorted(request, format=None):
    if request.method == 'POST':
        if request.POST['q'] == 'topic':
            result = getProblemsSortedByTopics(request.user)
            return Response(result, status=status.HTTP_200_OK)
        elif request.POST['q'] == 'difficulty':
            result = getProblemSortedbyDifficulty(request.user)
            return Response(result, status=status.HTTP_200_OK)
        else:
            Response({'error': 'wrong query'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        result = getProblemsSortedByTopics(request.user)
        return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    username = request.data['username']
    try:
        user = User.objects.create(username=username)
        user.set_password(request.data['password'])
        user.save()
    except IntegrityError:
        return Response({'error': 'Username already exists'}, status.HTTP_400_BAD_REQUEST)
    return Response({
        'message': 'Account Created successfully',
    }, status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data['username']
    from django.contrib.auth import authenticate,login
    user = authenticate(request, username=username, password=request.data['password'])
    if user is None:
        return Response({'error': 'Invalid username'}, status.HTTP_400_BAD_REQUEST)
    token,created = Token.objects.get_or_create(user=user)
    print(request)
    login(request, user)
    return Response({
        'token': token.key,
    }, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BearerAuthentication])
@permission_classes([IsAuthenticated])
def userdata(request):
    user = User.objects.get(username=request.user)
    print(user)
    return Response({'user_id': user.pk,
                     'username': user.username})


@api_view(['GET'])
def logout(request):
    from django.contrib.auth import logout
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')
