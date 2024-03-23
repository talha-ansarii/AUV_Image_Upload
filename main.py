import requests
import json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(
    "mongodb+srv://admin:OvpIVRbKRSH92ZQW@cluster0.hymysuv.mongodb.net/")

client_id = '071feac917ced9c'
client_secret = 'cff15a70650188c9da7525312034a087a6c1a4ec'
referesh_token = '8c83a1ec729ba7bb0e466a4e6086653abf42cd7b'
access_token = 'c35a9290605ddde61edc26f0b50c6cff188eb13d'

db = client.frames
images = db.images_links


def create_album(access_token):
    url = "https://api.imgur.com/3/album"

    payload = {
        'title': 'AUV Album',
        'description': 'This albums contains images coming from ROV.',
        'cover': 'MwDV3S5'}
    files = [

    ]
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    album_data = json.loads(response.text)
    print(album_data)
    album_id = json.loads(response.text)['data']['id']
    album_deletehash = json.loads(response.text)['data']['deletehash']
    print("album created", album_id)
    return album_data


def upload_image(access_token, image_path):

    url = "https://api.imgur.com/3/image"
    payload = {'type': 'file',
               'title': 'Image upload in album AUV',
               'description': 'Image from AUV.'}
    files = [
        ('image', ('image.png', open(image_path, 'rb'), 'image/png'))
    ]
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    image_data = json.loads(response.text)

    if image_data['success'] == False:
        print("Error in uploading image", image_data)
        return None

    image_link = json.loads(response.text)["data"]["link"]
    print("image uploaded", image_link)

    return image_link


def add_image_to_album(image_deletehash, album_deletehash):
    url = f'https://api.imgur.com/3/album/{album_deletehash}/add'

    payload = {'deletehashes[]': f'{image_deletehash}'
               }
    files = [

    ]
    headers = {
        'Authorization': f'Bearer {access_token}',

    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def get_album_images(access_token, album_id):
    url = f"https://api.imgur.com/3/album/{album_id}/images"
    payload = {}
    files = [

    ]
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)

    print(response.text)
    return json.loads(response.text)


if __name__ == "__main__":

    image_link = upload_image(access_token, "image.png")
    
    upload_data = {
    "image_link": image_link,
    "timestamp": datetime.now()  # Adding the current timestamp
}

    image_id = images.insert_one(upload_data).inserted_id
