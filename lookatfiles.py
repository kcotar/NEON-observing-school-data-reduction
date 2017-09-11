#lookatfiles.py

from astropy.io import fits
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt

list_science_images = 'list_object5_reduced'

image_filename = np.loadtxt(list_science_images, dtype='S50')


for f_img in image_filename:
  print f_img
  img_hud = fits.open(f_img[:-3])
  img_data = img_hud[1].data 
  img_data_np = np.array(img_data)

  plt.imshow(img_data_np, cmap='gray',vmin=-200, vmax=200)
  plt.show(block=False)
  plt.colorbar()
  
  raw_input("Press Enter to continue")
  plt.close("all")
  img_hud.close()
