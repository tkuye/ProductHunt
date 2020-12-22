from django.contrib import admin
from django.urls import path
import accounts.settings as settings
from django.conf.urls.static import static
from django.urls.conf import include
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'), 
    path('signup', views.signup, name='signup'),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
