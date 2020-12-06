import os
from modules.getImageUrls import getImageUrls
from modules.downloadImages import downloadImages
from modules.generateMasks import generateMasks
from modules.generateGif import generateGif


def main():
  urls = getImageUrls()
  inputs = downloadImages(urls)
  outputs = generateMasks(inputs)
  generateGif(inputs, 'color-grow.gif')

  # print(urls)

main()