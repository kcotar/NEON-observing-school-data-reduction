# ----------------------------------------------------
# ---------- IRAF script for spectra preprocessing ---
# ----------------------------------------------------

# select iraf package
noao
imred
ccdred

# create bias frame
delete bias_l.fits
zerocombine input=@list_bias_l output=bias_l combine=median

# create flat frame
imarith @list_flat_l - bias_l @list_flat_nobias_l
delete flat_l_temp.fits
flatcombine input=@list_flat_nobias_l output=flat_l_temp combine=median scale=mode statsec="[850:1050,2400:2800]" process=no delete=yes

# normalize flat field frame
delete flat_l_temp_sub.fits
imcopy flat_l_temp[850:1050,2400:2800] flat_l_temp_sub
imstat images=flat_s_temp_sub fields=mode format=no > flat_stat.log
delete flat_l.fits
imarith flat_l_temp / @flat_stat.log flat_l

# create bias corrected and flatened science images
delete @list_J032224_nobias
imarith @list_J032224 - bias_l @list_J032224_nobias
delete @list_J032224_red
imarith @list_J032224_nobias / flat_l @list_J032224_red
