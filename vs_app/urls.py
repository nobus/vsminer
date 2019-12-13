# -*- coding: utf-8 -*-
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from vs_app.views import (
    AstroMetryJobViewSet, CorrFitsViewSet, CeleryStatus, PutAstrometryJob)

router = DefaultRouter()
router.register(r'jobs', AstroMetryJobViewSet)
router.register(r'star_data', CorrFitsViewSet)

urlpatterns = [
    path('put_astrojob/', PutAstrometryJob.as_view()),
    path('celery_status/', CeleryStatus.as_view()),

    path('', include(router.urls)),
]
