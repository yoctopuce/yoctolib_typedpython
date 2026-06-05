# ********************************************************************
#
#  $Id: helloworld.py 72944 2026-04-24 08:06:03Z seb $
#
#  An example that shows how to use a  Yocto-RFID
#
#  You can find more information on our web site:
#   Yocto-RFID documentation:
#      https://www.yoctopuce.com/EN/products/yocto-rfid/doc.html
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************

import sys

from yoctolib.yocto_anbutton import YAnButton
from yoctolib.yocto_api import YRefParam, YAPI
from yoctolib.yocto_buzzer import YBuzzer
from yoctolib.yocto_colorledcluster import YColorLedCluster
from yoctolib.yocto_rfidreader import YRfidReader, YRfidStatus, YRfidOptions


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
    # retrieve any Relay
    sensor = YRfidReader.FirstRfidReader()
    if sensor is None:
        die('No Yocto-PowerRelay connected')
    target = sensor.get_serialNumber()

# retrieve specified functions
reader = YRfidReader.FindRfidReader(target + ".rfidReader")
led = YColorLedCluster.FindColorLedCluster(target + ".colorLedCluster")
button1 = YAnButton.FindAnButton(target + ".anButton1")
buzzer = YBuzzer.FindBuzzer(target + ".buzzer")

led.set_rgbColor(0, 1, 0x000000)
buzzer.set_volume(75)
print("Place a RFID tag near the Antenna")

tagList = []
while len(tagList) <= 0:
    YAPI.Sleep(250)
    tagList = reader.get_tagIdList()

tagId = tagList[0]
opStatus = YRfidStatus()
options = YRfidOptions()
taginfo = reader.get_tagInfo(tagId, opStatus)
blocksize = taginfo.get_tagBlockSize()
firstBlock = taginfo.get_tagFirstBlock()
print("Tag ID          = " + taginfo.get_tagId())
print("Tag Memory size = " + str(taginfo.get_tagMemorySize()) + " bytes")
print("Tag Block  size = " + str(taginfo.get_tagBlockSize()) + " bytes")

data = reader.tagReadHex(tagId, firstBlock, 3 * blocksize, options, opStatus)
if (opStatus.get_errorCode() == YRfidStatus.SUCCESS):
    print("First 3 blocks  = " + data)
    led.set_rgbColor(0, 1, 0x00FF00)
    buzzer.pulse(1000, 100)
else:
    print("Cannot read tag contents (" + opStatus.get_errorMessage() + ")")
    led.set_rgbColor(0, 1, 0xFF0000)

led.rgb_move(0, 1, 0x000000, 200)
YAPI.FreeAPI()
