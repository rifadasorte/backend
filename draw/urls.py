from django.urls import path
from .views import GetNumbers
urlpatterns = [
    path('numbers/<int:pk>', GetNumbers.as_view())
]
