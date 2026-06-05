# ********************************************************************
#
#  $Id: helloworld.py 72944 2026-04-24 08:06:03Z seb $
#
#  An example that shows how to use a  Yocto-Spectral
#
#  You can find more information on our web site:
#   Yocto-Spectral documentation:
#      https://www.yoctopuce.com/EN/products/yocto-spectral/doc.html
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************

import sys

from yoctolib.yocto_api import YRefParam, YAPI
from yoctolib.yocto_colorsensor import YColorSensor

def die(msg):
    YAPI.FreeAPI()
    sys.exit(msg + ' (check USB cable)')


# the API use local USB devices through VirtualHub
errmsg = YRefParam()
if YAPI.RegisterHub("localhost", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub failed: " + errmsg.value)

# To use a specific device, invoke the script as
#   python helloworld.py [serial_number]
# or
#   python helloworld.py [logical_name]
target = 'any'
if len(sys.argv) > 1:
    target = sys.argv[1]

if target == 'any':
    # retrieve any color sensor
    sensor = YColorSensor.FirstColorSensor()
    if sensor is None:
        die('No module connected')
    target = sensor.get_serialNumber()

# retrieve specified functions
colorSensor = YColorSensor.FindColorSensor(target + '.colorSensor')
if not colorSensor.isOnline():
    die("Yocto-Spectral '%s' not connected" % target)

print("Use device %s" % colorSensor.get_serialNumber())
while colorSensor.isOnline():
    colorSensor.set_workingMode(YColorSensor.WORKINGMODE_AUTO)
    colorSensor.set_estimationModel(YColorSensor.ESTIMATIONMODEL_REFLECTION)

    print("Near color : " + colorSensor.get_nearSimpleColor())
    print("RGB Hex : " + str(hex(colorSensor.get_estimatedRGB())))
    print("--------------------------------------------")
    YAPI.Sleep(5000)
YAPI.FreeAPI()
