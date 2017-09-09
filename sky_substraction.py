from astropy.io import fits
from astropy.table import Table
import numpy as np

prefix = 'NCAi0'
image_start = 60628
image_end = 60669

list_science_images = 'list_object4'
# create a list o images
txt_list = open(list_science_images, 'w')
for i_img in range(image_start, image_end+1):
  txt_list.write(prefix + str(i_img) + '.fits\n')
txt_list.close()

# other lists
list_science_images_reduced = list_science_images + '_reduced'
list_science_images_aligned = list_science_images + '_aligned'

flat_image = 'flat_final.fits'

# data reading
flat_hud = fits.open(flat_image)
flat_img = flat_hud[0].data
print np.shape(flat_img)

# sky median substraction
suffix = '_mediansub'
image_filename = np.loadtxt(list_science_images, dtype='S32')
sky_sub_imgs = np.ndarray((1024,1024,len(image_filename)))
i_s = 0
for f_img in image_filename:
  print f_img
  new_filename = f_img[:-5]+suffix+'.fits'
  image_filename[i_s] = new_filename
  # open image
  img_hud = fits.open(f_img)
  # remove headers
  for h in [7,5,4,3,2,1]:  # remove exposures
    del img_hud[h]
  # remove median
  img_data = img_hud[1].data 
  img_hud[1].data = img_data  - np.median(img_data)
  # store to array
  sky_sub_imgs[:,:,i_s] = np.array(img_hud[1].data)
  i_s += 1
  # save
  img_hud.writeto(new_filename, overwrite=True)
  img_hud.close()

# median combine and save sky image
sky_image = np.median(sky_sub_imgs, axis=2)
flat_hud[0].data = sky_image
flat_hud.writeto('syk_image.fits', overwrite=True)
flat_hud.close()

# substract sky image and median from image
suffix = '_sykcorr_flat'
i_s = 0
txt_list_out = open(list_science_images_reduced, 'w')
txt_list_out_al = open(list_science_images_aligned, 'w')
for f_img in image_filename:
  print f_img
  img_hud = fits.open(f_img)
  # remove sky
  img_data = img_hud[1].data
  img_data -= sky_image
  # remove median
  img_data -= np.median(img_data)
  # flatten an image
  img_data /= flat_img
  # save
  img_hud[1].data = img_data 
  new_filename = f_img[:-5]+suffix+'.fits'
  image_filename[i_s] = new_filename
  img_hud.writeto(new_filename, overwrite=True)
  img_hud.close()
  # add to list
  txt_list_out.write(new_filename+'[1]\n')
  txt_list_out_al.write(new_filename[:-5]+'_aligned.fits[0]\n')
txt_list_out.close()
txt_list_out_al.close()
