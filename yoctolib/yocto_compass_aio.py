# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YCompass
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
Yoctopuce library: Asyncio implementation of YCompass
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
    YAPIContext, YAPI, YAPI_Exception, HwId, hwid2str, YFunction, YSensor, YMeasure
)

# --- (YCompass class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YCompassValueCallback = Union[Callable[['YCompass', str], Awaitable[None]], None]
        YCompassTimedReportCallback = Union[Callable[['YCompass', YMeasure], Awaitable[None]], None]
    except TypeError:
        YCompassValueCallback = Union[Callable, Awaitable]
        YCompassTimedReportCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YCompass(YSensor):
    """
    The YCompass class allows you to read and configure Yoctopuce compass functions.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    # --- (end of YCompass class start)
    if not _IS_MICROPYTHON:
        # --- (YCompass return codes)
        BANDWIDTH_INVALID: Final[int] = YAPI.INVALID_UINT
        MAGNETICHEADING_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        AXIS_X: Final[int] = 0
        AXIS_Y: Final[int] = 1
        AXIS_Z: Final[int] = 2
        AXIS_INVALID: Final[int] = -1
        # --- (end of YCompass return codes)

    # --- (YCompass attributes declaration)
    _bandwidth: int
    _axis: int
    _magneticHeading: float
    _valueCallback: YCompassValueCallback
    _timedReportCallback: YCompassTimedReportCallback
    # --- (end of YCompass attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'Compass'
        # --- (YCompass constructor)
        self._bandwidth = YCompass.BANDWIDTH_INVALID
        self._axis = YCompass.AXIS_INVALID
        self._magneticHeading = YCompass.MAGNETICHEADING_INVALID
        # --- (end of YCompass constructor)

    # --- (YCompass implementation)

    @staticmethod
    def FirstCompass() -> Union[YCompass, None]:
        """
        Starts the enumeration of compass functions currently accessible.
        Use the method YCompass.nextCompass() to iterate on
        next compass functions.

        @return a pointer to a YCompass object, corresponding to
                the first compass function currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('Compass')
        if not next_hwid:
            return None
        return YCompass.FindCompass(hwid2str(next_hwid))

    @staticmethod
    def FirstCompassInContext(yctx: YAPIContext) -> Union[YCompass, None]:
        """
        Starts the enumeration of compass functions currently accessible.
        Use the method YCompass.nextCompass() to iterate on
        next compass functions.

        @param yctx : a YAPI context.

        @return a pointer to a YCompass object, corresponding to
                the first compass function currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('Compass')
        if not next_hwid:
            return None
        return YCompass.FindCompassInContext(yctx, hwid2str(next_hwid))

    def nextCompass(self):
        """
        Continues the enumeration of compass functions started using yFirstCompass().
        Caution: You can't make any assumption about the returned compass functions order.
        If you want to find a specific a compass function, use Compass.findCompass()
        and a hardwareID or a logical name.

        @return a pointer to a YCompass object, corresponding to
                a compass function currently online, or a None pointer
                if there are no more compass functions to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YCompass.FindCompassInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'bandwidth' in json_val:
            self._bandwidth = json_val["bandwidth"]
        if 'axis' in json_val:
            self._axis = json_val["axis"]
        if 'magneticHeading' in json_val:
            self._magneticHeading = round(json_val["magneticHeading"] / 65.536) / 1000.0
        super()._parseAttr(json_val)

    async def get_bandwidth(self) -> int:
        """
        Returns the measure update frequency, measured in Hz.

        @return an integer corresponding to the measure update frequency, measured in Hz

        On failure, throws an exception or returns YCompass.BANDWIDTH_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YCompass.BANDWIDTH_INVALID
        res = self._bandwidth
        return res

    async def set_bandwidth(self, newval: int) -> int:
        """
        Changes the measure update frequency, measured in Hz. When the
        frequency is lower, the device performs averaging.
        Remember to call the saveToFlash()
        method of the module if the modification must be kept.

        @param newval : an integer corresponding to the measure update frequency, measured in Hz

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("bandwidth", rest_val)

    async def get_axis(self) -> int:
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YCompass.AXIS_INVALID
        res = self._axis
        return res

    async def get_magneticHeading(self) -> float:
        """
        Returns the magnetic heading, regardless of the configured bearing.

        @return a floating point number corresponding to the magnetic heading, regardless of the configured bearing

        On failure, throws an exception or returns YCompass.MAGNETICHEADING_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YCompass.MAGNETICHEADING_INVALID
        res = self._magneticHeading
        return res

    @staticmethod
    def FindCompass(func: str) -> YCompass:
        """
        Retrieves a compass function for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the compass function is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCompass.isOnline() to test if the compass function is
        indeed online at a given time. In case of ambiguity when looking for
        a compass function by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the compass function, for instance
                Y3DMK002.compass.

        @return a YCompass object allowing you to drive the compass function.
        """
        obj: Union[YCompass, None]
        obj = YFunction._FindFromCache("Compass", func)
        if obj is None:
            obj = YCompass(YAPI, func)
            YFunction._AddToCache("Compass", func, obj)
        return obj

    @staticmethod
    def FindCompassInContext(yctx: YAPIContext, func: str) -> YCompass:
        """
        Retrieves a compass function for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the compass function is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCompass.isOnline() to test if the compass function is
        indeed online at a given time. In case of ambiguity when looking for
        a compass function by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the compass function, for instance
                Y3DMK002.compass.

        @return a YCompass object allowing you to drive the compass function.
        """
        obj: Union[YCompass, None]
        obj = YFunction._FindFromCacheInContext(yctx, "Compass", func)
        if obj is None:
            obj = YCompass(yctx, func)
            YFunction._AddToCache("Compass", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YCompassValueCallback) -> int:
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

    if not _IS_MICROPYTHON:
        async def registerTimedReportCallback(self, callback: YCompassTimedReportCallback) -> int:
            """
            Registers the callback function that is invoked on every periodic timed notification.
            The callback is invoked only during the execution of ySleep or yHandleEvents.
            This provides control over the time when the callback is triggered. For good responsiveness, remember to call
            one of these two functions periodically. To unregister a callback, pass a None pointer as argument.

            @param callback : the callback function to call, or a None pointer. The callback function should take two
                    arguments: the function object of which the value has changed, and an YMeasure object describing
                    the new advertised value.
            @noreturn
            """
            return await super().registerTimedReportCallback(callback)

    # --- (end of YCompass implementation)

