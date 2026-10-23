# ********************************************************************
#
#  $Id: inventory.py 76368 2026-10-14 11:12:27Z mvuilleu $
#
#  Doc-Inventory example
#
#  You can find more information on our web site:
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************

from yoctolib.yocto_api import YRefParam, YAPI, YModule

def main():
    errmsg = YRefParam()
    if YAPI.RegisterHub("localhost", errmsg) != YAPI.SUCCESS:
        print("YAPI.RegisterHub : " + str(errmsg))
        return

    print('Device list:')
    module = YModule.FirstModule()
    while module is not None:
        serial = module.get_serialNumber()
        product_name = module.get_productName()
        print(serial + ' (' + product_name + ')')
        module = module.nextModule()
    YAPI.FreeAPI()


if __name__ == '__main__':
    main()
