from django.urls import path
from rest_framework.authtoken import views 
from .views import *

urlpatterns = [
    path('problem', getProblems),
    path('problem/sorted', getProblemsSorted),
    path('problem/<slug:slug>', getProblem),
    path('solution/', setSolution),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('api-token-auth/',views.obtain_auth_token)
]
