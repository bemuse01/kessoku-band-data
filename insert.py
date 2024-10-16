from utils import *
import os
import requests
from io import BytesIO
from PIL import Image
from collections import Counter
from const import *
from delete import *


def insert(p):
    data = load_json(data_path)
    audios = os.listdir(audio_path)
    images = os.listdir(images_path)
    artist = p.title
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    ids = [i['id'] for i in data['body']['data']]


    for video in p.videos:

        title = video.title
        video_id = video.video_id


        if video_id in ids:
            continue


        new_item = {
            "id": video_id,
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
        data['body']['data'].append(new_item)


    data['header']['last_update'] = current_time

    save_json(data_path, data)
