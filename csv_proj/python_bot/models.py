import os
from django.db import models

# Create your models here.

class SourceFile(models.Model):
    sno = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255,blank=True,unique=True)
    source_file = models.FileField(upload_to="source_files")
    created_at = models.DateTimeField

    def __str__(self):
        return self.file_name
    def filename(self):
        return os.path.basename(self.source_file.name)
    def delete(self):
        self.source_file.storage.delete(self.source_file.name)
        super().delete()
    

class SecondaryFile(models.Model):
    sno = models.AutoField(primary_key=True)
    secondary_file_name = models.CharField(max_length=255,blank=True,unique=True)
    secondary_file = models.FileField(upload_to="destination_files")
    created_at = models.DateTimeField

    def __str__(self):
        return self.secondary_file_name
    def delete(self):
        self.secondary_file.storage.delete(self.secondary_file.name)
        super().delete()