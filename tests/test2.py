import requests
import json


def getSetCookieValue(response, key):
    cookies = response.headers['set-cookie']
    if cookies is None:
        return None

    for i in range(0, len(cookies)):
        sections = cookies[i].split(';')
        for j in range(0, len(sections)):
            kv = sections[j].trim().split('')
            if(kv[0] == key):
                return kv[1]
    return None


user = {
    'login': 'LazyBoi',
    'password': 'h59sBmrDKd8Tuq',
    'loginCSRF': None,
    'sessionCSRF': None,
    'sessionId':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiIybGxieCIsIl9hdXRoX3VzZXJfaWQiOiI0MzY2NjUzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkZTZkNmE3NzEwNDI1ODg1YTYyYjhlYmE1OGI1ODQwMjE1OWEyMzU0IiwiaWQiOjQzNjY2NTMsImVtYWlsIjoia3NpbmdoMjAwMS5kZXZAZ21haWwuY29tIiwidXNlcm5hbWUiOiJMYXp5Qm9pIiwidXNlcl9zbHVnIjoiTGF6eUJvaSIsImF2YXRhciI6Imh0dHBzOi8vd3d3LmdyYXZhdGFyLmNvbS9hdmF0YXIvYzU4ZjYyYTI0MjM4YzhmZjcyMmU3M2I0NjdmZjZhM2MucG5nP3M9MjAwIiwicmVmcmVzaGVkX2F0IjoxNjI1NjY3NDI0LCJpcCI6IjIwNS4yNTQuMTY3LjUwIiwiaWRlbnRpdHkiOiJjMDNmN2MyMjNmNjRiODM5NTIzZWU2ZGU1OWQ3NDgxZCIsInNlc3Npb25faWQiOjk4ODQzMjEsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.PgZuLMNyghyhDH2Zy_K4BEXCbPekgNf83JLMTlsHo4Y',

}
url = 'https://leetcode.com/accounts/login/'


def checkError(error, response, expectedStatus):
    if error is None and response and response.status != expectedStatus:
        code = resp.statusCode
        if code == 403 or code == 401:
            pass
            # error = (session.error.expired message)
        else:
            error = {
                'msg': 'http error',
                'statusCode': code
            }
    return error


client = requests.session()
client.get(url)
if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']
user['loginCSRF'] = csrftoken

headers = {
    'Origin': 'https://leetcode.com',
    'Referer': url,
    'Cookie': 'csrftoken=' + user['loginCSRF'] + ';'
}

form = {
    'csrfmiddlewaretoken': user['loginCSRF'],
    'login': user['login'],
    'password': user['password']
}

response = client.post(url, headers=headers, data=form)
print(response.content.decode('utf-8'))


# response = requests.get(url)
# print(response.cookies.extract_cookies.)

# plugin.signin = function (user, cb) {
#     log.debug('running leetcode.signin');
#     const spin = h.spin('Signing in leetcode.com');
#     request(config.sys.urls.login, function (e, resp, body) {
#         spin.stop();
#         e = plugin.checkError(e, resp, 200);
#         if (e) return cb(e);

#         user.loginCSRF = h.getSetCookieValue(resp, 'csrftoken');
#         const opts = {
#             url: config.sys.urls.login,
#             headers: {
#                 Origin: config.sys.urls.base,
#                 Referer: config.sys.urls.login,
#                 Cookie: 'csrftoken=' + user.loginCSRF + ';'
#             },
#             form: {
#                 csrfmiddlewaretoken: user.loginCSRF,
#                 login: user.login,
#                 password: user.pass
#             }
#         };
#         request.post(opts, function (e, resp, body) {
#             if (e) return cb(e);
#             if (resp.statusCode !== 302) return cb('invalid password?');
#             user.sessionCSRF = h.getSetCookieValue(resp, 'csrftoken');
#             user.sessionId = h.getSetCookieValue(resp, 'LEETCODE_SESSION');
#             session.saveUser(user);
#             return cb(None, user);
#         });
#     });
# };
