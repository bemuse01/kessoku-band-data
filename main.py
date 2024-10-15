from pytubefix import Playlist
from structure import *
import os

audio_path = './assets/audio'
temp_path = './temp'
bitrate = 256000

playlist_url = 'https://www.youtube.com/watch?v=PiIAVnFX2eo&list=PL3On5o_P3DzPM6HYQ28qzR0262-eS_AWa'
p = Playlist(playlist_url)

videos = os.listdir(temp_path)

print(p.title)
print(len(p.video_urls))

for i, video in enumerate(p.videos):

    if video.title not in [v.split('.')[0] for v in videos]:
        
        video_stream = video.streams.filter(abr='128kbps', file_extension='mp4', only_audio=True).first()
        video_path = video_stream.download(output_path=temp_path)
        video_name = video_path.split('/').pop()

        audio_name = video_name.split('.')[0] + '.mp3'
        output_path = os.rename(video_path, os.path.join(temp_path, audio_name))

    else:

        video_path = os.path.join(temp_path, videos[i])
        video_name = video_path.split('/').pop()

        audio_name = video_name.split('.')[0] + '.mp3'
        output_path = os.rename(video_path, os.path.join(temp_path, audio_name))