# -*- coding: utf-8 -*-

import re
import sys
import time
import json
import requests

from random import randint

from django.core.management.base import BaseCommand

from vs_app.models import CorrFits, SimbadData, AAVSOData


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-number', dest='job_number', type=int, help='job number')

    def _get_info_from_aavso(self, obj_name):
        time.sleep(randint(3, 9))

        aavso_format = obj_name.replace(' ', '+').lstrip('V*')

        print(f'Get AAVSO data for {aavso_format}', file=sys.stderr)

        resp = requests.get(f'https://www.aavso.org/vsx/index.php?ident={aavso_format}&view=api.object&format=json')

        """
            {"VSXObject": {
                "Name":"phi Per",
                "AUID":"000-BBD-264",
                "RA2000":"25.91517",
                "Declination2000":"50.68872",
                "ProperMotionRA":"24.5900",
                "ProperMotionDec":"-14.0100",
                "VariabilityType":"GCAS",
                "Period":"19.5",
                "MaxMag":"3.96 V",
                "MinMag":"4.11 V",
                "SpectralType":"B2Vne+B3Vne",
                "Category":"Variable",
                "OID":"26210",
                "Constellation":"Per"
                }
            }
        """

        aavso_data = json.loads(resp.text)
        aavso_data = aavso_data.get('VSXObject', {})
        print(aavso_data, file=sys.stderr)

        if aavso_data:
            aavso_data['RA2000'] = float(aavso_data['RA2000'])
            aavso_data['Declination2000'] = float(aavso_data['Declination2000'])
            aavso_data['ProperMotionRA'] = float(aavso_data['ProperMotionRA'])
            aavso_data['ProperMotionDec'] = float(aavso_data['ProperMotionDec'])

            if 'Period' in aavso_data:
                aavso_data['Period'] = float(re.sub('[^0-9]','', aavso_data['Period']))

            if 'Epoch' in aavso_data:
                aavso_data['Epoch'] = float(aavso_data['Epoch'])

        return aavso_data

    def handle(self, *args, **options):
        self.radius = 0.05
        self.job_number = options['job_number']

        for corr_obj in CorrFits.objects.filter(astro_job_id=self.job_number):
            if corr_obj.aavso_data:
                continue

            RA2000 = corr_obj.field_ra
            Declination2000 = corr_obj.field_dec

            found_obj = AAVSOData.objects.filter(
                RA2000__range=(RA2000 - self.radius, RA2000 + self.radius),
                Declination2000__range=(Declination2000 - self.radius, Declination2000 + self.radius),
            )

            if found_obj:
                if len(found_obj) > 1:
                    print(
                        f'Two or more object in AAVSOData for RA2000 = {RA2000} Declination2000 = {Declination2000} radius {self.radius}',
                        file=sys.stderr,
                        )
                else:
                    corr_obj.aavso_data(found_obj[0])
                    corr_obj.save()
            else:
                params = self._get_info_from_aavso(corr_obj.simbad_data.MAIN_ID)
                
                if params:
                    aavso_obj = AAVSOData(**params)
                    aavso_obj.save()

                    corr_obj.aavso_data = aavso_obj
                    corr_obj.save()