from dataclasses import field
from django import forms
from .models import SourceFile , SecondaryFile

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = SourceFile
        fields = ('source_file','file_name')

class SecondaryModelForm(forms.ModelForm):
    class Meta:
        model = SecondaryFile
        fields = ('secondary_file_name','secondary_file')