from django.db import models
import os
from django.conf import settings
class UserUpload(models.Model):
    user_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    attachment = models.FileField(upload_to='uploads/%Y/%m/%d/',
                                   help_text='Only .txt, .doc, .docx files are allowed')
    audio_file_name = models.CharField(max_length=100, blank=True)
    audio_location = models.CharField(max_length=255, blank=True)
    merged_audio_path = models.CharField(max_length=255, blank=True)  # New field for merged audio path

    def __str__(self):
        return self.title
    
    #for downloading all audio files
  