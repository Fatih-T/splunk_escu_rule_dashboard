from django.urls import path
from . import views
urlpatterns = [
    path("", views.rule_list, name="escu_list"),
    path("<int:pk>/", views.rule_detail, name="escu_detail"),
    path("import/", views.import_csv, name="escu_import"),
    path("batches/", views.batch_list, name="escu_batches"),
    path("batches/<int:pk>/diff/", views.batch_diff, name="escu_diff"),
    path("similarity/", views.similarity_list, name="escu_similarity"),
    path("compute-similarity/", views.compute_similarity_view, name="compute_similarity"),
]
