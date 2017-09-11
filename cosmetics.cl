noao
imred
ccdred

ccdproc "" fixpix=no

# create bias frame
delete bias_s.fits
zerocombine input=@list_bias_s output=bias_s combine=median

# create flat frame
imarith @list_flat_s - bias_s @list_flat_nobias_s
delete flat_s.fits
flatcombine input=@list_flat_nobias_s output=flat_s combine=median scale=mode statsec="[150:400,2500:3000]" process=no delete=yes
imstat flat_s


# create corrected science images
#delete @list_J170341_nobias
#imarith @list_J170341 - bias_s @list_J170341_nobias
#delete @list_J170341_reduced
#imarith @list_J170341_nobias / flat_s @list_J170341_reduced
