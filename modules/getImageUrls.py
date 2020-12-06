from urllib import request
import json 

PI_SHOT_LIST_API = "https://yzqcszhfh5.execute-api.eu-central-1.amazonaws.com/live/list-shots"


def getImageUrls():
  urls = []
  with request.urlopen(PI_SHOT_LIST_API) as url:
    data = json.loads(url.read().decode())
    urls = data['body']['urls']
  return list(filter(lambda url: url.lower().endswith(".jpg"), urls))

