from django.db import models


class AstroMetryJob(models.Model):
    # http://astrometry.net/doc/net/api.html#getting-job-results

    job_number = models.PositiveIntegerField(primary_key=True)
    url = models.URLField()
    orientation = models.FloatField(null=True, blank=True, default=None)
    pixscale = models.FloatField(null=True, blank=True, default=None)
    radius = models.FloatField(null=True, blank=True, default=None)
    center_ra = models.FloatField()
    center_dec = models.FloatField()

    class Meta:
        index_together = (('center_ra', 'center_dec'),)

class NewFits(models.Model):
    astro_job = models.ForeignKey('AstroMetryJob', on_delete=models.CASCADE)

    naxis = models.IntegerField(null=True, blank=True, default=None)
    naxis1 = models.IntegerField(null=True, blank=True, default=None)
    naxis2 = models.IntegerField(null=True, blank=True, default=None)
    date_obs = models.DateField()
    ut_start = models.TimeField() # UTC +0
    exptime = models.FloatField(null=True, blank=True, default=None)
    ref_point_ra = models.FloatField()
    ref_point_dec = models.FloatField()
    ref_point_x = models.FloatField(null=True, blank=True, default=None)
    ref_point_y = models.FloatField(null=True, blank=True, default=None)
    tranform_matrix = models.FloatField(null=True, blank=True, default=None)
    scale = models.FloatField(null=True, blank=True, default=None) # arcsec/pix

    class Meta:
        index_together = (('ref_point_ra', 'ref_point_dec'),)

class CorrFits(models.Model):
    astro_job = models.ForeignKey('AstroMetryJob', on_delete=models.CASCADE)

    simbad_data = models.ForeignKey('SimbadData', on_delete=models.CASCADE, blank=True, null=True)
    aavso_data = models.ForeignKey('AAVSOdata', on_delete=models.CASCADE, blank=True, null=True)

    field_x = models.FloatField(null=True, blank=True, default=None)
    field_y = models.FloatField(null=True, blank=True, default=None)
    field_ra = models.FloatField()
    field_dec = models.FloatField()

    index_x = models.FloatField(null=True, blank=True, default=None)
    index_y = models.FloatField(null=True, blank=True, default=None)
    index_ra = models.FloatField(null=True, blank=True, default=None)
    index_dec = models.FloatField(null=True, blank=True, default=None)

    index_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    field_id = models.PositiveIntegerField(null=True, blank=True, default=None)

    match_weight = models.FloatField(null=True, blank=True, default=None)
    FLUX = models.FloatField(null=True, blank=True, default=None)
    BACKGROUND = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        index_together = (('field_ra', 'field_dec'),)

class SimbadData(models.Model):
    """
    >>> import astropy.coordinates as coord
    >>> import astropy.units as u
    >>> from astroquery.simbad import Simbad
    >>> ra = 25.9144
    >>> dec = 50.6871
    >>> result_table = Simbad.query_region(coord.SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg)),radius=0.05 * u.deg)
    >>> result_table
    <Table masked=True length=1>
    MAIN_ID        RA           DEC      RA_PREC DEC_PREC COO_ERR_MAJA COO_ERR_MINA COO_ERR_ANGLE COO_QUAL COO_WAVELENGTH     COO_BIBCODE
                "h:m:s"       "d:m:s"                         mas          mas           deg
    object      str13         str13      int16   int16     float32      float32        int16       str1        str1             object
    --------- ------------- ------------- ------- -------- ------------ ------------ ------------- -------- -------------- -------------------
    * phi Per 01 43 39.6379 +50 41 19.432      11       11        0.110        0.120            90        A              O 2007A&A...474..653V
    """

    MAIN_ID = models.CharField(max_length=33, null=True, blank=True, default=None)
    RA = models.FloatField()
    DEC = models.FloatField()
    RA_PREC = models.IntegerField(null=True, blank=True, default=None)
    DEC_PREC = models.IntegerField(null=True, blank=True, default=None)
    COO_ERR_MAJA = models.FloatField(null=True, blank=True, default=None)
    COO_ERR_MINA = models.FloatField(null=True, blank=True, default=None)
    COO_ERR_ANGLE = models.FloatField(null=True, blank=True, default=None)
    COO_QUAL = models.CharField(max_length=3, null=True, blank=True, default=None)
    COO_WAVELENGTH = models.CharField(max_length=3, null=True, blank=True, default=None)
    COO_BIBCODE = models.BinaryField(max_length=21, null=True, blank=True, default=None)

    class Meta:
        index_together = (('RA', 'DEC'),)

class AAVSOData(models.Model):
    """
        https://www.aavso.org/comment/62475#comment-62475

        {"VSXObject":
            {
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

        https://www.aavso.org/vsx/index.php?ident=1SWASP+J022916.91-395901.4&view=api.object&format=json
        {"VSXObject":
            {
                "Name":"1SWASP J022916.91-395901.4",
                "AUID":"000-BLF-895",
                "RA2000":"37.32058",
                "Declination2000":"-39.98378",
                "ProperMotionRA":"40.5000",
                "ProperMotionDec":"4.9000",
                "VariabilityType":"NL\/VY",
                "Period":"0.137206",
                "Epoch":"2454416.48",
                "MaxMag":"12.8 V",
                "MinMag":"16.7: V",
                "Discoverer":"Gregor Srdoc, Klaus Bernhard, Stefan H\u00fcmmerich",
                "Category":"Variable",
                "OID":"358947",
                "Constellation":"Eri"
            }
        }
    """

    Name = models.CharField(max_length=33, null=True, blank=True, default=None)
    AUID = models.CharField(max_length=33, null=True, blank=True, default=None)
    RA2000 = models.FloatField()
    Declination2000 = models.FloatField()
    ProperMotionRA = models.FloatField(null=True, blank=True, default=None)
    ProperMotionDec = models.FloatField(null=True, blank=True, default=None)
    VariabilityType = models.CharField(max_length=13, null=True, blank=True, default=None)
    Period = models.FloatField(null=True, blank=True, default=None)
    Epoch = models.FloatField(null=True, blank=True, default=None)
    MaxMag = models.CharField(max_length=9, null=True, blank=True, default=None)
    MinMag = models.CharField(max_length=9, null=True, blank=True, default=None)
    Discoverer = models.CharField(max_length=256, null=True, blank=True, default=None)
    SpectralType = models.CharField(max_length=33, null=True, blank=True, default=None)
    Category = models.CharField(max_length=15, null=True, blank=True, default=None)
    OID = models.CharField(max_length=15, null=True, blank=True, default=None)
    Constellation = models.CharField(max_length=9, null=True, blank=True, default=None)

    # perhaps need TTL in future?
    class Meta:
        index_together = (('RA2000', 'Declination2000'),)
