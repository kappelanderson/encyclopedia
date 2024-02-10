from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("edit/<str:name>", views.edit, name="edit"),

    path("random", views.random, name="random"),

    path("<str:name>", views.article, name="article"),

]
