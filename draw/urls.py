from django.urls import path
from .views import (
    Authentication, 
    GetDraws, 
    GetNumbers,
    SetRequest)
urlpatterns = [
    path('', GetDraws.as_view()),
    path('numbers/<int:pk>', GetNumbers.as_view()),
    path('auth/', Authentication.as_view()),
    path('request/', SetRequest.as_view())
]
