from django.urls import path
from . import views

urlpatterns = [
    path('v1/health', views.health,name="health"),
    path('v1/authenticate',views.authenticate,name='authenticate'),
    path('v1/upload', views.file_upload,name="file-upload")
]
