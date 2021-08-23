import requests
import json
import markdownify as md

url = "https://leetcode.com/graphql"
#options for OperationName = ["globalData","questionData","Submissions","allQuestionsStatusesRaw","filterableCategories","allFavorites","questionTags","achievement","debuggerLanguageFeatures","questionTopicCount","interviewOptions",""]
# https://leetcode.com/api/problems/all/

payload = {
    "operationName": "questionData",
    "variables": {"titleSlug": "two-sum"},
    "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    title    titleSlug    content     difficulty    similarQuestions    exampleTestcases        topicTags {      name      slug   }    hints    sampleTestCase     }}"} 

headers = {
    "content-type": "application/json",
}

response = requests.request("GET", url, json=payload, headers=headers)
content = json.loads(response.content.decode("utf-8"))
title:str = content["data"]["question"]["title"]
# html: str = content["data"]["question"]["content"]
# body = f"<h3>{title}</h3>" + html
# markdown:str = md.markdownify(body, heading_style="ATX")
#print(markdown)
topicTags = content["data"]["question"]["topicTags"]
dictionary= {}
for name in topicTags:
    dictionary["name"] = name['name']
    dictionary["slug"] = name['slug']
print(type(dictionary))


# payload = {
#     "operationName": "Submissions",
#     "variables": {"titleSlug": "plus-one"},
#     "query":"query Submissions($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!) {  submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug) {    lastKey    hasNext    submissions {      id      statusDisplay      lang      runtime      timestamp      url      isPending      memory      __typename    }    __typename  }}"}

# headers = {
#     "cookie": "csrftoken=PvUkMvrXcDfxFUT8p8QyHxd1Yp75mMbSODliJaPasfo66uiK544LjYySGu6KtYGb",
#     "content-type": "application/json",
#     "Origin": "https://leetcode.com",
# }

# response:requests.models.Response = requests.request("POST", url, json=payload, headers=headers)
# print(json.loads(response.content.d   ecode("utf-8")))
