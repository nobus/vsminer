# -*- coding: utf-8 -*-

from rest_framework import serializers

from vs_app.models import AstroMetryJob, CorrFits, AAVSOData, SimbadData


class AstroMetryJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstroMetryJob
        fields = '__all__'

class AAVSODataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AAVSOData
        fields = ['Name', 'AUID', 'VariabilityType', 'Period', 'MaxMag', 'MinMag', 'Category']

class SimbadDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimbadData
        fields = ['MAIN_ID']

class CorrFitsSerializer(serializers.ModelSerializer):
    aavso_data = AAVSODataSerializer(many=False, read_only=True)
    simbad_data = SimbadDataSerializer(many=False, read_only=True)
    astro_job = AstroMetryJobSerializer(many=False, read_only=True)

    class Meta:
        model = CorrFits
        fields = ['field_x', 'field_y', 'field_ra', 'field_dec', 'aavso_data', 'simbad_data', 'astro_job']
