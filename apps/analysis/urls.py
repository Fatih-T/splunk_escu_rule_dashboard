from django.urls import path
from . import views
urlpatterns = [
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("notes/add/<str:rule_type>/<int:rule_id>/", views.note_add, name="note_add"),
]
