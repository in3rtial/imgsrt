
# spectrum sort
#researchgate.net/post/What_is_a_good_way_to_convert_a_RGB_pixel_to_a_wavelength
#In the scalar path, we're converting RGB to HSV, and then ignoring the SV
#part and the 300°-360° section of the hue part since it's magenta, a
#two-photon color. We then perform a 1:1 mapping of 0°-300° to 750-380 nm.
#A histogram of this across the image gives us a spectrum, and aligning these
#spectra according to time gives us a spectrogram.


def generate_rgb_to_spectrum(rgb_coordinates):
    """converts RGB -> 380-780nm
    http://www.physics.sfasu.edu/astro/color/spectra.html"""
    CV = zeros((500, 500, 3))
    M = 400
    N = 50
    MAX = 255
    GAMMA = 0.80

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            WL = 380 + (i * 400 / M)
            if(380 <= WL <= 440):
                R = (-1 * (WL - 440)) / (440 - 380)
                G = 0
                B = 1
            elif(440 <= WL <= 490):
                R = 0
                G = (WL - 440) / (490 - 440)
                B = 1
            elif(490 <= WL <= 510):
                R = 0
                G = 1
                B = (-1 * (WL - 510)) / (510 - 490)
            elif(510 <= WL <= 580):
                R = (WL - 510) / (580 - 510)
                G = 1
                B = 0
            elif(580 <= WL <= 645):
                R = 1
                G = (-1 * (WL - 645)) / (645 - 580)
                B = 0
            elif(645 <= 780):
                R = 1
                G = 0
                B = 0
            # let the intensity SSS fall off near the vision limit
            if(WL > 700):
                SSS = 0.3 + (0.7 * (780 - WL) / (780 - 700))
            elif(WL < 420):
                SSS = 0.3 + (0.7 * (WL - 380) / (420 - 380))
            else:
                SSS = 1

            # GAMMA adjust and write image to an array
            CV[i][j][0] = (SSS * R) ** GAMMA
            CV[i][j][1] = (SSS * G) ** GAMMA
            CV[i][j][2] = (SSS * B) ** GAMMA

        # write result to file
        #for i in range(1, M + 1):
            #for j in range(1, N + 1):
