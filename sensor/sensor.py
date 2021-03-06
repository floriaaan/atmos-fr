# sensor ESP8206-01 script
import json
import urequests
import random
import time
from machine import I2C, Pin
from i2c_lcd8050 import I2cLcd
import si7021
import machine

DEFAULT_I2C_ADDR = 0x27

i2C_c = machine.I2C(-1, machine.Pin(2), machine.Pin(0))
i2C_l = I2C(scl=Pin(2), sda=Pin(0))
temp_sensor = si7021.Si7021(i2C_c)
lcd = I2cLcd(i2C_l, DEFAULT_I2C_ADDR, 2, 16)


def http_post(probe_id, temp, humidity):
    url = 'http://floriaaan.alwaysdata.net/atmos/measure/add/'
    datas = {
        'probe_id': probe_id,
        'temp': temp,
        'humidity': humidity
    }
    headers = {
        'charset': 'utf-8',
        'Access-Control-Allow-Headers': '*'
    }
    resp = urequests.post(url, data=json.dumps(datas), headers=headers)
    lcd.clear()
    lcd.putstr("Requête envoyée")
    time.sleep(2)


def moyenneTemp():
    temp = 0
    for i in range(0,5):
        temp += temp_sensor.temperature
        time.sleep(1)

    moy_temp = temp / 5
    moy_temparr = round(moy_temp, 2)
    lcd.clear()
    lcd.putstr("Temperature :\n " + str(moy_temparr) + " C")
    return moy_temparr


def moyenneHumid():
    humid = 0
    for i in range(0,5):
        humid += temp_sensor.relative_humidity
        time.sleep(1)


    moy_humi = humid / 5
    moy_humiarr = round(moy_humi, 2)
    lcd.clear()
    lcd.putstr("Humidite :\n " + str(moy_humiarr) + " %")

    return moy_humiarr


def sensor_dispsend():
    while True:
        try:
            moy_temp = moyenneTemp()
            moy_humi = moyenneHumid()

            http_post(1, moy_temp, moy_humi)
        except KeyboardInterrupt:
            lcd.clear()
            lcd.putstr("Keyboard\nInterrupt!")
            exit()
        except:
            lcd.clear()
            print("!!!ERROR!!!")
            lcd.putstr("!!!ERROR!!!")

        time.sleep(10)


def sensor_disp():
    while True:
        try:
            moy_temp = moyenneTemp()
            moy_humi = moyenneHumid()

        except KeyboardInterrupt:
            lcd.clear()
            lcd.putstr("Keyboard\nInterrupt!")
            exit()
        except:
            lcd.clear()
            print("!!!ERROR!!!")
            lcd.putstr("!!!ERROR!!!")

        time.sleep(3)
