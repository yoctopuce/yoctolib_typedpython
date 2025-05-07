# ********************************************************************
#
#  $Id: helloworld.py 66267 2025-05-06 07:58:57Z seb $
#
#  An example that show how to use a  Yocto-Knob
#
#  You can find more information on our web site:
#   Yocto-Knob documentation:
#      https://www.yoctopuce.com/EN/products/yocto-knob/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************
import sys

from yoctolib.yocto_api import YAPI, YRefParam
from yoctolib.yocto_colorled import YColorLed


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
    # retrieve any compatible module
    func: YColorLed = YColorLed.FirstColorLed()
    if func is None:
        die('No Yocto-Color connected')
    target = func.get_serialNumber()

led1: YColorLed = YColorLed.FindColorLed(target + '.colorLed1')
led2: YColorLed = YColorLed.FindColorLed(target + '.colorLed2')

all_colors = [0xff0000, 0x00ff00, 0x0000ff]
for color in all_colors:
    print("Change color to 0x%06x" % color)
    led1.set_rgbColor(color)  # immediate transition
    led2.rgbMove(color, 1000)  # smooth transition
    YAPI.Sleep(1000)

YAPI.FreeAPI()
