# ********************************************************************
#
#  $Id: helloworld.py 65391 2025-03-27 11:10:52Z mvuilleu $
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

from yoctolib.yocto_api import *
from yoctolib.yocto_anbutton import *

def die(msg):
    YAPI.FreeAPI()
    sys.exit(msg + ' (check USB cable)')

# setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub failed: " + errmsg.value)

# In order to use a specific device, invoke the script as
#   python doubleBuffering.py [serial_number]
# or
#   python doubleBuffering.py [logical_name]
target = 'any'
if len(sys.argv) > 1:
    target = sys.argv[1]

if target == 'any':
    # retrieve any compatible module
    func = YAnButton.FirstAnButton()
    if func is None:
        die('No Yocto-Knob connected')
    target = func.get_serialNumber()

# retrieve specified module
channel1 = YAnButton.FindAnButton(target + '.anButton1')
channel5 = YAnButton.FindAnButton(target + '.anButton5')
if not channel1.isOnline():
    die("Yocto-Knob '%s' not connected" % target)

done = False
while not done:
    line = ""
    if channel1.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        line = "Button 1 pressed     "
    else:
        line = "Button 1 not pressed "
    line += ' - analog value: ' + str(channel1.get_calibratedValue())
    print(line)

    if channel5.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        line = "Button 5 pressed     "
    else:
        line = "Button 5 not pressed "
    line += ' - analog value: ' + str(channel5.get_calibratedValue())
    print(line)

    print('(press both buttons simultaneously to exit)')
    done = (channel1.get_isPressed() == YAnButton.ISPRESSED_TRUE) and \
           (channel5.get_isPressed() == YAnButton.ISPRESSED_TRUE)
    YAPI.Sleep(1000)
YAPI.FreeAPI()