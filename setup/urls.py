from django.contrib import admin
from django.urls import path, include
from draw import urls as urls_draw
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls import url
from django.conf.urls.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('draw/', include(urls_draw)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^media/(.*)$', serve, {'document_root':settings.STATIC_ROOT}),
]