from django.contrib import admin
from django.urls import path
from rareapi.views import login_user, register_user
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),


]
