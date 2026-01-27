from django.contrib import admin
from django.urls import path, include

# api.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
