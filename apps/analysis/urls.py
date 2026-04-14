from django.urls import path
from . import views
urlpatterns = [
    path("assignments/",                              views.assignment_list, name="assignment_list"),
    path("notes/<str:rule_type>/<int:rule_id>/",      views.note_list,       name="note_list"),
    path("notes/<str:rule_type>/<int:rule_id>/add/",  views.note_add,        name="note_add"),
    path("notes/<int:pk>/edit/",                      views.note_edit,       name="note_edit"),
    path("notes/<int:pk>/history/",                   views.note_history,    name="note_history"),
    path("comments/add/",                             views.comment_add,     name="comment_add"),
]
