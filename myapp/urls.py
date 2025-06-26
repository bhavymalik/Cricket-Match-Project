from django.urls import path
from .views import indexLC, indexRU



urlpatterns = [
    path('live/', indexLC.as_view(), name='live-match'),
    path('live/<int:pk>/', indexRU.as_view(), name='live-match-update'),
]
