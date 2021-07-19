from django.db import IntegrityError
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .utility import *


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getProblems(request, format=None):
    if request.method == 'GET':
        problems = Problem.objects.all()
        serializer = ProblemSerializer(problems, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        slug = request.POST['problem_slug']
        problem = createProblem(slug)
        serializer = ProblemSerializer(problem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"blah": "blah"})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getProblem(request, slug, format=None):
    try:
        problem = Problem.objects.get(problem_slug=slug)
    except Problem.DoesNotExist:
        problem = createProblem(slug)
    serializer = ProblemSerializer(problem)
    print(serializer)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST', 'GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def setSolution(request, format=None):
    if request.method == 'POST':
        slug = request.data["problem"]["problem_slug"]
        try:
            problem = Problem.objects.get(problem_slug=slug)
        except Problem.DoesNotExist:
            problem = createProblem(slug)
        solution = Solution(problem=problem, user=request.user, solution=request.data["solution"])
        solution.save()
        solution = SolutionSerializer(solution)
        return Response(solution.data, status=status.HTTP_201_CREATED)
    else:
        solutions = Solution.objects.filter(user=request.user)
        solution = SolutionSerializer(solutions, many=True)
        return Response(solution.data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateSolution(request, format=None):
    slug = request.data["problem"]["problem_slug"]
    problem = Problem.objects.get(problem_slug=slug)
    solution = Solution.objects.get(user=request.user, problem=problem)
    solution.solution = request.data["solution"]
    solution.save()
    solution = SolutionSerializer(solution)
    return Response(solution.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getProblemsSorted(request, format=None):
    if request.method == 'POST':
        if request.POST['q'] == 'topic':
            result = getProblemsSortedByTopics()
            return Response(result, status=status.HTTP_200_OK)
        elif request.POST['q'] == 'difficulty':
            result = getProblemSortedbyDifficulty()
            return Response(result, status=status.HTTP_200_OK)
        else:
            Response({'error': 'wrong query'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        result = getProblemsSortedByTopics()
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
    user = UserSerializer(user)
    return Response(user.data, status.HTTP_201_CREATED)


@api_view(['POST', 'GET'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=request.data['password'])
        if user is None:
            return Response({'error': 'No user with that username'}, status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({'message': 'Login Successful'}, status.HTTP_200_OK)
    else:
        get_token(request)
        return Response()


@api_view(['GET'])
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    request.session.delete()
    return Response(status.HTTP_200_OK)
