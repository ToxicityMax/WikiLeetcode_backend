from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utility import *

'''
{
    "problem": {
        "id": "id",
        "problem_slug": "slug",
        "problem_name": "name"
    },
    "solution": "solution",
    "language": "language",
}
'''


@api_view(['GET', 'POST'])
def getProblems(request, format=None):
    if request.method == 'GET':
        problems = Problem.objects.all()
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)
        slug = request.POST['problem_slug']
        problem = createProblem(slug)
        serializer = ProblemSerializer(problem)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"blah": "blah"})


@api_view(['GET'])
def getProblem(request, slug, format=None):
    try:
        problem = Problem.objects.get(problem_slug=slug)
    except Problem.DoesNotExist:
        problem = createProblem(slug)
    serializer = ProblemSerializer(problem)
    print(serializer)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def setSolution(request, format=None):
    slug = request.data["problem"]["problem_slug"]
    try:
        problem = Problem.objects.get(problem_slug=slug)
    except Problem.DoesNotExist:
        problem = createProblem(slug)
    solution = Solution(problem=problem, user=request.user, solution=request.data["solution"])
    solution.save()
    solution = SolutionSerializer(solution)
    return Response(solution.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def updateSolution(request, format=None):
    slug = request.data["problem"]["problem_slug"]
    problem = Problem.objects.get(problem_slug=slug)
    solution = Solution.objects.get(user=request.user, problem=problem)
    solution.solution = request.data["solution"]
    solution.save()
    solution = SolutionSerializer(solution)
    return Response(solution.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getProblemsSortedTopics(request, format=None):
    result = getProblemsSortedByTopics()
    return Response(result)


@api_view(['GET'])
def getProblemsSortedDifficulty(request, format=None):
    result = getProblemSortedbyDifficulty()
    return Response(result)


@api_view(['GET', 'POST'])
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
