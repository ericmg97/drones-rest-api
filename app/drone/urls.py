"""
URL mappings for the drone app.
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from drone import views


router = DefaultRouter()
router.register('drones', views.DroneViewSet)

app_name = 'drone'

urlpatterns = [
    path('', include(router.urls)),
]
