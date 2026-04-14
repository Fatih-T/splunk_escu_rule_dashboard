from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/",      admin.site.urls),
    path("",            include("apps.dashboard.urls")),
    path("escu/",       include("apps.escu.urls")),
    path("cb/",         include("apps.carbonblack.urls")),
    path("pipeline/",   include("apps.pipeline.urls")),
    path("analysis/",   include("apps.analysis.urls")),
    path("config/",     include("apps.core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
