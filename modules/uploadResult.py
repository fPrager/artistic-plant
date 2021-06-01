from urllib import request
from os import  environ
import json

PI_SHOT_PRESIGNED_API = "https://yzqcszhfh5.execute-api.eu-central-1.amazonaws.com/live/get-signed-url"
API_TOKEN = environ["token"]

def getPresignedUrl(name, dst) : 
  headers = {
      "Authorization": f"Bearer {API_TOKEN}"
  }
  body = {"contentType":"image/gif", "name": name}
  data = json.dumps(body)
  data = data.encode("ascii")
  req = request.Request(PI_SHOT_PRESIGNED_API, data, headers)
  with request.urlopen(req) as response:
    content = json.loads(response.read())
    return content['url']

def uploadResult(file, name, dst="result/") :
    presignedUrl = getPresignedUrl(name, dst)
    def readFileBytestream(image_path):
      data = open(image_path, 'rb').read()
      return data
    headers = {
      "Content-Type": "image/gif"
    }
    data = readFileBytestream(file)
    req = request.Request(url=presignedUrl, headers=headers, data=data, method='PUT')
    with request.urlopen(req) as response:
      print(response.read())
