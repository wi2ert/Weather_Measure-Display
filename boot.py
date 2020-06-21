import sys 
sys.path.append('flowlib/lib')

import machine, time, m5base, uiflow
from m5stack import *
__VERSION__ = m5base.get_version()

lcd.clear(lcd.BLACK)
lcd.image(lcd.CENTER, 35, 'img/uiflow_logo_80x80.bmp')
lcd.print(__VERSION__, lcd.CENTER, 10)

start = uiflow.cfgRead('start')
mode = uiflow.cfgRead('mode')

if start == 'flow':
    if mode == 'usb':
        lcd.print('USB', lcd.CENTER, 125)
    else:
        lcd.print('Cloud', lcd.CENTER, 125)
else:
    lcd.print(start.upper(), lcd.CENTER, 120)


cnt_down = time.ticks_ms() + 1000
while time.ticks_ms() < cnt_down:
    if btnA.wasPressed():
        lcd.clear()
        choose = 0
        lcd.image(0, 0, 'img/2-1.jpg')
        while True:
            time.sleep_ms(50)
            if btnB.wasPressed():
                choose = choose + 1 if choose < 2 else 0
                lcd.image(0, 0, 'img/2-{}.jpg'.format(choose + 1))
            if btnA.wasPressed():
                if choose == 0:
                    uiflow.start('flow')
                elif choose == 1:
                    from app_manage import file_choose
                    file_choose()
                    uiflow.start('app')
                elif choose == 2:
                    import statechoose
                    statechoose.start()
                break
    if btnB.wasPressed():
        if start == 'flow':
            uiflow.start('app')
        else:
            uiflow.start('flow')

# 0:app, 1:flow_internet, 2:debug, 3:flow use 
start = uiflow.cfgRead('start')
if start == 'app':
    m5base.app_start(0)
elif start == 'flow':
    if uiflow.cfgRead('mode') == 'usb':
        m5base.app_start(3)
        lcd.print('USB', lcd.CENTER, 125)
    else:
        lcd.print('Cloud', lcd.CENTER, 125)
        m5base.app_start(1)
else:
    m5base.app_start(2)

del start
del cnt_down