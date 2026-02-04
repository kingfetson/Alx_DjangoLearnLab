from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


def home_view(request):
    return HttpResponse("LibraryProject is working!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
]
