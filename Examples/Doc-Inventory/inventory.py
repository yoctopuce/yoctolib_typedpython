# ********************************************************************
#
#  $Id: inventory.py 72944 2026-04-24 08:06:03Z seb $
#
#  Doc-Inventory example
#
#  You can find more information on our web site:
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************

# ********************************************************************
#
#  $Id: inventory.py 72944 2026-04-24 08:06:03Z seb $
#
#  Doc-Inventory example
#
#  You can find more information on our web site:
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************
"""
Yoctopuce library: 
version: PATCH_WITH_VERSION
# ********************************************************************
#
#  $Id: inventory.py 72944 2026-04-24 08:06:03Z seb $
#
#  Doc-Inventory example
#
#  You can find more information on our web site:
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************
"""
Yoctopuce library: 
version: PATCH_WITH_VERSION
# ********************************************************************
#
#  $Id: inventory.py 72944 2026-04-24 08:06:03Z seb $
#
#  Doc-Inventory example
#
#  You can find more information on our web site:
#   Typed Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-typedpython-EN.html
#
# *********************************************************************
"""
Yoctopuce library: 
version: PATCH_WITH_VERSION
# ********************************************************************
#
#  $Id: inventory.py 72944 2026-04-24 08:06:03Z seb $
#
#  Doc-Inventory example
#
#  You can find more information on our web site:
#   Python V2 API Reference:
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
