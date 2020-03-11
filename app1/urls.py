from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.login),
    path("login_process", views.login_process),
    path("register_process", views.register_process),
    path("home", views.home),
    path("logout_process", views.logout_process),
    path("add_quote_process", views.add_quote_process),
    path("user/<int:id>/", views.user),
    path("edit/<int:id>/", views.edit),
    path("edit_process", views.edit_process),
    path("delete_process/<int:id>/", views.delete_process),
    path("process_like/<int:id>/", views.process_like),
]