# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YDaisyChain
#
#  - - - - - - - - - License information: - - - - - - - - -
#
#  Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#
#  Yoctopuce Sarl (hereafter Licensor) grants to you a perpetual
#  non-exclusive license to use, modify, copy and integrate this
#  file into your software for the sole purpose of interfacing
#  with Yoctopuce products.
#
#  You may reproduce and distribute copies of this file in
#  source or object form, as long as the sole purpose of this
#  code is to interface with Yoctopuce products. You must retain
#  this notice in the distributed source file.
#
#  You should refer to Yoctopuce General Terms and Conditions
#  for additional information regarding your rights and
#  obligations.
#
#  THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#  WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING
#  WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#  EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#  INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA,
#  COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR
#  SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT
#  LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#  CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#  BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#  WARRANTY, OR OTHERWISE.
#
# *********************************************************************
"""
Yoctopuce library: Asyncio implementation of YDaisyChain
version: PATCH_WITH_VERSION
requires: yocto_api_aio
"""
from __future__ import annotations

import sys

# On MicroPython, code below will be wiped out at compile time
if sys.implementation.name != "micropython":
    # In CPython, enable edit-time type checking, including Final declaration
    from typing import Any, Union, Final
    from collections.abc import Callable, Awaitable
    from .yocto_api_aio import const, _IS_MICROPYTHON
else:
    # In our micropython VM, common generic types are global built-ins
    # Others such as TypeVar should be avoided when using micropython,
    # as they produce overhead in runtime code
    # Final is translated into const() expressions before compilation
    _IS_MICROPYTHON: Final[bool] = True # noqa

from .yocto_api_aio import (
    YAPIContext, YAPI, YAPI_Exception, HwId, hwid2str, YFunction
)

