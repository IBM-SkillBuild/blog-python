import os
from datetime import datetime

audio_dir = 'static/audio'
print('Archivos MP3 actuales:')
print('=' * 50)

for filename in os.listdir(audio_dir):
    if filename.lower().endswith('.mp3'):
        file_path = os.path.join(audio_dir, filename)
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        file_size = os.path.getsize(file_path)
        print(f'{filename} - {mod_time.strftime("%Y-%m-%d %H:%M:%S")} - {file_size / 1024:.1f} KB') 