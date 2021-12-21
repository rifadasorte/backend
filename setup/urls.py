from django.contrib import admin
from django.urls import path, include
from draw import urls as urls_draw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('draw/', include(urls_draw))
]
