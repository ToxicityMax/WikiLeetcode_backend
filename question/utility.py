import json

import requests

from .serializers import *

URL = "https://leetcode.com/graphql"

def createProblem(slug):
    import markdownify as md
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    title    titleSlug    content     difficulty    similarQuestions    exampleTestcases        topicTags {      name      slug   }    hints    sampleTestCase     }}"}
    headers = {
        "content-type": "application/json",
    }
    response = requests.request("GET", URL, json=payload, headers=headers)
    content = json.loads(response.content.decode("utf-8"))["data"]["question"]
    problem = Problem()
    problem.problem_name: str = content["title"]
    problem.problem_slug: str = content['titleSlug']
    problem.difficulty: str = content['difficulty']
    problem.topic: str = content['topicTags'][0]["name"]
    topicTags: list = content['topicTags']
    problem.related_topics: dict = {}
    for i in topicTags:
        problem.related_topics["name"] = i['name']
        problem.related_topics["slug"] = i['slug']
    html: str = content["content"]
    html = f"<h3>{content['title']}</h3>" + html
    problem.markdown: str = md.markdownify(html, heading_style="ATX")
    problem.save()
    return problem


def getProblemsSortedByTopics(user:User):
    topics = []
    problems = []
    result = []
    solution = Solution.objects.filter(user=user)
    for i in solution:
        problems.append(i.problem)
    for problem in problems:
        t = problem.topic
        if t not in topics:
            topics.append(problem.topic)
    for i in range(len(topics)):
        node = {'name': topics[i]}
        problem = Solution.objects.filter(user=user,problem__topic=topics[i])
        problems =[]
        for p in problem:
            problems.append(p.problem)
        problemS = ProblemShortSerializer(problems, many=True)
        node['children'] = problemS.data
        result.append(node)
    return result


def getProblemSortedbyDifficulty():
    difficulty: list = ['Easy', 'Medium', 'Hard']
    result = []
    for i in difficulty:
        problem = Problem.objects.filter(difficulty=i)
        if problem:
            node = {'name': i}
            problemS = ProblemShortSerializer(problem, many=True)
            node['children'] = problemS.data
            result.append(node)
    return result
