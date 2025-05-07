# ********************************************************************
#
#  $Id: helloworld.py 66294 2025-05-06 10:17:53Z seb $
#
#  An example that show how to use a  Yocto-Meteo
#
#  You can find more information on our web site:
#   Yocto-Meteo documentation:
#      https://www.yoctopuce.com/EN/products/yocto-meteo/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************
import sys

from yoctolib.yocto_api import YRefParam, YAPI
from yoctolib.yocto_gps import YGps


def die(msg):
    YAPI.FreeAPI()
    sys.exit(msg + ' (check USB cable)')


# the API use local USB devices through VirtualHub
errmsg: YRefParam = YRefParam()
if YAPI.RegisterHub("localhost", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub failed: " + errmsg.value)

# To use a specific device, invoke the script as
#   python helloworld.py [serial_number]
# or
#   python helloworld.py [logical_name]
target: str = 'any'
if len(sys.argv) > 1:
    target = sys.argv[1]

if target == 'any':
    # retrieve any humidity sensor
    sensor: YGps = YGps.FirstGps()
    if sensor is None:
        die('No module connected')
    target = sensor.get_serialNumber()

# retrieve specified functions
gps: YGps = YGps.FindGps(target + '.gps')
if not gps.isOnline():
    die("Yocto-GPS '%s' not connected" % target)

print("Use device %s" % gps.get_serialNumber())

while gps.isOnline():
    if gps.get_isFixed() != YGps.ISFIXED_TRUE:
        print("Fixing...")
    else:
        print(gps.get_latitude() + "  " + gps.get_longitude())
    YAPI.Sleep(1000)
YAPI.FreeAPI()
