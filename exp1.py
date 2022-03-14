import numpy as np
import math as m
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider, Button

def wvl2rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).
    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''
    #380    440     490     510     580     645     750
    #       B               G               R                    
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma


    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0


    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R,G,B)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)

wavelenghth_slider_val = 700 #wav_l in nm
wavelenghth_light = wavelenghth_slider_val*(10**-9) #wav_l in m

color_ = wvl2rgb(wavelenghth_slider_val)#rgb tuple of current color

lmb=[700*(10**-9),550*(10**-9),475*(10**-9)]#wvl of R,G,B

i = 0.2 #intenisity in watt/m2
s = 0.00002 #slit sepr in metres
d = 50 #screen distance in metres
y_lim = 50
spc=0.075#y intervals
bh=0.2#height of spectral band width
y = np.arange(-y_lim,y_lim,spc)

for x in y:#polychromatic fringe pattern
    d1=m.sqrt(d**2 + (x-s/2)**2)
    d2=m.sqrt(d**2 + (x+s/2)**2)
    pathdif=abs(d1-d2)

    phi_r=2*(np.pi)*pathdif/lmb[0]
    ints_r=(4*i*(np.cos(phi_r/2)**2))

    phi_g=2*(np.pi)*pathdif/lmb[1]
    ints_g=(4*i*(np.cos(phi_g/2)**2))

    phi_b=2*(np.pi)*pathdif/lmb[2]
    ints_b=(4*i*(np.cos(phi_b/2)**2))

    ax.add_patch(Rectangle((x,-2*bh),spc*0.9,bh*0.9,
    color=(ints_r/0.8,ints_g/0.8,ints_b/0.8)))

intensities_light = []

def create_y_axis():
    global wavelenghth_light, wavelenghth_slider_val

    wavelenghth_light = wavelenghth_slider_val*(10**-9)
    print(wavelenghth_light)
    for x in y:#mono chromatc fringe pattern
        d1=m.sqrt(d**2 + (x-s/2)**2)
        d2=m.sqrt(d**2 + (x+s/2)**2)
        pathdif=abs(d1-d2)

        phi=2*(np.pi)*pathdif/wavelenghth_light
        intensities_light.append(4*i*(np.cos(phi/2)**2))
        f=intensities_light[-1]/(4*i)

        ax.add_patch(Rectangle((x,-bh),spc*0.9,bh*0.9,
        color=(color_[0]*f,color_[1]*f,color_[2]*f)))

create_y_axis()
l, = ax.plot(y,intensities_light ,color=color_, label="Red")

# Slider stuff
wav_slider_ax = plt.axes([0.15, 0.15, 0.7, 0.035], facecolor='lightgoldenrodyellow')
wav_slider = Slider(wav_slider_ax, 'Wavelengths', valmin=380 , valmax=700, valfmt='%1.0f', valstep=2, color=color_)

wav_slider.set_val(wavelenghth_slider_val)

def update(val):
    global intensities_light, wavelenghth_slider_val, color_
    wavelenghth_slider_val = wav_slider.val
    color_ = wvl2rgb(wavelenghth_slider_val)
    l.set_color(color_) 
    intensities_light.clear()
    create_y_axis()
    l.set_ydata(intensities_light)
    fig.canvas.draw()
wav_slider.on_changed(update)
plt.show()