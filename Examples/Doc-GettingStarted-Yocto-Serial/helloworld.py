# ********************************************************************
#
#  $Id: helloworld.py 66453 2025-05-09 10:25:49Z seb $
#
#  An example that shows how to use a  Yocto-Serial
#
#  You can find more information on our web site:
#   Yocto-Serial documentation:
#      https://www.yoctopuce.com/EN/products/yocto-serial/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************
import sys

from yoctolib.yocto_api import YRefParam, YAPI
from yoctolib.yocto_serialport import YSerialPort


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
    # retrieve any serial port
    sensor: YSerialPort = YSerialPort.FirstSerialPort()
    if sensor is None:
        die('No module connected')
    target = sensor.get_serialNumber()

serialPort: YSerialPort = YSerialPort.FindSerialPort(sys.argv[1] + ".serialPort")
if serialPort is None:
    die('No module connected (check cable)')

serialPort.set_serialMode("9600,8N1")
serialPort.set_protocol("Line")
serialPort.reset()

print("****************************")
print("* make sure voltage levels *")
print("* are properly configured  *")
print("****************************")
while True:
    print("Type line to send, or Ctrl-C to exit:")
    line: str = input(": ")
    if line == "":
        break
    serialPort.writeLine(line)
    YAPI.Sleep(500)
    line = serialPort.readLine()
    if line != "":
        print("Received: " + line)
YAPI.FreeAPI()
