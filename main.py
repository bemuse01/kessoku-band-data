from pytubefix import Playlist
from structure import *
import os
import requests
from io import BytesIO
from PIL import Image
from collections import Counter

audio_path = 'assets/audio'
images_path = 'assets/images'
github_url = 'https://github.com/bemuse01/kessoku-band-data/raw/main/'
playlist_url = 'https://www.youtube.com/watch?v=PiIAVnFX2eo&list=PL3On5o_P3DzPM6HYQ28qzR0262-eS_AWa'
thumbnail_url = 'https://img.youtube.com/vi/'
thubnail_size = '/maxresdefault.jpg'


p = Playlist(playlist_url)
audios = os.listdir(audio_path)
images = os.listdir(images_path)
artist = p.title


print(p.title)
print(len(p.video_urls))


for i, video in enumerate(p.videos):


    title = video.title
    video_id = video.video_id


    # audio
    if video_id not in [v.split('.')[0] for v in audios]:

        stream = video.streams.filter(abr='128kbps', file_extension='mp4', only_audio=True).first()
        stream_path = stream.download(output_path=audio_path, filename=video_id)
        stream_name = stream_path.split('/').pop()

        audio_name = stream_name.split('.')[0] + '.mp3'
        os.rename(stream_path, os.path.join(audio_path, audio_name))


    # thumbnail
    if video_id not in [i.split('.')[0] for i in images]:
        
        response = requests.get(thumbnail_url + video_id + thubnail_size)
        output_path = os.path.join(images_path, video_id + '.jpg')
        
        if response.status_code == 200:
            
            image = Image.open(BytesIO(response.content))

            w = image.width
            h = image.height
            x = (w - h) / 2
            crop_area = (x, 0, x + h, h)
            cropped_image = image.crop(crop_area)
            cx = cropped_image.width
            cy = cropped_image.height

            resized_image = cropped_image.resize((200, 200)) 

            pixels = list(resized_image.getdata())
            most_common_color = Counter(pixels).most_common(1)[0]

            # pixel_color = image.getpixel((cx - 1, cy - 1))
            
            print(f"{title}, most common color: {most_common_color[0]}, frequency: {most_common_color[1]}")

            cropped_image.save(output_path)

        else:
            print(f"error code: {response.status_code}")


    # json
    