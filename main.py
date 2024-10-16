from pytubefix import Playlist
from utils import *
import os
import requests
from io import BytesIO
from PIL import Image
from collections import Counter
from datetime import datetime


audio_path = 'assets/audio/'
images_path = 'assets/images/'
github_url = 'https://github.com/bemuse01/kessoku-band-data/raw/main/'
playlist_url = 'https://www.youtube.com/watch?v=PiIAVnFX2eo&list=PL3On5o_P3DzPM6HYQ28qzR0262-eS_AWa'
thumbnail_url = 'https://img.youtube.com/vi/'
thubnail_size = '/maxresdefault.jpg'
data_path = 'data.json'


p = Playlist(playlist_url)
audios = os.listdir(audio_path)
images = os.listdir(images_path)
artist = p.title
data = load_json(data_path)
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
sub_ids = [i['sub_id'] for i in data['body']]


print(p.title)
print(len(p.video_urls))


data['header']['last_update'] = current_time


for i, video in enumerate(p.videos):

    title = video.title
    video_id = video.video_id


    if video_id in sub_ids:
        continue


    new_item = {
        "id": i,
        "sub_id": video_id,
        "artist": artist,
        "title": title,
        "media_file": "",
        "thumbnail": "",
        "main_color": ""
    }


    # audio
    audio_name = video_id + '.mp3'

    if audio_name not in audios:

        stream = video.streams.filter(abr='128kbps', file_extension='mp4', only_audio=True).first()
        stream_path = stream.download(output_path=audio_path, filename=video_id)
        
        os.rename(stream_path, os.path.join(audio_path, audio_name))

        new_item['media_file'] = github_url + audio_path + audio_name

    else:

        new_item['media_file'] = github_url + audio_path + audio_name


    # thumbnail
    image_name = video_id + '.jpg'

    if image_name not in images:
        response = requests.get(thumbnail_url + video_id + thubnail_size)
        output_path = os.path.join(images_path, image_name)
        
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
            r, g, b = most_common_color[0]

            print(f"{title}, most common color: {most_common_color[0]}, frequency: {most_common_color[1]}")

            cropped_image.save(output_path)

            new_item['thumbnail'] = github_url + images_path + image_name
            new_item['main_color'] = '{:02X}{:02X}{:02X}'.format(r, g, b)

        else:

            print(f"error code: {response.status_code}")

    else:

        image = Image.open(os.path.join(images_path, image_name))
        resized_image = image.resize((200, 200)) 

        pixels = list(resized_image.getdata())
        most_common_color = Counter(pixels).most_common(1)[0]
        r, g, b = most_common_color[0]

        print(f"{title}, most common color: {most_common_color[0]}, frequency: {most_common_color[1]}")

        new_item['thumbnail'] = github_url + images_path + image_name
        new_item['main_color'] = '{:02X}{:02X}{:02X}'.format(r, g, b)

    
    # push item
    data['body'].append(new_item)


# json
save_json(data_path, data)