# --- (YDaisyChain class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YDaisyChainValueCallback = Union[Callable[['YDaisyChain', str], Awaitable[None]], None]
    except TypeError:
        YDaisyChainValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YDaisyChain(YFunction):
    """
    The YDaisyChain class can be used to verify that devices that
    are daisy-chained directly from device to device, without a hub,
    are detected properly.

    """
    # --- (end of YDaisyChain class start)
    if not _IS_MICROPYTHON:
        # --- (YDaisyChain return codes)
        CHILDCOUNT_INVALID: Final[int] = YAPI.INVALID_UINT
        REQUIREDCHILDCOUNT_INVALID: Final[int] = YAPI.INVALID_UINT
        DAISYSTATE_READY: Final[int] = 0
        DAISYSTATE_IS_CHILD: Final[int] = 1
        DAISYSTATE_FIRMWARE_MISMATCH: Final[int] = 2
        DAISYSTATE_CHILD_MISSING: Final[int] = 3
        DAISYSTATE_CHILD_LOST: Final[int] = 4
        DAISYSTATE_INVALID: Final[int] = -1
        # --- (end of YDaisyChain return codes)

    # --- (YDaisyChain attributes declaration)
    _daisyState: int
    _childCount: int
    _requiredChildCount: int
    _valueCallback: YDaisyChainValueCallback
    # --- (end of YDaisyChain attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'DaisyChain'
        # --- (YDaisyChain constructor)
        self._daisyState = YDaisyChain.DAISYSTATE_INVALID
        self._childCount = YDaisyChain.CHILDCOUNT_INVALID
        self._requiredChildCount = YDaisyChain.REQUIREDCHILDCOUNT_INVALID
        # --- (end of YDaisyChain constructor)

    # --- (YDaisyChain implementation)

    @staticmethod
    def FirstDaisyChain() -> Union[YDaisyChain, None]:
        """
        Starts the enumeration of module chains currently accessible.
        Use the method YDaisyChain.nextDaisyChain() to iterate on
        next module chains.

        @return a pointer to a YDaisyChain object, corresponding to
                the first module chain currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('DaisyChain')
        if not next_hwid:
            return None
        return YDaisyChain.FindDaisyChain(hwid2str(next_hwid))

    @staticmethod
    def FirstDaisyChainInContext(yctx: YAPIContext) -> Union[YDaisyChain, None]:
        """
        Starts the enumeration of module chains currently accessible.
        Use the method YDaisyChain.nextDaisyChain() to iterate on
        next module chains.

        @param yctx : a YAPI context.

        @return a pointer to a YDaisyChain object, corresponding to
                the first module chain currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('DaisyChain')
        if not next_hwid:
            return None
        return YDaisyChain.FindDaisyChainInContext(yctx, hwid2str(next_hwid))

    def nextDaisyChain(self):
        """
        Continues the enumeration of module chains started using yFirstDaisyChain().
        Caution: You can't make any assumption about the returned module chains order.
        If you want to find a specific a module chain, use DaisyChain.findDaisyChain()
        and a hardwareID or a logical name.

        @return a pointer to a YDaisyChain object, corresponding to
                a module chain currently online, or a None pointer
                if there are no more module chains to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YDaisyChain.FindDaisyChainInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'daisyState' in json_val:
            self._daisyState = json_val["daisyState"]
        if 'childCount' in json_val:
            self._childCount = json_val["childCount"]
        if 'requiredChildCount' in json_val:
            self._requiredChildCount = json_val["requiredChildCount"]
        super()._parseAttr(json_val)

    async def get_daisyState(self) -> int:
        """
        Returns the state of the daisy-link between modules.

        @return a value among YDaisyChain.DAISYSTATE_READY, YDaisyChain.DAISYSTATE_IS_CHILD,
        YDaisyChain.DAISYSTATE_FIRMWARE_MISMATCH, YDaisyChain.DAISYSTATE_CHILD_MISSING and
        YDaisyChain.DAISYSTATE_CHILD_LOST corresponding to the state of the daisy-link between modules

        On failure, throws an exception or returns YDaisyChain.DAISYSTATE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YDaisyChain.DAISYSTATE_INVALID
        res = self._daisyState
        return res

    async def get_childCount(self) -> int:
        """
        Returns the number of child nodes currently detected.

        @return an integer corresponding to the number of child nodes currently detected

        On failure, throws an exception or returns YDaisyChain.CHILDCOUNT_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YDaisyChain.CHILDCOUNT_INVALID
        res = self._childCount
        return res

    async def get_requiredChildCount(self) -> int:
        """
        Returns the number of child nodes expected in normal conditions.

        @return an integer corresponding to the number of child nodes expected in normal conditions

        On failure, throws an exception or returns YDaisyChain.REQUIREDCHILDCOUNT_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YDaisyChain.REQUIREDCHILDCOUNT_INVALID
        res = self._requiredChildCount
        return res

    async def set_requiredChildCount(self, newval: int) -> int:
        """
        Changes the number of child nodes expected in normal conditions.
        If the value is zero, no check is performed. If it is non-zero, the number
        child nodes is checked on startup and the status will change to error if
        the count does not match. Remember to call the saveToFlash()
        method of the module if the modification must be kept.

        @param newval : an integer corresponding to the number of child nodes expected in normal conditions

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("requiredChildCount", rest_val)

    @staticmethod
    def FindDaisyChain(func: str) -> YDaisyChain:
        """
        Retrieves a module chain for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the module chain is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YDaisyChain.isOnline() to test if the module chain is
        indeed online at a given time. In case of ambiguity when looking for
        a module chain by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the module chain, for instance
                MyDevice.daisyChain.

        @return a YDaisyChain object allowing you to drive the module chain.
        """
        obj: Union[YDaisyChain, None]
        obj = YFunction._FindFromCache("DaisyChain", func)
        if obj is None:
            obj = YDaisyChain(YAPI, func)
            YFunction._AddToCache("DaisyChain", func, obj)
        return obj

    @staticmethod
    def FindDaisyChainInContext(yctx: YAPIContext, func: str) -> YDaisyChain:
        """
        Retrieves a module chain for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the module chain is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YDaisyChain.isOnline() to test if the module chain is
        indeed online at a given time. In case of ambiguity when looking for
        a module chain by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the module chain, for instance
                MyDevice.daisyChain.

        @return a YDaisyChain object allowing you to drive the module chain.
        """
        obj: Union[YDaisyChain, None]
        obj = YFunction._FindFromCacheInContext(yctx, "DaisyChain", func)
        if obj is None:
            obj = YDaisyChain(yctx, func)
            YFunction._AddToCache("DaisyChain", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YDaisyChainValueCallback) -> int:
            """
            Registers the callback function that is invoked on every change of advertised value.
            The callback is invoked only during the execution of ySleep or yHandleEvents.
            This provides control over the time when the callback is triggered. For good responsiveness, remember to call
            one of these two functions periodically. To unregister a callback, pass a None pointer as argument.

            @param callback : the callback function to call, or a None pointer. The callback function should take two
                    arguments: the function object of which the value has changed, and the character string describing
                    the new advertised value.
            @noreturn
            """
            return await super().registerValueCallback(callback)

    # --- (end of YDaisyChain implementation)

