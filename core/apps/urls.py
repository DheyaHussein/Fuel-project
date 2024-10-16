from django.urls import path, include
from . import views


urlpatterns = [
    # path("store/", include('apps.storehouse.urls')),
    path("", include("apps.api.urls")),
]
