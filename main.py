import os
from modules.getImageUrls import getImageUrls
from modules.downloadImages import downloadImages
from modules.generateMasks import generateMasks
from modules.generateGif import generateGif
from modules.uploadResult import uploadResult


def main():
  urls = getImageUrls()
  inputs = downloadImages(urls)
  outputs = generateMasks(inputs)
  generateGif(inputs, 'color-grow.gif')
  print("color gif generated")
  generateGif(outputs, 'bw-grow.gif')
  print("mask gif generated")
  print("upload colored gif");
  uploadResult('color-grow.gif', 'color-grow.gif')
  print("upload bw gif")
  uploadResult('bw-grow.gif', 'bw-grow.gif')

  # print(urls)

main()