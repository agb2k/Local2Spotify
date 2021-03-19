from tinytag import TinyTag
from pathlib import Path
import json


fileList = Path("D:/Music/").rglob('*.mp3')
data = {'music': []}

for path in fileList:
    file = str(path)
    tag = TinyTag.get(file)

    data['music'].append({
        'Title: ': tag.title,
        'Artist: ': tag.artist,
        'Album: ': tag.album
    })

    with open("C:/Users/abhin/PycharmProjects/Local2Spotify/Music.json", 'w') as fp:
        json.dump(data, fp, indent=4)
