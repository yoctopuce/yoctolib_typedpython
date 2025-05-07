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
from yoctolib.yocto_weighscale import YWeighScale


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
    func: YWeighScale = YWeighScale.FirstWeighScale()
    if func is None:
        die('No Yocto-Bridge connected')
    target = func.get_serialNumber()

sensor: YWeighScale = YWeighScale.FindWeighScale(target + '.weighScale1')

if not sensor.isOnline():
    die('device not connected')

# On startup, enable excitation and tare weigh scale
print("Resetting tare weight...")
sensor.set_excitation(YWeighScale.EXCITATION_AC)
YAPI.Sleep(3000)
sensor.tare()

while sensor.isOnline():
    print("Weight:  %f %s" % (sensor.get_currentValue(), sensor.get_unit()))
    print("  (Ctrl-C to stop)")
    YAPI.Sleep(1000)
YAPI.FreeAPI()
