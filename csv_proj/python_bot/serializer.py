from csv import excel
from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from python_bot.models import *


class Get_Source_Data_Serializer(serializers.Serializer):
    class Meta:
        model=SourceFile
        fields=[
            'file_name',
        ]


class Get_Secondary_Data_Serializer(serializers.Serializer):
    class Meta:
        model=SecondaryFile
        fields=[
            'secondary_file_name',
        ]