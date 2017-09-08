from astropy.io import fits
import numpy as np

list_science_images = 'list_object4'
list_shifts = 'ref_shift'

image_filename = np.loadtxt(list_science_images, dtype='S32')

ref_img = fits.open(image_filename[0])
ra_ref = ref_img[0].header.get('RA')
de_ref = ref_img[0].header.get('DEC')
ref_img.close()

txt_out = open(list_shifts,'w')
for i_img in range(0, len(image_filename)):
  print image_filename[i_img]
  obj_img = fits.open(image_filename[i_img])
  ra_obj = obj_img[0].header.get('RA')
  de_obj = obj_img[0].header.get('DEC')
  obj_img.close()
  x_shift = (ra_ref - ra_obj) * 3600. / 0.234
  y_shift = (de_ref - de_obj) * 3600. / 0.234
  txt_out.write(str(-1.*x_shift)+' '+str(0)+'\n')
txt_out.close()
  
