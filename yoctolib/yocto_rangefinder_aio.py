# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YRangeFinder
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
Yoctopuce library: Asyncio implementation of YRangeFinder
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
    const = lambda obj: obj
    _IS_MICROPYTHON = False
else:
    # In our micropython VM, common generic types are global built-ins
    # Others such as TypeVar should be avoided when using micropython,
    # as they produce overhead in runtime code
    # Final is translated into const() expressions before compilation
    _IS_MICROPYTHON: Final[bool] = True # noqa

from .yocto_api_aio import (
    YAPIContext, YAPI, YAPI_Exception, HwId, hwid2str, YFunction, YSensor, YMeasure
)

# --- (YRangeFinder class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YRangeFinderValueCallback = Union[Callable[['YRangeFinder', str], Any], None]
        YRangeFinderTimedReportCallback = Union[Callable[['YRangeFinder', YMeasure], Any], None]
    except TypeError:
        YRangeFinderValueCallback = Union[Callable, Awaitable]
        YRangeFinderTimedReportCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YRangeFinder(YSensor):
    """
    The YRangeFinder class allows you to read and configure Yoctopuce range finders.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.
    This class adds the ability to easily perform a one-point linear calibration
    to compensate the effect of a glass or filter placed in front of the sensor.

    """
    # --- (end of YRangeFinder class start)
    if not _IS_MICROPYTHON:
        # --- (YRangeFinder return codes)
        TIMEFRAME_INVALID: Final[int] = YAPI.INVALID_LONG
        QUALITY_INVALID: Final[int] = YAPI.INVALID_UINT
        HARDWARECALIBRATION_INVALID: Final[str] = YAPI.INVALID_STRING
        CURRENTTEMPERATURE_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        COMMAND_INVALID: Final[str] = YAPI.INVALID_STRING
        RANGEFINDERMODE_DEFAULT: Final[int] = 0
        RANGEFINDERMODE_LONG_RANGE: Final[int] = 1
        RANGEFINDERMODE_HIGH_ACCURACY: Final[int] = 2
        RANGEFINDERMODE_HIGH_SPEED: Final[int] = 3
        RANGEFINDERMODE_INVALID: Final[int] = -1
        # --- (end of YRangeFinder return codes)

    # --- (YRangeFinder attributes declaration)
    _rangeFinderMode: int
    _timeFrame: int
    _quality: int
    _hardwareCalibration: str
    _currentTemperature: float
    _command: str
    _valueCallback: YRangeFinderValueCallback
    _timedReportCallback: YRangeFinderTimedReportCallback
    # --- (end of YRangeFinder attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'RangeFinder'
        # --- (YRangeFinder constructor)
        self._rangeFinderMode = YRangeFinder.RANGEFINDERMODE_INVALID
        self._timeFrame = YRangeFinder.TIMEFRAME_INVALID
        self._quality = YRangeFinder.QUALITY_INVALID
        self._hardwareCalibration = YRangeFinder.HARDWARECALIBRATION_INVALID
        self._currentTemperature = YRangeFinder.CURRENTTEMPERATURE_INVALID
        self._command = YRangeFinder.COMMAND_INVALID
        # --- (end of YRangeFinder constructor)

    # --- (YRangeFinder implementation)

    @staticmethod
    def FirstRangeFinder() -> Union[YRangeFinder, None]:
        """
        Starts the enumeration of range finders currently accessible.
        Use the method YRangeFinder.nextRangeFinder() to iterate on
        next range finders.

        @return a pointer to a YRangeFinder object, corresponding to
                the first range finder currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('RangeFinder')
        if not next_hwid:
            return None
        return YRangeFinder.FindRangeFinder(hwid2str(next_hwid))

    @staticmethod
    def FirstRangeFinderInContext(yctx: YAPIContext) -> Union[YRangeFinder, None]:
        """
        Starts the enumeration of range finders currently accessible.
        Use the method YRangeFinder.nextRangeFinder() to iterate on
        next range finders.

        @param yctx : a YAPI context.

        @return a pointer to a YRangeFinder object, corresponding to
                the first range finder currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('RangeFinder')
        if not next_hwid:
            return None
        return YRangeFinder.FindRangeFinderInContext(yctx, hwid2str(next_hwid))

    def nextRangeFinder(self):
        """
        Continues the enumeration of range finders started using yFirstRangeFinder().
        Caution: You can't make any assumption about the returned range finders order.
        If you want to find a specific a range finder, use RangeFinder.findRangeFinder()
        and a hardwareID or a logical name.

        @return a pointer to a YRangeFinder object, corresponding to
                a range finder currently online, or a None pointer
                if there are no more range finders to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YRangeFinder.FindRangeFinderInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'rangeFinderMode' in json_val:
            self._rangeFinderMode = json_val["rangeFinderMode"]
        if 'timeFrame' in json_val:
            self._timeFrame = json_val["timeFrame"]
        if 'quality' in json_val:
            self._quality = json_val["quality"]
        if 'hardwareCalibration' in json_val:
            self._hardwareCalibration = json_val["hardwareCalibration"]
        if 'currentTemperature' in json_val:
            self._currentTemperature = round(json_val["currentTemperature"] / 65.536) / 1000.0
        if 'command' in json_val:
            self._command = json_val["command"]
        super()._parseAttr(json_val)

    async def set_unit(self, newval: str) -> int:
        """
        Changes the measuring unit for the measured range. That unit is a string.
        String value can be " or mm. Any other value is ignored.
        Remember to call the saveToFlash() method of the module if the modification must be kept.
        WARNING: if a specific calibration is defined for the rangeFinder function, a
        unit system change will probably break it.

        @param newval : a string corresponding to the measuring unit for the measured range

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return await self._setAttr("unit", rest_val)

    async def get_rangeFinderMode(self) -> int:
        """
        Returns the range finder running mode. The rangefinder running mode
        allows you to put priority on precision, speed or maximum range.

        @return a value among YRangeFinder.RANGEFINDERMODE_DEFAULT,
        YRangeFinder.RANGEFINDERMODE_LONG_RANGE, YRangeFinder.RANGEFINDERMODE_HIGH_ACCURACY and
        YRangeFinder.RANGEFINDERMODE_HIGH_SPEED corresponding to the range finder running mode

        On failure, throws an exception or returns YRangeFinder.RANGEFINDERMODE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRangeFinder.RANGEFINDERMODE_INVALID
        res = self._rangeFinderMode
        return res

    async def set_rangeFinderMode(self, newval: int) -> int:
        """
        Changes the rangefinder running mode, allowing you to put priority on
        precision, speed or maximum range.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : a value among YRangeFinder.RANGEFINDERMODE_DEFAULT,
        YRangeFinder.RANGEFINDERMODE_LONG_RANGE, YRangeFinder.RANGEFINDERMODE_HIGH_ACCURACY and
        YRangeFinder.RANGEFINDERMODE_HIGH_SPEED corresponding to the rangefinder running mode, allowing you
        to put priority on
                precision, speed or maximum range

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("rangeFinderMode", rest_val)

    async def get_timeFrame(self) -> int:
        """
        Returns the time frame used to measure the distance and estimate the measure
        reliability. The time frame is expressed in milliseconds.

        @return an integer corresponding to the time frame used to measure the distance and estimate the measure
                reliability

        On failure, throws an exception or returns YRangeFinder.TIMEFRAME_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRangeFinder.TIMEFRAME_INVALID
        res = self._timeFrame
        return res

    async def set_timeFrame(self, newval: int) -> int:
        """
        Changes the time frame used to measure the distance and estimate the measure
        reliability. The time frame is expressed in milliseconds. A larger timeframe
        improves stability and reliability, at the cost of higher latency, but prevents
        the detection of events shorter than the time frame.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : an integer corresponding to the time frame used to measure the distance and estimate the measure
                reliability

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("timeFrame", rest_val)

    async def get_quality(self) -> int:
        """
        Returns a measure quality estimate, based on measured dispersion.

        @return an integer corresponding to a measure quality estimate, based on measured dispersion

        On failure, throws an exception or returns YRangeFinder.QUALITY_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRangeFinder.QUALITY_INVALID
        res = self._quality
        return res

    async def get_hardwareCalibration(self) -> str:
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRangeFinder.HARDWARECALIBRATION_INVALID
        res = self._hardwareCalibration
        return res

    async def set_hardwareCalibration(self, newval: str) -> int:
        rest_val = newval
        return await self._setAttr("hardwareCalibration", rest_val)

    async def get_currentTemperature(self) -> float:
        """
        Returns the current sensor temperature, as a floating point number.

        @return a floating point number corresponding to the current sensor temperature, as a floating point number

        On failure, throws an exception or returns YRangeFinder.CURRENTTEMPERATURE_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRangeFinder.CURRENTTEMPERATURE_INVALID
        res = self._currentTemperature
        return res

    async def get_command(self) -> str:
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRangeFinder.COMMAND_INVALID
        res = self._command
        return res

    async def set_command(self, newval: str) -> int:
        rest_val = newval
        return await self._setAttr("command", rest_val)

    @staticmethod
    def FindRangeFinder(func: str) -> YRangeFinder:
        """
        Retrieves a range finder for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the range finder is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRangeFinder.isOnline() to test if the range finder is
        indeed online at a given time. In case of ambiguity when looking for
        a range finder by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the range finder, for instance
                YRNGFND1.rangeFinder1.

        @return a YRangeFinder object allowing you to drive the range finder.
        """
        obj: Union[YRangeFinder, None]
        obj = YFunction._FindFromCache("RangeFinder", func)
        if obj is None:
            obj = YRangeFinder(YAPI, func)
            YFunction._AddToCache("RangeFinder", func, obj)
        return obj

    @staticmethod
    def FindRangeFinderInContext(yctx: YAPIContext, func: str) -> YRangeFinder:
        """
        Retrieves a range finder for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the range finder is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRangeFinder.isOnline() to test if the range finder is
        indeed online at a given time. In case of ambiguity when looking for
        a range finder by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the range finder, for instance
                YRNGFND1.rangeFinder1.

        @return a YRangeFinder object allowing you to drive the range finder.
        """
        obj: Union[YRangeFinder, None]
        obj = YFunction._FindFromCacheInContext(yctx, "RangeFinder", func)
        if obj is None:
            obj = YRangeFinder(yctx, func)
            YFunction._AddToCache("RangeFinder", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YRangeFinderValueCallback) -> int:
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
        async def registerTimedReportCallback(self, callback: YRangeFinderTimedReportCallback) -> int:
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

    async def get_hardwareCalibrationTemperature(self) -> float:
        """
        Returns the temperature at the time when the latest calibration was performed.
        This function can be used to determine if a new calibration for ambient temperature
        is required.

        @return a temperature, as a floating point number.
                On failure, throws an exception or return YAPI.INVALID_DOUBLE.
        """
        hwcal: str
        hwcal = await self.get_hardwareCalibration()
        if not (hwcal[0: 0 + 1] == "@"):
            return YAPI.INVALID_DOUBLE
        return YAPI._atoi(hwcal[1: 1 + len(hwcal)])

    async def triggerTemperatureCalibration(self) -> int:
        """
        Triggers a sensor calibration according to the current ambient temperature. That
        calibration process needs no physical interaction with the sensor. It is performed
        automatically at device startup, but it is recommended to start it again when the
        temperature delta since the latest calibration exceeds 8 degrees Celsius.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("T")

    async def triggerSpadCalibration(self) -> int:
        """
        Triggers the photon detector hardware calibration.
        This function is part of the calibration procedure to compensate for the effect
        of a cover glass. Make sure to read the chapter about hardware calibration for details
        on the calibration procedure for proper results.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("S")

    async def triggerOffsetCalibration(self, targetDist: float) -> int:
        """
        Triggers the hardware offset calibration of the distance sensor.
        This function is part of the calibration procedure to compensate for the the effect
        of a cover glass. Make sure to read the chapter about hardware calibration for details
        on the calibration procedure for proper results.

        @param targetDist : true distance of the calibration target, in mm or inches, depending
                on the unit selected in the device

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        distmm: int
        if await self.get_unit() == "\"":
            distmm = int(round(targetDist * 25.4))
        else:
            distmm = int(round(targetDist))
        return await self.set_command("O%d" % distmm)

    async def triggerXTalkCalibration(self, targetDist: float) -> int:
        """
        Triggers the hardware cross-talk calibration of the distance sensor.
        This function is part of the calibration procedure to compensate for the effect
        of a cover glass. Make sure to read the chapter about hardware calibration for details
        on the calibration procedure for proper results.

        @param targetDist : true distance of the calibration target, in mm or inches, depending
                on the unit selected in the device

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        distmm: int
        if await self.get_unit() == "\"":
            distmm = int(round(targetDist * 25.4))
        else:
            distmm = int(round(targetDist))
        return await self.set_command("X%d" % distmm)

    async def cancelCoverGlassCalibrations(self) -> int:
        """
        Cancels the effect of previous hardware calibration procedures to compensate
        for cover glass, and restores factory settings.
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_hardwareCalibration("")

    # --- (end of YRangeFinder implementation)

