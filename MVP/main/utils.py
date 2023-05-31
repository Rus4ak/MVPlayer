from django.conf import settings
from pydub import AudioSegment
import os
import uuid

def handle_uploaded_file(audio_file):
    file_path = os.path.join(settings.MEDIA_ROOT, 'music')

    # Generate a unique filename
    file_name = f'{uuid.uuid4().hex}.mp3'

    # File compression
    audio = AudioSegment.from_file(audio_file)
    compressed_audio = audio.export(os.path.join(file_path, file_name), format='mp3', bitrate='128k')
    compressed_audio.close()

    return os.path.join('media', 'music', file_name)
