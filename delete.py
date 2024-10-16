from utils import *
import os
from const import *
from datetime import datetime


def delete(p):
    data = load_json(data_path)
    audios = os.listdir(audio_path)
    images = os.listdir(images_path)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    old_ids = data['body']['index']
    new_ids = [video.video_id for video in p.videos]
    remove_ids = list(set(old_ids) - set(new_ids))

    data['body']['data'] = [item for item in data['body']['data'] if item['id'] not in remove_ids]


    for rid in remove_ids:
        audio_name = rid + '.mp3'
        image_name = rid + '.jpg'


        if audio_name in audios:
            os.remove(os.path.join(audio_path, audio_name))
        else:
            print(f'{audio_name} not exists')

        if image_name in images:
            os.remove(os.path.join(images_path, image_name))
        else:
            print(f'{image_name} not exists')


    data['body']['index'] = new_ids
    data['header']['last_update'] = current_time

    save_json(data_path, data)