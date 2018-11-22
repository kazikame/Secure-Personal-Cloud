from PIL import Image
import numpy as np

def get_first_band(image):
  shape = image.shape
  ans = np.zeros((shape[0], shape[1]))
  for r in range(shape[0]):
    for c in range(shape[1]):
      ans[r][c] = image[r][c][0]

  return ans

def evaluate(student_image, ref_image):
  segmented = Image.open(student_image)
  segmented = np.array(segmented)

  segmented_ref = Image.open(ref_image)
  segmented_ref = np.array(segmented_ref)

  if len(segmented.shape) == 3:
    segmented = get_first_band(segmented)
  
  diff = segmented == segmented_ref
  diff_shape = diff.shape
  total_num_pixels = diff_shape[0] * diff_shape[1]
  misclassified_pixel_count = 0
  for r in range(diff_shape[0]):
    for c in range(diff_shape[1]):
      if not diff[r][c]: 
        misclassified_pixel_count += 1

  misclassified_ratio = float(misclassified_pixel_count) / float(total_num_pixels)
  return 1 - misclassified_ratio

try:
  accuracy = evaluate('segmented_eu.png', 'segmented_eu_ref.png')
  print('%f' % (22 * accuracy), end='\t')
except Exception:
  print('0', end='\t')

try:
  accuracy = evaluate('segmented_man.png', 'segmented_man_ref.png')
  print('%f' % (22 * accuracy), end='\t')
except Exception:
  print('0', end='\t')
