from django.urls import path
from . import views
urlpatterns = [
    path("",                 views.rule_list,   name="cb_list"),
    path("<int:pk>/",        views.rule_detail, name="cb_detail"),
    path("create/",          views.rule_create, name="cb_create"),
    path("<int:pk>/edit/",   views.rule_edit,   name="cb_edit"),
    path("<int:pk>/delete/", views.rule_delete, name="cb_delete"),
]
