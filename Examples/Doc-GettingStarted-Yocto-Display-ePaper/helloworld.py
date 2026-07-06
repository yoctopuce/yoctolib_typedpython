# ********************************************************************
#
#  $Id: helloworld.py 75069 2026-07-02 16:41:18Z martinm $
#
#  An example that shows how to use a  Yocto-Display-ePaper
#
#  You can find more information on our web site:
#   Yocto-Display-ePaper documentation:
#      https://www.yoctopuce.com/EN/products/yocto-display-epaper/doc.html
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************

import sys
import random

from yoctolib.yocto_api import YRefParam, YAPI
from yoctolib.yocto_display import YDisplay, YDisplayLayer


def die(msg: str) -> None:
    YAPI.FreeAPI()
    sys.exit(msg + ' (check USB cable)')

colors  = [0xFFFFFF,0x000000, 0xFF0000, 0xFFFF00 ]

# the API use local USB devices through VirtualHub
errmsg: YRefParam = YRefParam()
if YAPI.RegisterHub("127.0.0.1", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub failed: " + errmsg.value)

# To use a specific device, invoke the script as
#   python helloworld.py [serial_number]
# or
#   python helloworld.py [logical_name]
target: str = 'any'
if len(sys.argv) > 1:
    target = sys.argv[1]

if target == 'any':
    # retrieve any display
    tmp: YDisplay = YDisplay.FirstDisplay()
    if tmp is None:
        die('No module connected')
    target = tmp.get_serialNumber()

# retrieve specified functions
disp = YDisplay.FindDisplay(target + ".display")
if not disp.isOnline():
    die("Yocto-Display '%s' not connected" % target)

# Makes sure the Panel type is set
paneltype:str = disp.get_displayPanel()
if paneltype=="NOT_SET" :
  print("Use the virtual to Configure the panel first")
  exit()

# retrieve the display size
w: int = disp.get_displayWidth()
h: int = disp.get_displayHeight()
middleX : int = int(w/2)
middleY : int = int(h/2)
print("Using device %s (panel: %s %dx%d pixels)" % (disp.get_serialNumber(),paneltype,w,h) )
disp.resetAll()

# retrieve the first layer
l0: YDisplayLayer = disp.get_displayLayer(0)
l0.selectFont("medium.yfm")

# makes sure the next refresh will be a full one
disp.regenerateDisplay()

animation   : bool = True
while animation:
  # prevent refreshing for 2 sec
  disp.postponeRefresh(2000)
  l0.clear()
  ## draw a few circle
  for i in range(15):
     cx : int =  random.randint(0,w)
     cy : int =  random.randint(0,h)
     r  : int =  random.randint(int(h/20),int(h/10))
     l0.selectFillColor(colors[random.randint(0,3)])
     l0.drawDisc(cx, cy, r)
     l0.drawCircle(cx,cy,r)
  # draw a rectangle with panel type in it
  l0.selectFillColor(0xffffff)
  l0.drawBar(middleX-75,middleY-10,middleX+75,middleY+12 )
  l0.drawRect(middleX-75,middleY-10,middleX+75,middleY+12 )
  l0.drawText(middleX,middleY,YDisplayLayer.ALIGN.CENTER,paneltype)  
  disp.triggerRefresh() # display is allowed to refresh  again
  YAPI.Sleep(1000)
  # if no fast refresh available, don't even try to run animations
  if (paneltype.find("KS")<0) : animation=False

YAPI.FreeAPI()
