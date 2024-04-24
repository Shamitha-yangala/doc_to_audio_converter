
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserUploadForm
from .models import UserUpload
from gtts import gTTS
import os
import docx  # for handling .docx files
import zipfile
from django.conf import settings
import io




def display_all_files(request):
    # Retrieve all instances of UserUpload model from the database
    all_files = UserUpload.objects.all()

    # Pass the list of UserUpload instances to the template
    return render(request, 'app1/all_files.html', {'all_files': all_files})

def upload_document(request):
    if request.method == 'POST':
        form = UserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_upload = form.save(commit=False)  # Don't save yet, to modify audio file details
            # Extract text from the uploaded document
            uploaded_file = request.FILES['attachment']
            if uploaded_file.name.endswith('.docx'):
                text = extract_text_from_docx(uploaded_file)
            elif uploaded_file.name.endswith('.txt'):
                text = extract_text_from_txt(uploaded_file)
            else:
                errors = ['Only .txt, .doc, .docx files are allowed']
                return render(request, 'app1/upload_document.html', {'form': form, 'errors': errors})

            # Convert text to audio
            audio_files = convert_text_to_audio(text, user_upload.title)

            # Save audio file details to the UserUpload instance
            user_upload.audio_file_name = ', '.join([os.path.basename(file) for file in audio_files])
            user_upload.audio_location = ', '.join(audio_files)
            user_upload.save()

            # Render success page with necessary data
            return redirect('upload_success', pk=user_upload.pk)
    else:
        form = UserUploadForm()
    return render(request, 'app1/upload_document.html', {'form': form})

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_text_from_txt(txt_file):
    return txt_file.read().decode('utf-8')



def convert_text_to_audio(text, title):
    # Create the directory to store audio files
    audio_dir = os.path.join('media', 'audio', title)
    os.makedirs(audio_dir, exist_ok=True)

    # Split the text into words
    words = text.split()
    chunks = []
    chunk = ""
    for word in words:
        # Check if adding the next word exceeds the chunk size
        if len(chunk) + len(word) + 1 <= 2000:  # Adding 1 for space between words
            chunk += " " + word
        else:
            chunks.append(chunk)
            chunk = word
    chunks.append(chunk)  # Add the last chunk

    audio_files = []
    for i, chunk in enumerate(chunks):
        tts = gTTS(text=chunk, lang='en')
        audio_file_path = f'media/audio/{title}/{title}_CH_{i+1}.mp3'  # Adjust filename format
        tts.save(audio_file_path)
        audio_files.append(audio_file_path)
    return audio_files



def upload_success(request, pk):
    user_upload = get_object_or_404(UserUpload, pk=pk)
    
    audio_files = [audio_file.strip() for audio_file in user_upload.audio_location.split(',')]
    print('------------------',audio_files,'------------')



    
    return render(request, 'app1/upload_success.html', {'user_upload': user_upload, 
                                                        'audio_files': audio_files,
                                                        # 'merged_audio_path': merged_audio_path
                                                        })




def download_all_audio_files(request, pk):
    user_upload = get_object_or_404(UserUpload, pk=pk)
    audio_location = [audio_file.strip() for audio_file in user_upload.audio_location.split(',')]
    # audio_location = user_upload.audio_location.split(',')  # Assuming file paths are separated by ';'

    # Create a BytesIO buffer to store the zip file
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in audio_location:
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                zip_file.write(file_path, arcname=file_name)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="downloaded_files.zip"'
    return response



