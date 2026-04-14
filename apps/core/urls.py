from django.urls import path
from . import views
urlpatterns = [
    path("", views.config_list, name="config_list"),
    path("<int:pk>/edit/", views.config_edit, name="config_edit"),
    path("audit-logs/", views.audit_log_list, name="audit_log_list"),
]
