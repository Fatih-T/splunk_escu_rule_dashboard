from django.urls import path
from . import views
urlpatterns = [
    path("board/", views.pipeline_board, name="pipeline_board"),
    path("transition/<str:type>/<int:pk>/", views.stage_transition, name="stage_transition"),
    path("convert/<int:escu_pk>/", views.convert_wizard, name="convert_wizard"),
]
