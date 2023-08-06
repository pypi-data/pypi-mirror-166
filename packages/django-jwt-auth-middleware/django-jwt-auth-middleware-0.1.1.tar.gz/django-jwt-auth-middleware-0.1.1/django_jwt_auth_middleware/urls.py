from django.urls import path, include

from . import views


subpatterns = [
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
    path("refresh/", views.Refresh.as_view()),
]

urlpatterns = [path("jwt/", include(subpatterns))]
