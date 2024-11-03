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
    path(
        "<int:project_id>/update_element/", views.update_element, name="update_element"
    ),
    path(
        "<int:project_id>/<int:element_id>/update_material/",
        views.update_material,
        name="update_material",
    ),
    path(
        "<int:project_id>/<int:element_id>/update_material_detail/<int:material_id>",
        views.update_material_detail,
        name="update_material_detail",
    ),
    path(
        "<int:project_id>/update_status_approved/",
        views.update_status_approved,
        name="update_status_approved",
    ),
    path(
        "<int:project_id>/update_status_declined/",
        views.update_status_declined,
        name="update_status_declined",
    ),
    path(
        "<int:project_id>/update_status_completed/",
        views.update_status_completed,
        name="update_status_completed",
    ),
]

urlpatterns += [
    path(
        "<int:element_id>/delete/", views.delete_project_element, name="delete_element"
    ),
    path(
        "<int:material_id>/delete/",
        views.delete_project_element_material,
        name="delete_material",
    ),
]
