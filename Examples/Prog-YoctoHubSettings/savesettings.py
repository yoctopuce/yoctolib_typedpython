import sys

from yoctolib.yocto_api import YRefParam, YAPI, YModule


def usage():
    sys.exit("usage: demo <serial or logical name> <new logical name>")


if len(sys.argv) != 3:
    usage()

# the API use local USB devices through VirtualHub
errmsg: YRefParam = YRefParam()
if YAPI.RegisterHub("localhost", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub failed: " + errmsg.value)

m: YModule = YModule.FindModule(sys.argv[1])  # use serial or logical name
if m.isOnline():
    newname: str = sys.argv[2]
    if not YAPI.CheckLogicalName(newname):
        sys.exit("Invalid name (" + newname + ")")
    m.set_logicalName(newname)
    m.saveToFlash()  # do not forget this
    print("Module: serial= " + m.get_serialNumber() + " / name= " + m.get_logicalName())
else:
    print("not connected (check identification and USB cable")
YAPI.FreeAPI()
