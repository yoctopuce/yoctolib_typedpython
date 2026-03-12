import sys

from yoctolib.yocto_api import YRefParam, YAPI, xarray
from yoctolib.yocto_messagebox import YSms, YMessageBox


def die(msg: str) -> None:
    YAPI.FreeAPI()
    sys.exit(msg + ' (check USB cable)')

# callback that will be invoked when a new message is received
def smsCallback(msgBox: YMessageBox, sms: YSms):
    print('New message dated %s:' % sms.get_timestamp())
    print('  from %s' % sms.get_sender())
    print('  "%s"' % sms.get_textData())
    sms.deleteFromSIM()

# the API uses local USB devices through VirtualHub
errmsg: YRefParam = YRefParam()
print("Registerhub...")
if YAPI.RegisterHub("127.0.0.1", errmsg) != YAPI.SUCCESS:
    sys.exit("RegisterHub failed: " + errmsg.value)
print("Done")

target: str = 'any'
if len(sys.argv) > 1:
    target = sys.argv[1]

if target == 'any':
    # retrieve any filesystem
    mbox = YMessageBox.FirstMessageBox()
    if mbox is None:
        die('No module connected')
else:
    mbox = YMessageBox.FindMessageBox(target + ".messageBox")

if not mbox.isOnline():
    die("Module not connected ")

# list messages found on the device
print("Messages found on the SIM Card:")
messages: list[YSms] = mbox.get_messages()
if len(messages) == 0:
    print("  No messages found")
for sms in messages:
    print('- dated %s:' % sms.get_timestamp())
    print('  from %s' % sms.get_sender())
    print('  "%s"' % sms.get_textData())

# register a callback to receive any new message
mbox.registerSmsCallback(smsCallback)

# offer to send a new message
print("To test sending SMS, provide message recipient.")
print("To skip sending, leave empty and press Enter.")
number: str = input("Recipient number (+xxxxxxxxxx): ")
if number:
    # if that call fails, make sure that your SIM operator
    # allows you to send SMS given your current contract
    mbox.sendTextMessage(number, "Hello from YoctoHub-GSM !")

while True:
    print("Waiting to receive SMS, press Ctrl-C to quit.")
    YAPI.Sleep(5000)

YAPI.FreeAPI()
