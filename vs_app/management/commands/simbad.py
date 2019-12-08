# -*- coding: utf-8 -*-

import sys
import time

from random import randint

import astropy.coordinates as coord
import astropy.units as u
from astroquery.simbad import Simbad

from django.core.management.base import BaseCommand

from vs_app.models import AstroMetryJob, CorrFits, SimbadData


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-number', dest='job_number', type=int, help='job number')

    def _get_info_from_simbad(self, ra, dec):
        """
        MAIN_ID        RA           DEC      RA_PREC DEC_PREC COO_ERR_MAJA COO_ERR_MINA COO_ERR_ANGLE COO_QUAL COO_WAVELENGTH     COO_BIBCODE    
             "h:m:s"       "d:m:s"                         mas          mas           deg                                                 
        --------- ------------- ------------- ------- -------- ------------ ------------ ------------- -------- -------------- -------------------
        * phi Per 01 43 39.6379 +50 41 19.432      11       11        0.110        0.120            90        A              O 2007A&A...474..653V
        """
        def _coord_convert(ra_hms, dec_dms):
            # '01 43 39.6379', '+50 41 19.432' => 25.915157916666665, 50.68873111111111
            c = coord.SkyCoord(ra_hms, dec_dms, unit=(u.hourangle, u.deg))
            return c.ra.value, c.dec.value

        ret = {}

        while True:
            time.sleep(randint(3, 9))

            try:
                result_table = Simbad.query_region(
                    coord.SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg)),
                    radius=self.radius*u.deg)

                data = result_table[0]

                ret['MAIN_ID'] = data[0].decode('ascii')
                ret['RA'], ret['DEC'] = _coord_convert(data[1], data[2])
                ret['RA_PREC'] = data[3]
                ret['DEC_PREC'] = data[4]
                ret['COO_ERR_MAJA'] = data[5]
                ret['COO_ERR_MINA'] = data[6]
                ret['COO_ERR_ANGLE'] = data[7]
                ret['COO_QUAL'] = data[8]
                ret['COO_WAVELENGTH'] = data[9]
                ret['COO_BIBCODE'] = data[10]

                return ret
            except Exception as ex:
                print('Simbad: ', ex, file=sys.stderr)

        return None

    def handle(self, *args, **options):
        self.radius = 0.05
        self.job_number = options['job_number']

        for corr_obj in CorrFits.objects.filter(astro_job_id=self.job_number):
            if corr_obj.simbad_data:
                continue
    
            RA = corr_obj.field_ra
            DEC = corr_obj.field_dec

            found_obj = SimbadData.objects.filter(
                RA__range=(RA - self.radius, RA + self.radius),
                DEC__range=(DEC - self.radius, DEC + self.radius),
            )

            if found_obj:
                if len(found_obj) > 1:
                    print(
                        f'Two or more object in SimbadData for RA = {RA} DEC = {DEC} radius {self.radius}',
                        file=sys.stderr,
                        )
                else:
                    corr_obj.simbad_data(found_obj[0])
                    corr_obj.save()
            else:
                sim_obj = SimbadData(**self._get_info_from_simbad(RA, DEC))

                if sim_obj:
                    sim_obj.save()

                    corr_obj.simbad_data = sim_obj
                    corr_obj.save()
