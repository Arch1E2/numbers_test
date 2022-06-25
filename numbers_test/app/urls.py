from django.urls import path, include
# from rest_framework import routers
from .viewsets import *
from .views import *

# router = routers.DefaultRouter()
# router.register('inspectorshares', InspectorShareViewSet, basename='inspectorshares')

urlpatterns = [
    # path(r'^', include(router.urls)),
    path('orders/', orders),
]