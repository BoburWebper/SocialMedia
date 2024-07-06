from pprint import pprint

import requests

url = "https://youtube-video-and-shorts-downloader1.p.rapidapi.com/api/getYTVideo"

querystring = {"url": "https://youtu.be/BjPKs2Dl7Ew?si=yIjSzA4WBDnqKXHB"}

headers = {
    "x-rapidapi-key": "3e98ed8ce1msh1a05c8a7aede75ap1ccdb6jsn2f6f17651931",
    "x-rapidapi-host": "youtube-video-and-shorts-downloader1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.status_code)
pprint(response.json())
