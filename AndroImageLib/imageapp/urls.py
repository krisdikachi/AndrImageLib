from django.urls import path
from . import views
from .views import trigger_download, download_image

urlpatterns = [
    path("", views.app, name="app"),
    path("download/<str:image_id>/", views.trigger_download, name="trigger_download"),
    path('download-image/', download_image, name='download_image'),


]


