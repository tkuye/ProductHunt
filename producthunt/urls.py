
from django.contrib import admin
from django.urls import path
from products import views 
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls'))
]
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



