# -*- coding: utf-8 -*-

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from vs_app.models import AstroMetryJob, CorrFits
from vs_app.serializers import AstroMetryJobSerializer, CorrFitsSerializer


class AstroMetryJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AstroMetryJob.objects.all()
    serializer_class = AstroMetryJobSerializer

class CorrFitsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CorrFits.objects.all()
    serializer_class = CorrFitsSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('astro_job',)
