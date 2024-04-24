from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    
    path('', upload_document, name='upload_document'),
    path('all_files', display_all_files, name='all_files'),
    path('upload/success/<int:pk>/', upload_success, name='upload_success'),
    path('download_all_audios/<int:pk>/', download_all_audio_files, name='download_all_audios'),
   
    
    
    
   
   
]