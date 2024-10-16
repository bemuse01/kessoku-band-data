from pytubefix import Playlist
from utils import *
from const import *
from delete import *
from insert import *


p = Playlist(playlist_url)


print(p.title)
print(len(p.video_urls))


# delete
delete(p)


# insert
insert(p)