import requests
import secrets
import os

subscription_key = secrets.subscription_key
assert subscription_key

face_api_url = secrets.face_api_url

headers = {'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key}

def send(path):
    data = open(path, 'rb')

    params = {
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'headPose',
    }

    response = requests.post(face_api_url, params=params,
                            headers=headers, data=data)
    return response.json()

if __name__=='__main__':
    image_directory = os.path.dirname(__file__) + '/image.jpg'
    response = send(image_directory)
    print(response)