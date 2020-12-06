from urllib import request
from os import path
from modules.indexToFile import indexToFile

def downloadImages(urls, dst="./input/") :
  images = []
  for index, url in enumerate(urls):
    image = f"{dst}{indexToFile(index)}.jpg"
    if path.isfile(image) == False:
      print(f"downloading image {index}/{len(urls)-1}")
      request.urlretrieve(url, image)
    else:
      print(f"skip downloading image {index}/{len(urls)-1}")
    images.append(image)
  return images
