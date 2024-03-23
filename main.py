import requests
import json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(
    "MONGODB_URL")


access_token = 'ACCESS_TOKEN'

db = client.frames
images = db.images_links




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




if __name__ == "__main__":

    image_link = upload_image(access_token, "image.png")
    
    upload_data = {
    "image_link": image_link,
    "timestamp": datetime.now()  # Adding the current timestamp
}

    image_id = images.insert_one(upload_data).inserted_id
