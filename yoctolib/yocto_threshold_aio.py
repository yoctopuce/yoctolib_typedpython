# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YThreshold
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
Yoctopuce library: Asyncio implementation of YThreshold
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

# --- (YThreshold class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YThresholdValueCallback = Union[Callable[['YThreshold', str], Awaitable[None]], None]
    except TypeError:
        YThresholdValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YThreshold(YFunction):
    """
    The Threshold class allows you define a threshold on a Yoctopuce sensor
    to trigger a predefined action, on specific devices where this is implemented.

    """
    # --- (end of YThreshold class start)
    if not _IS_MICROPYTHON:
        # --- (YThreshold return codes)
        TARGETSENSOR_INVALID: Final[str] = YAPI.INVALID_STRING
        ALERTLEVEL_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        SAFELEVEL_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        THRESHOLDSTATE_SAFE: Final[int] = 0
        THRESHOLDSTATE_ALERT: Final[int] = 1
        THRESHOLDSTATE_INVALID: Final[int] = -1
        # --- (end of YThreshold return codes)

    # --- (YThreshold attributes declaration)
    _thresholdState: int
    _targetSensor: str
    _alertLevel: float
    _safeLevel: float
    _valueCallback: YThresholdValueCallback
    # --- (end of YThreshold attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'Threshold'
        # --- (YThreshold constructor)
        self._thresholdState = YThreshold.THRESHOLDSTATE_INVALID
        self._targetSensor = YThreshold.TARGETSENSOR_INVALID
        self._alertLevel = YThreshold.ALERTLEVEL_INVALID
        self._safeLevel = YThreshold.SAFELEVEL_INVALID
        # --- (end of YThreshold constructor)

    # --- (YThreshold implementation)

    @staticmethod
    def FirstThreshold() -> Union[YThreshold, None]:
        """
        Starts the enumeration of threshold functions currently accessible.
        Use the method YThreshold.nextThreshold() to iterate on
        next threshold functions.

        @return a pointer to a YThreshold object, corresponding to
                the first threshold function currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('Threshold')
        if not next_hwid:
            return None
        return YThreshold.FindThreshold(hwid2str(next_hwid))

    @staticmethod
    def FirstThresholdInContext(yctx: YAPIContext) -> Union[YThreshold, None]:
        """
        Starts the enumeration of threshold functions currently accessible.
        Use the method YThreshold.nextThreshold() to iterate on
        next threshold functions.

        @param yctx : a YAPI context.

        @return a pointer to a YThreshold object, corresponding to
                the first threshold function currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('Threshold')
        if not next_hwid:
            return None
        return YThreshold.FindThresholdInContext(yctx, hwid2str(next_hwid))

    def nextThreshold(self):
        """
        Continues the enumeration of threshold functions started using yFirstThreshold().
        Caution: You can't make any assumption about the returned threshold functions order.
        If you want to find a specific a threshold function, use Threshold.findThreshold()
        and a hardwareID or a logical name.

        @return a pointer to a YThreshold object, corresponding to
                a threshold function currently online, or a None pointer
                if there are no more threshold functions to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YThreshold.FindThresholdInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'thresholdState' in json_val:
            self._thresholdState = json_val["thresholdState"]
        if 'targetSensor' in json_val:
            self._targetSensor = json_val["targetSensor"]
        if 'alertLevel' in json_val:
            self._alertLevel = round(json_val["alertLevel"] / 65.536) / 1000.0
        if 'safeLevel' in json_val:
            self._safeLevel = round(json_val["safeLevel"] / 65.536) / 1000.0
        super()._parseAttr(json_val)

    async def get_thresholdState(self) -> int:
        """
        Returns current state of the threshold function.

        @return either YThreshold.THRESHOLDSTATE_SAFE or YThreshold.THRESHOLDSTATE_ALERT, according to
        current state of the threshold function

        On failure, throws an exception or returns YThreshold.THRESHOLDSTATE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.THRESHOLDSTATE_INVALID
        res = self._thresholdState
        return res

    async def get_targetSensor(self) -> str:
        """
        Returns the name of the sensor monitored by the threshold function.

        @return a string corresponding to the name of the sensor monitored by the threshold function

        On failure, throws an exception or returns YThreshold.TARGETSENSOR_INVALID.
        """
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.TARGETSENSOR_INVALID
        res = self._targetSensor
        return res

    async def set_alertLevel(self, newval: float) -> int:
        """
        Changes the sensor alert level triggering the threshold function.
        Remember to call the matching module saveToFlash()
        method if you want to preserve the setting after reboot.

        @param newval : a floating point number corresponding to the sensor alert level triggering the
        threshold function

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return await self._setAttr("alertLevel", rest_val)

    async def get_alertLevel(self) -> float:
        """
        Returns the sensor alert level, triggering the threshold function.

        @return a floating point number corresponding to the sensor alert level, triggering the threshold function

        On failure, throws an exception or returns YThreshold.ALERTLEVEL_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.ALERTLEVEL_INVALID
        res = self._alertLevel
        return res

    async def set_safeLevel(self, newval: float) -> int:
        """
        Changes the sensor acceptable level for disabling the threshold function.
        Remember to call the matching module saveToFlash()
        method if you want to preserve the setting after reboot.

        @param newval : a floating point number corresponding to the sensor acceptable level for disabling
        the threshold function

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return await self._setAttr("safeLevel", rest_val)

    async def get_safeLevel(self) -> float:
        """
        Returns the sensor acceptable level for disabling the threshold function.

        @return a floating point number corresponding to the sensor acceptable level for disabling the
        threshold function

        On failure, throws an exception or returns YThreshold.SAFELEVEL_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YThreshold.SAFELEVEL_INVALID
        res = self._safeLevel
        return res

    @staticmethod
    def FindThreshold(func: str) -> YThreshold:
        """
        Retrieves a threshold function for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the threshold function is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YThreshold.isOnline() to test if the threshold function is
        indeed online at a given time. In case of ambiguity when looking for
        a threshold function by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the threshold function, for instance
                MyDevice.threshold1.

        @return a YThreshold object allowing you to drive the threshold function.
        """
        obj: Union[YThreshold, None]
        obj = YFunction._FindFromCache("Threshold", func)
        if obj is None:
            obj = YThreshold(YAPI, func)
            YFunction._AddToCache("Threshold", func, obj)
        return obj

    @staticmethod
    def FindThresholdInContext(yctx: YAPIContext, func: str) -> YThreshold:
        """
        Retrieves a threshold function for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the threshold function is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YThreshold.isOnline() to test if the threshold function is
        indeed online at a given time. In case of ambiguity when looking for
        a threshold function by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the threshold function, for instance
                MyDevice.threshold1.

        @return a YThreshold object allowing you to drive the threshold function.
        """
        obj: Union[YThreshold, None]
        obj = YFunction._FindFromCacheInContext(yctx, "Threshold", func)
        if obj is None:
            obj = YThreshold(yctx, func)
            YFunction._AddToCache("Threshold", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YThresholdValueCallback) -> int:
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

    # --- (end of YThreshold implementation)

