import sys
import os
from fbchat import Client
from fbchat.models import *

general = [
    'film',
    'ishootfilm',
    'shootfilm',
    'filmcommunity',
    'filmisnotdead',
    'buyfilmnotmegapixels',
    'filmphotography',
    'filmfeed',
    'analogphotography',
    'analogfeatures',
    'postthepeople',
    'streetphotography',
    'filmcamera',
    'staybrokeshootfilm',
    'stayandwander',
    'magnumphotos',
    'lensculture'
]

cameras = {
    'm2': (['leica', 'leicam', '35mm', '35mmfilm'], 'M2'),
    'p67': (['pentax67', 'pentax', '120mm', 'mediumformat'], 'Pentax 67')
}

films = {
    'portra': (['kodak','colorfilm', 'kodakportra'], 'Portra'),
    'fuji400h': (['ishootfujifilm', 'colorfilm', 'fuji400h', 'fujifilm'], 'Fuji 400H'),
    'fuji160ns': (['ishootfujifilm', 'colorfilm', 'fuji160ns', 'fujifilm'], 'Fuji 160NS'),
    'trix': (['kodak', 'blackandwhite', 'kodaktrix', 'madewithkodak'], 'Tri-X'),
    'natura': (['ishootfujifilm', 'colorfilm', 'fujinatura', 'fujifilm'], 'Fuji Natura')
}

cities = {
    'taipei': (['taipei'], 'taiwan'),
    'tamsui': (['tamsui'], 'taiwan'),
    'jiufen': (['oldstreet', 'taipei', 'jiufen'], 'taiwan'),
    'kyoto': (['kyoto'], 'japan'),
    'osaka': (['osaka'], 'japan'),
    'tokyo': (['tokyo'], 'japan'),
    'sf': (['sanfrancisco'], 'california'),
    'la': (['losangels', 'la'], 'california'),
    'berkeley': (['berkeley', 'berkeleypov'], 'california')
}

countries = {
    'japan': ['unknownjapan', 'explorejapan', 'japan'],
    'taiwan': ['iseetaiwan', 'taiwan', 'exploretaiwan'],
    'california': ['california']
}

def get_city(city):
    if city not in cities:
        print('ERROR: city not found')
        print('Available cities:')
        for c in cities:
            print(c)
        return []
    words, country = cities[city]
    return words + countries[country]


def get_film(film):
    if film not in films:
        print('ERROR: film not found')
        print('Available films:')
        for f in films:
            print(f)

        return [], ''
    return films[film]


def get_camera(camera):
    if camera not in cameras:
        print('ERROR: camera not found')
        print('Available cameras:')
        for c in cameras:
            print(c)

        return [], ''
    return cameras[camera]


def get_extras(extras):
    return set(extras.split(','))


def format_tags(tags):
    tags = ['#' + tag for tag in tags]
    return '.\n' * 5 + ' '.join(tags)


def format_caption(caption, camera_name, film_name):
    caption = '{0}\n{1} + {2}'.format(caption, camera_name, film_name)
    return caption


def main():
    if len(sys.argv) < 5:
        print('USAGE: python ighash.py [camera] [film] [city] [extras..]')
        return

    caption, camera, film, city = sys.argv[1:5]

    camera_tags, camera_name = get_camera(camera)
    film_tags, film_name = get_film(film)
    location_tags = get_city(city)

    tags = general + camera_tags + film_tags + location_tags

    if len(sys.argv) > 5:
        extras = sys.argv[5]
        tags += get_extras(extras)

    print('Total words: {0}\n'.format(len(tags)))

    if len(tags) > 30:
        print('WARNING: number of words is greater than 30')
        return

    if 'FB_EMAIL' not in os.environ or 'FB_PASS' not in os.environ:
        print('ERROR: Facebook credentials not found in environment variables')
        return

    client = Client(os.environ['FB_EMAIL'], os.environ['FB_PASS'])

    client.send(Message(text=('=' * 23)), thread_id=client.uid, thread_type=ThreadType.USER)

    formatted_caption = format_caption(caption, camera_name, film_name)
    print('Sending caption message...')
    print(formatted_caption,'\n')
    client.send(Message(text=formatted_caption), thread_id=client.uid, thread_type=ThreadType.USER)

    formatted_tags = format_tags(tags)
    print('Sending tags message...')
    print(formatted_tags)
    client.send(Message(text=formatted_tags), thread_id=client.uid, thread_type=ThreadType.USER)

    client.logout()

if __name__== "__main__":
    main()

