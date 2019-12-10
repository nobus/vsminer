# -*- coding: utf-8 -*-
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from vs_app.views import AstroMetryJobViewSet, CorrFitsViewSet

router = DefaultRouter()
router.register(r'jobs', AstroMetryJobViewSet)
router.register(r'star_data', CorrFitsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
