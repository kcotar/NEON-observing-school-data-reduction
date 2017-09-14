from astropy.io import fits

fits_file = 'J032224.fits'
dat_file = fits_file[:-4]+'dat'

hud_fits = fits.open(fits_file)

spectra = hud_fits[1].data['flux']
wvl = 10.0**hud_fits[1].data['loglam']

dat_t = open(dat_file, 'w')
for i in range(len(spectra)):
  dat_t.write(str(wvl[i])+' '+str(spectra[i])+'\n')

dat_t.close()
hud_fits.close()
