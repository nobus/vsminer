# -*- coding: utf-8 -*-

import json

from django.views import View
from django.http import JsonResponse

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from celery.task.control import inspect

from vs_app import tasks
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


class CeleryStatus(View):
    def get(self, request, *args, **kwargs):
        """
        {
            "active": {
                "celery@nobus": [
                    {
                        "id": "19ce8e20-0d6a-4892-8e81-a73bb473982a",
                        "name": "vs_app.tasks.sleep",
                        "args": "(120,)",
                        "kwargs": "{}",
                        "type": "vs_app.tasks.sleep",
                        "hostname": "celery@nobus",
                        "time_start": 1576218943.5906646,
                        "acknowledged": true,
                        "delivery_info": {
                            "exchange": "",
                            "routing_key": "celery",
                            "priority": 0,
                            "redelivered": false
                        }, "worker_pid": 17513
                    }
                ]},
            "sheduled": {"celery@nobus": []}}
        """
        resp = []

        i = inspect()
        active = i.active()

        if active:
            for task_list in active.values():
                for task in task_list:
                    resp.append({
                        'id': task['id'],
                        'name': task['name'],
                        'args': task.get('args', ''),
                        'kwargs': task.get('kwargs', ''),
                        })

        return JsonResponse({"resp": resp})

class PutAstrometryJob(View):
    def post(self, request, *args, **kwargs):
        data = request.read()
        params = json.loads(data.decode('ascii'))

        print(params)

        tasks.download_astrometry_data.delay(
            int(params['job_number']),
            params['status_url'],
        )

        return JsonResponse({'status': 'ok'})
