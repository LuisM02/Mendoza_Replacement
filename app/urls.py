from . import views
from django.urls import path

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("approved/", views.project_list_approved, name="project_list_approved"),
    path("declined/", views.project_list_declined, name="project_list_declined"),
    path("completed", views.project_list_completed, name="project_list_completed"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("request_quote/", views.request_quote, name="request_quote"),
    path("<int:project_id>/", views.project_detail, name="project_detail"),
]
