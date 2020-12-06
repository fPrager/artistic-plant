from os import path
from plantcv import plantcv as pcv

from modules.indexToFile import indexToFile

MASK_TYPES = {
  'BW':0,
  'COLORED': 1
}

def generateMask(input, output, maskType=MASK_TYPES['BW']): 
  pcv.params.debug=True #set debug mode
  # pcv.params.debug_outdir="./output.txt" #set output directory

  # Read image (readimage mode defaults to native but if image is RGBA then specify mode='rgb')
  # Inputs:
  #   filename - Image file to be read in 
  #   mode - Return mode of image; either 'native' (default), 'rgb', 'gray', 'envi', or 'csv'
  img, path, filename = pcv.readimage(filename=input, mode='rgb')

  s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

  # Threshold the saturation image
  s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')

  # Median Blur
  s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
  s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

  # Convert RGB to LAB and extract the Blue channel
  b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

  # Threshold the blue image
  b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')
  b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')

  # Fill small objects
  # b_fill = pcv.fill(b_thresh, 10)

  # Join the thresholded saturation and blue-yellow images
  bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

  # Apply Mask (for VIS images, mask_color=white)
  masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')

  # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
  masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
  masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

  # Threshold the green-magenta and blue images
  maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
  maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
  maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

  # Join the thresholded saturation and blue-yellow images (OR)
  ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
  ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)
  if maskType == MASK_TYPES['BW']:
    pcv.print_image(ab, filename=output)
    return (True , None)

  # Fill small objects
  ab_fill = pcv.fill(bin_img=ab, size=200)

  # Apply mask (for VIS images, mask_color=white)
  masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='black')
  if maskType == MASK_TYPES['COLORED']:
    pcv.print_image(masked2, filename=output)
    return (True , None)

  return (False , 'Unknown mask type.')

  """
  # Identify objects
  id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)

  # Define ROI
  roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=100, y=100, h=200, w=200)

  # Decide which objects to keep
  roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                              roi_hierarchy=roi_hierarchy, 
                                                              object_contour=id_objects, 
                                                              obj_hierarchy=obj_hierarchy,
                                                              roi_type='partial')

  # Object combine kept objects
  obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)

  ############### Analysis ################

  # Find shape properties, output shape image (optional)
  shape_imgs = pcv.analyze_object(img=img, obj=obj, mask=mask)

  # Shape properties relative to user boundary line (optional)
  boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, line_position=1680)
  pcv.print_image(boundary_img1, filename="pseudocolored_img.jpg")

  # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
  color_histogram = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='all')
  pcv.print_image(color_histogram, filename="color_histogram.jpg")

  # Pseudocolor the grayscale image
  pseudocolored_img = pcv.visualize.pseudocolor(gray_img=s, mask=mask, cmap='jet')
  
  pcv.print_image(pseudocolored_img, filename="pseudocolored_img.jpg")
  pcv.print_results(filename="result.txt")
  """

def generateMasks(inputs, dst="./output/"):
  masks = [] 
  for index, input in enumerate(inputs):
    mask = f"{dst}{indexToFile(index)}.jpg"
    if path.isfile(mask) == False:
      print(f"generate mask {index}/{len(inputs)-1}")
      generateMask(input, mask)
    else:
      print(f"skip generate mask {index}/{len(inputs)-1}")
    masks.append(mask)
    