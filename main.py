from m5stack import *
from m5ui import *
from uiflow import *
import hat
from weerstathome import lights, connect, ntpztime, dbo, dmo
import time

axp = axp192.Axp192()
axp.setLcdBrightness(40)
setScreenColor(0x000000)
label_tout = M5TextBox(75, 20, "Out", lcd.FONT_DejaVu40,0xFFFFFF, rotate=90)
label_tin = M5TextBox(35, 20, "In", lcd.FONT_DejaVu40,0xFFFFFF, rotate=90)

hat_yun = hat.get(hat.YUN)

leds = lights.Lights(hat_yun)
leds.zone_leds((0,0,0), (1,15))

print(connect.wifi("SSID", "password"))

wsin = dbo.Dbo("192.168.0.xxx", 8086, "weerstathome", "wsin2", "sensor", "value")

sensors = dmo.Dmo()

if not ntpztime.settime(3600):
    while True:
        leds.zone_leds((10,0,0), (1,15), 20)
        leds.zone_leds((0,0,0), (1,15), 20)

import urequests

def stringbuilder(device, limit):
    return "http://192.168.0.xxx:8086/query?db=weerstathome&q=SELECT%20waarde%20FROM%20%22wsex%22%20WHERE%20device=%27" + str(device) + "%27order%20by%20time%20desc%20LIMIT%20" + str(limit)

def paint_outside_colour(leds, label):
    url = stringbuilder("Tws1", 1)
    response = urequests.get(url).json()
    temp = response["results"][0]["series"][0]["values"][0][1]
    label.setText(str(round(float(temp), 1)))
    leds.colour(0, 35, temp, (6,10))

def presdif(leds):
    url = stringbuilder("Pws", 9)
    response = urequests.get(url).json()
    readings = response["results"][0]["series"][0]["values"]
    avgnew = (readings[0][1] + readings[1][1] + readings[2][1]) / 3
    avgold = (readings[-1][1] + readings[-2][1] + readings[-3][1]) / 3
    delta = avgnew - avgold
    leds.colour(-1.2, 1.2, delta, (4, 6))
    
def uv(leds):
    url = stringbuilder("Uws", 1)
    response = urequests.get(url).json()
    uv = response["results"][0]["series"][0]["values"][0][1]
    leds.colour(0, 7, uv, (10,12))

def windspeed(leds):
    url = stringbuilder("Sex", 1)
    response = urequests.get(url).json()
    ws = response["results"][0]["series"][0]["values"][0][1]
    leds.colour(0, 15, ws, (12,15))

def get_light(yun):
    l = yun.getLight()
    return round(1700000/l**1.5-6.65,2)

leds.zone_leds((0,0,10), (1,15), 50)
time.sleep(0.5)
leds.zone_leds((10,8,0), (1,15), 50)
time.sleep(0.5)
# leds.zone_leds((0,0,0), (1,15))
windspeed(leds)
leds.colour(0, 35, hat_yun.temperature, (1,4))
label_tin.setText(str(round(float(hat_yun.temperature), 1)))
paint_outside_colour(leds, label_tout)
presdif(leds)
uv(leds)
leds.update()


me = -1
while True:
    lt = time.localtime()
    if lt[4] % 10 != me:  # code inside gets run every time the minute rolls over
        date = "{:02d}/{:02d}".format(lt[2], lt[1])
        tijd = "{:02d}:{:02d}:{:02d}".format(lt[3], lt[4], lt[5])
        t, h, p, l = hat_yun.temperature, hat_yun.humidity, hat_yun.pressure, get_light(hat_yun)
        print(date, tijd, str(t) + "°C", str(h) + "%", str(p) + "hPa", l)
        sensors.add(t, h, p+1.1, l)
        label_tin.setText(str(round(float(t), 1)))
        if lt[4] % 10 == 0:  # code inside gets run every 10 minutes
            wsin.make_datapoint("temp", sensors.t / sensors.c)
            wsin.make_datapoint("hum", sensors.h / sensors.c)
            wsin.make_datapoint("pres", sensors.p / sensors.c)
            wsin.make_datapoint("light", sensors.l / sensors.c)
            sensors.reset()
            wsin.write_cache()
            time.sleep(3)
            windspeed(leds)
            leds.colour(0, 35, t, (1,4))
            paint_outside_colour(leds, label_tout)
            presdif(leds)
            uv(leds)
            leds.update()
            if lt[3] == 3 and lt[4] == 10:  # code inside runs once a day at 03:10
                ntpztime.settime(3600)  # update the current time, in case of zone change or drift
    me = lt[4] % 10  # update the variable that keeps the last minute
    time.sleep(0.5)