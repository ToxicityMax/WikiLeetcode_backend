from django.urls import path

from .views import *

urlpatterns = [
    path('problem', getProblems),
    path('problem/sorted', getProblemsSorted),
    path('problem/<slug:slug>', getProblem),
    path('solution/', setSolution),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
]
