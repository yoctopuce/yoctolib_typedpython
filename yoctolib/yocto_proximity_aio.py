# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YProximity
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
Yoctopuce library: Asyncio implementation of YProximity
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

# --- (YProximity class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YProximityValueCallback = Union[Callable[['YProximity', str], Awaitable[None]], None]
        YProximityTimedReportCallback = Union[Callable[['YProximity', YMeasure], Awaitable[None]], None]
    except TypeError:
        YProximityValueCallback = Union[Callable, Awaitable]
        YProximityTimedReportCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YProximity(YSensor):
    """
    The YProximity class allows you to read and configure Yoctopuce proximity sensors.
    It inherits from YSensor class the core functions to read measures,
    to register callback functions, and to access the autonomous datalogger.
    This class adds the ability to set up a detection threshold and to count the
    number of detected state changes.

    """
    # --- (end of YProximity class start)
    if not _IS_MICROPYTHON:
        # --- (YProximity return codes)
        SIGNALVALUE_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        DETECTIONTHRESHOLD_INVALID: Final[int] = YAPI.INVALID_UINT
        DETECTIONHYSTERESIS_INVALID: Final[int] = YAPI.INVALID_UINT
        PRESENCEMINTIME_INVALID: Final[int] = YAPI.INVALID_UINT
        REMOVALMINTIME_INVALID: Final[int] = YAPI.INVALID_UINT
        LASTTIMEAPPROACHED_INVALID: Final[int] = YAPI.INVALID_LONG
        LASTTIMEREMOVED_INVALID: Final[int] = YAPI.INVALID_LONG
        PULSECOUNTER_INVALID: Final[int] = YAPI.INVALID_LONG
        PULSETIMER_INVALID: Final[int] = YAPI.INVALID_LONG
        ISPRESENT_FALSE: Final[int] = 0
        ISPRESENT_TRUE: Final[int] = 1
        ISPRESENT_INVALID: Final[int] = -1
        PROXIMITYREPORTMODE_NUMERIC: Final[int] = 0
        PROXIMITYREPORTMODE_PRESENCE: Final[int] = 1
        PROXIMITYREPORTMODE_PULSECOUNT: Final[int] = 2
        PROXIMITYREPORTMODE_INVALID: Final[int] = -1
        # --- (end of YProximity return codes)

    # --- (YProximity attributes declaration)
    _signalValue: float
    _detectionThreshold: int
    _detectionHysteresis: int
    _presenceMinTime: int
    _removalMinTime: int
    _isPresent: int
    _lastTimeApproached: int
    _lastTimeRemoved: int
    _pulseCounter: int
    _pulseTimer: int
    _proximityReportMode: int
    _valueCallback: YProximityValueCallback
    _timedReportCallback: YProximityTimedReportCallback
    # --- (end of YProximity attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'Proximity'
        # --- (YProximity constructor)
        self._signalValue = YProximity.SIGNALVALUE_INVALID
        self._detectionThreshold = YProximity.DETECTIONTHRESHOLD_INVALID
        self._detectionHysteresis = YProximity.DETECTIONHYSTERESIS_INVALID
        self._presenceMinTime = YProximity.PRESENCEMINTIME_INVALID
        self._removalMinTime = YProximity.REMOVALMINTIME_INVALID
        self._isPresent = YProximity.ISPRESENT_INVALID
        self._lastTimeApproached = YProximity.LASTTIMEAPPROACHED_INVALID
        self._lastTimeRemoved = YProximity.LASTTIMEREMOVED_INVALID
        self._pulseCounter = YProximity.PULSECOUNTER_INVALID
        self._pulseTimer = YProximity.PULSETIMER_INVALID
        self._proximityReportMode = YProximity.PROXIMITYREPORTMODE_INVALID
        # --- (end of YProximity constructor)

    # --- (YProximity implementation)

    @staticmethod
    def FirstProximity() -> Union[YProximity, None]:
        """
        Starts the enumeration of proximity sensors currently accessible.
        Use the method YProximity.nextProximity() to iterate on
        next proximity sensors.

        @return a pointer to a YProximity object, corresponding to
                the first proximity sensor currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('Proximity')
        if not next_hwid:
            return None
        return YProximity.FindProximity(hwid2str(next_hwid))

    @staticmethod
    def FirstProximityInContext(yctx: YAPIContext) -> Union[YProximity, None]:
        """
        Starts the enumeration of proximity sensors currently accessible.
        Use the method YProximity.nextProximity() to iterate on
        next proximity sensors.

        @param yctx : a YAPI context.

        @return a pointer to a YProximity object, corresponding to
                the first proximity sensor currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('Proximity')
        if not next_hwid:
            return None
        return YProximity.FindProximityInContext(yctx, hwid2str(next_hwid))

    def nextProximity(self):
        """
        Continues the enumeration of proximity sensors started using yFirstProximity().
        Caution: You can't make any assumption about the returned proximity sensors order.
        If you want to find a specific a proximity sensor, use Proximity.findProximity()
        and a hardwareID or a logical name.

        @return a pointer to a YProximity object, corresponding to
                a proximity sensor currently online, or a None pointer
                if there are no more proximity sensors to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YProximity.FindProximityInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'signalValue' in json_val:
            self._signalValue = round(json_val["signalValue"] / 65.536) / 1000.0
        if 'detectionThreshold' in json_val:
            self._detectionThreshold = json_val["detectionThreshold"]
        if 'detectionHysteresis' in json_val:
            self._detectionHysteresis = json_val["detectionHysteresis"]
        if 'presenceMinTime' in json_val:
            self._presenceMinTime = json_val["presenceMinTime"]
        if 'removalMinTime' in json_val:
            self._removalMinTime = json_val["removalMinTime"]
        if 'isPresent' in json_val:
            self._isPresent = json_val["isPresent"] > 0
        if 'lastTimeApproached' in json_val:
            self._lastTimeApproached = json_val["lastTimeApproached"]
        if 'lastTimeRemoved' in json_val:
            self._lastTimeRemoved = json_val["lastTimeRemoved"]
        if 'pulseCounter' in json_val:
            self._pulseCounter = json_val["pulseCounter"]
        if 'pulseTimer' in json_val:
            self._pulseTimer = json_val["pulseTimer"]
        if 'proximityReportMode' in json_val:
            self._proximityReportMode = json_val["proximityReportMode"]
        super()._parseAttr(json_val)

    async def get_signalValue(self) -> float:
        """
        Returns the current value of signal measured by the proximity sensor.

        @return a floating point number corresponding to the current value of signal measured by the proximity sensor

        On failure, throws an exception or returns YProximity.SIGNALVALUE_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.SIGNALVALUE_INVALID
        res = round(self._signalValue * 1000) / 1000
        return res

    async def get_detectionThreshold(self) -> int:
        """
        Returns the threshold used to determine the logical state of the proximity sensor, when considered
        as a binary input (on/off).

        @return an integer corresponding to the threshold used to determine the logical state of the
        proximity sensor, when considered
                as a binary input (on/off)

        On failure, throws an exception or returns YProximity.DETECTIONTHRESHOLD_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.DETECTIONTHRESHOLD_INVALID
        res = self._detectionThreshold
        return res

    async def set_detectionThreshold(self, newval: int) -> int:
        """
        Changes the threshold used to determine the logical state of the proximity sensor, when considered
        as a binary input (on/off).
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer corresponding to the threshold used to determine the logical state of
        the proximity sensor, when considered
                as a binary input (on/off)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("detectionThreshold", rest_val)

    async def get_detectionHysteresis(self) -> int:
        """
        Returns the hysteresis used to determine the logical state of the proximity sensor, when considered
        as a binary input (on/off).

        @return an integer corresponding to the hysteresis used to determine the logical state of the
        proximity sensor, when considered
                as a binary input (on/off)

        On failure, throws an exception or returns YProximity.DETECTIONHYSTERESIS_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.DETECTIONHYSTERESIS_INVALID
        res = self._detectionHysteresis
        return res

    async def set_detectionHysteresis(self, newval: int) -> int:
        """
        Changes the hysteresis used to determine the logical state of the proximity sensor, when considered
        as a binary input (on/off).
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer corresponding to the hysteresis used to determine the logical state of
        the proximity sensor, when considered
                as a binary input (on/off)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("detectionHysteresis", rest_val)

    async def get_presenceMinTime(self) -> int:
        """
        Returns the minimal detection duration before signalling a presence event. Any shorter detection is
        considered as noise or bounce (false positive) and filtered out.

        @return an integer corresponding to the minimal detection duration before signalling a presence event

        On failure, throws an exception or returns YProximity.PRESENCEMINTIME_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.PRESENCEMINTIME_INVALID
        res = self._presenceMinTime
        return res

    async def set_presenceMinTime(self, newval: int) -> int:
        """
        Changes the minimal detection duration before signalling a presence event. Any shorter detection is
        considered as noise or bounce (false positive) and filtered out.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer corresponding to the minimal detection duration before signalling a presence event

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("presenceMinTime", rest_val)

    async def get_removalMinTime(self) -> int:
        """
        Returns the minimal detection duration before signalling a removal event. Any shorter detection is
        considered as noise or bounce (false positive) and filtered out.

        @return an integer corresponding to the minimal detection duration before signalling a removal event

        On failure, throws an exception or returns YProximity.REMOVALMINTIME_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.REMOVALMINTIME_INVALID
        res = self._removalMinTime
        return res

    async def set_removalMinTime(self, newval: int) -> int:
        """
        Changes the minimal detection duration before signalling a removal event. Any shorter detection is
        considered as noise or bounce (false positive) and filtered out.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer corresponding to the minimal detection duration before signalling a removal event

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("removalMinTime", rest_val)

    async def get_isPresent(self) -> int:
        """
        Returns true if the input (considered as binary) is active (detection value is smaller than the
        specified threshold), and false otherwise.

        @return either YProximity.ISPRESENT_FALSE or YProximity.ISPRESENT_TRUE, according to true if the
        input (considered as binary) is active (detection value is smaller than the specified threshold),
        and false otherwise

        On failure, throws an exception or returns YProximity.ISPRESENT_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.ISPRESENT_INVALID
        res = self._isPresent
        return res

    async def get_lastTimeApproached(self) -> int:
        """
        Returns the number of elapsed milliseconds between the module power on and the last observed
        detection (the input contact transitioned from absent to present).

        @return an integer corresponding to the number of elapsed milliseconds between the module power on
        and the last observed
                detection (the input contact transitioned from absent to present)

        On failure, throws an exception or returns YProximity.LASTTIMEAPPROACHED_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.LASTTIMEAPPROACHED_INVALID
        res = self._lastTimeApproached
        return res

    async def get_lastTimeRemoved(self) -> int:
        """
        Returns the number of elapsed milliseconds between the module power on and the last observed
        detection (the input contact transitioned from present to absent).

        @return an integer corresponding to the number of elapsed milliseconds between the module power on
        and the last observed
                detection (the input contact transitioned from present to absent)

        On failure, throws an exception or returns YProximity.LASTTIMEREMOVED_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.LASTTIMEREMOVED_INVALID
        res = self._lastTimeRemoved
        return res

    async def get_pulseCounter(self) -> int:
        """
        Returns the pulse counter value. The value is a 32 bit integer. In case
        of overflow (>=2^32), the counter will wrap. To reset the counter, just
        call the resetCounter() method.

        @return an integer corresponding to the pulse counter value

        On failure, throws an exception or returns YProximity.PULSECOUNTER_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.PULSECOUNTER_INVALID
        res = self._pulseCounter
        return res

    async def set_pulseCounter(self, newval: int) -> int:
        rest_val = str(newval)
        return await self._setAttr("pulseCounter", rest_val)

    async def get_pulseTimer(self) -> int:
        """
        Returns the timer of the pulse counter (ms).

        @return an integer corresponding to the timer of the pulse counter (ms)

        On failure, throws an exception or returns YProximity.PULSETIMER_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.PULSETIMER_INVALID
        res = self._pulseTimer
        return res

    async def get_proximityReportMode(self) -> int:
        """
        Returns the parameter (sensor value, presence or pulse count) returned by the get_currentValue
        function and callbacks.

        @return a value among YProximity.PROXIMITYREPORTMODE_NUMERIC,
        YProximity.PROXIMITYREPORTMODE_PRESENCE and YProximity.PROXIMITYREPORTMODE_PULSECOUNT corresponding
        to the parameter (sensor value, presence or pulse count) returned by the get_currentValue function and callbacks

        On failure, throws an exception or returns YProximity.PROXIMITYREPORTMODE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YProximity.PROXIMITYREPORTMODE_INVALID
        res = self._proximityReportMode
        return res

    async def set_proximityReportMode(self, newval: int) -> int:
        """
        Changes the  parameter  type (sensor value, presence or pulse count) returned by the
        get_currentValue function and callbacks.
        The edge count value is limited to the 6 lowest digits. For values greater than one million, use
        get_pulseCounter().
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : a value among YProximity.PROXIMITYREPORTMODE_NUMERIC,
        YProximity.PROXIMITYREPORTMODE_PRESENCE and YProximity.PROXIMITYREPORTMODE_PULSECOUNT corresponding
        to the  parameter  type (sensor value, presence or pulse count) returned by the get_currentValue
        function and callbacks

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("proximityReportMode", rest_val)

    @staticmethod
    def FindProximity(func: str) -> YProximity:
        """
        Retrieves a proximity sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the proximity sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YProximity.isOnline() to test if the proximity sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a proximity sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the proximity sensor, for instance
                YPROXIM1.proximity1.

        @return a YProximity object allowing you to drive the proximity sensor.
        """
        obj: Union[YProximity, None]
        obj = YFunction._FindFromCache("Proximity", func)
        if obj is None:
            obj = YProximity(YAPI, func)
            YFunction._AddToCache("Proximity", func, obj)
        return obj

    @staticmethod
    def FindProximityInContext(yctx: YAPIContext, func: str) -> YProximity:
        """
        Retrieves a proximity sensor for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the proximity sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YProximity.isOnline() to test if the proximity sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a proximity sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the proximity sensor, for instance
                YPROXIM1.proximity1.

        @return a YProximity object allowing you to drive the proximity sensor.
        """
        obj: Union[YProximity, None]
        obj = YFunction._FindFromCacheInContext(yctx, "Proximity", func)
        if obj is None:
            obj = YProximity(yctx, func)
            YFunction._AddToCache("Proximity", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YProximityValueCallback) -> int:
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
        async def registerTimedReportCallback(self, callback: YProximityTimedReportCallback) -> int:
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

    async def resetCounter(self) -> int:
        """
        Resets the pulse counter value as well as its timer.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return await self.set_pulseCounter(0)

    # --- (end of YProximity implementation)

