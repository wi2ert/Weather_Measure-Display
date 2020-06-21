import time
from math import sin

class Lights:
    def __init__(self, yun, nm=20):
        self.yun = yun
        self.nm = nm
        self.leds_c = [(0,0,0)] * 15
        
    def __rgb_to_hex(self, rgb):
        return int('0x%02x%02x%02x' % rgb, 16)

    def __calc_gradient(self, c1, c2, amount):
        # eg 0.2 => mostly c1
        deltar = (c1[0] - c2[0]) * amount
        deltag = (c1[1] - c2[1]) * amount
        deltab = (c1[2] - c2[2]) * amount
        return round(c1[0] - deltar), round(c1[1] - deltag), round(c1[2] - deltab)

    def __calc_colour(self, low, up, val):
        rxt = (up-low)/10
        val = up+rxt if val > up+rxt else val
        val = low-rxt if val < low-rxt else val
        i = 100* (val-low)/(up-low)
        r = int(255*sin(2.4+i/17))
        g = int(250*sin(5.9 + i/30))
        b = int(250*sin(0.7 + i/25))
        return tuple(map(lambda x: 0 if x < 0 else x, (r, g, b)))
    
    def zone_leds(self, colour, zone, delay=0):
        for i in range(zone[0], zone[1]):
            self.yun.SetRGB(i, self.__rgb_to_hex(colour))
            time.sleep(delay/1000)
                

    def __nightmode(self, colour, n):
        return tuple(map(lambda x: round(x/n), colour))
    
    def colour(self, low, up, val, zone):
        for i in range(zone[0], zone[1]):
            self.leds_c[i-1] = self.__nightmode(self.__calc_colour(low, up, val), self.nm)
    
    def update(self):
        print("updating leds, nightmode = " + str(self.nm))
        for i in range(14,0,-1):
            self.yun.SetRGB(i, self.__rgb_to_hex(self.leds_c[i-1]))

