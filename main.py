import os
from modules.getImageUrls import getImageUrls
from modules.downloadImages import downloadImages
from modules.generateMasks import MASK_TYPES, generateMasks


def main():
  urls = getImageUrls()
  inputs = downloadImages(urls)
  output = generateMasks(inputs)
  # print(urls)

main()