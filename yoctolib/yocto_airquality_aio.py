# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YAirQuality
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
Yoctopuce library: Asyncio implementation of YAirQuality
version: PATCH_WITH_VERSION
requires: yocto_api_aio
provides: YAirQuality
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

# --- (YAirQuality class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YAirQualityValueCallback = Union[Callable[['YAirQuality', str], Any], None]
        YAirQualityTimedReportCallback = Union[Callable[['YAirQuality', YMeasure], Any], None]
    except TypeError:
        YAirQualityValueCallback = Union[Callable, Awaitable]
        YAirQualityTimedReportCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YAirQuality(YSensor):
    """
    The YAirQuality class allows you to read and configure Yoctopuce air quality sensors.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    # --- (end of YAirQuality class start)
    if not _IS_MICROPYTHON:
        # --- (YAirQuality return codes)
        UBAINDEX_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        RELATIVEINDEX_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        AQIMODE_RELATIVE: Final[int] = 0
        AQIMODE_UBA: Final[int] = 1
        AQIMODE_INVALID: Final[int] = -1
        # --- (end of YAirQuality return codes)

    # --- (YAirQuality attributes declaration)
    _valueCallback: YAirQualityValueCallback
    _timedReportCallback: YAirQualityTimedReportCallback
    # --- (end of YAirQuality attributes declaration)

    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, 'AirQuality', func)
        # --- (YAirQuality constructor)
        # --- (end of YAirQuality constructor)

    # --- (YAirQuality implementation)
    @classmethod
    def FindAirQuality(cls, func: str) -> YAirQuality:
        """
        Retrieves a air quality sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the air quality sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YAirQuality.isOnline() to test if the air quality sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a air quality sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the air quality sensor, for instance
                MyDevice.airQuality.

        @return a YAirQuality object allowing you to drive the air quality sensor.
        """
        return cls.FindAirQualityInContext(YAPI, func)

    @classmethod
    def FindAirQualityInContext(cls, yctx: YAPIContext, func: str) -> YAirQuality:
        """
        Retrieves a air quality sensor for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the air quality sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YAirQuality.isOnline() to test if the air quality sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a air quality sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the air quality sensor, for instance
                MyDevice.airQuality.

        @return a YAirQuality object allowing you to drive the air quality sensor.
        """
        obj: Union[YAirQuality, None] = yctx._findInCache('AirQuality', func)
        if obj:
            return obj
        return YAirQuality(yctx, func)

    @classmethod
    def FirstAirQuality(cls) -> Union[YAirQuality, None]:
        """
        Starts the enumeration of air quality sensors currently accessible.
        Use the method YAirQuality.nextAirQuality() to iterate on
        next air quality sensors.

        @return a pointer to a YAirQuality object, corresponding to
                the first air quality sensor currently online, or a None pointer
                if there are none.
        """
        return cls.FirstAirQualityInContext(YAPI)

    @classmethod
    def FirstAirQualityInContext(cls, yctx: YAPIContext) -> Union[YAirQuality, None]:
        """
        Starts the enumeration of air quality sensors currently accessible.
        Use the method YAirQuality.nextAirQuality() to iterate on
        next air quality sensors.

        @param yctx : a YAPI context.

        @return a pointer to a YAirQuality object, corresponding to
                the first air quality sensor currently online, or a None pointer
                if there are none.
        """
        hwid: Union[HwId, None] = yctx._firstHwId('AirQuality')
        if hwid:
            return cls.FindAirQualityInContext(yctx, hwid2str(hwid))
        return None

    def nextAirQuality(self) -> Union[YAirQuality, None]:
        """
        Continues the enumeration of air quality sensors started using yFirstAirQuality().
        Caution: You can't make any assumption about the returned air quality sensors order.
        If you want to find a specific a air quality sensor, use AirQuality.findAirQuality()
        and a hardwareID or a logical name.

        @return a pointer to a YAirQuality object, corresponding to
                a air quality sensor currently online, or a None pointer
                if there are no more air quality sensors to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            next_hwid = self._yapi._nextHwId('AirQuality', self.get_hwId())
        except YAPI_Exception:
            pass
        if next_hwid:
            return self.FindAirQualityInContext(self._yapi, hwid2str(next_hwid))
        return None

    async def get_ubaIndex(self) -> float:
        """
        Returns the current air quality index, according to UBA (from 1 to 5).

        @return a floating point number corresponding to the current air quality index, according to UBA (from 1 to 5)

        On failure, throws an exception or returns YAirQuality.UBAINDEX_INVALID.
        """
        json_val: Union[float, None] = await self._fromCache("ubaIndex")
        if json_val is None:
            return YAirQuality.UBAINDEX_INVALID
        return round(json_val / 65.536) / 1000.0

    async def get_relativeIndex(self) -> float:
        """
        Returns the relative air quality index, according to ScioSense (from 0 to 500).
        A value below 100 indicates better-than-average air quality compared to the past 24 hours,
        while a value above 100 indicates poorer-than-average air quality compared to the past 24 hours.

        @return a floating point number corresponding to the relative air quality index, according to
        ScioSense (from 0 to 500)

        On failure, throws an exception or returns YAirQuality.RELATIVEINDEX_INVALID.
        """
        json_val: Union[float, None] = await self._fromCache("relativeIndex")
        if json_val is None:
            return YAirQuality.RELATIVEINDEX_INVALID
        return round(json_val / 65.536) / 1000.0

    async def get_aqiMode(self) -> int:
        """
        Returns the type of index reported by the get_currentValue function and callbacks (UBA index or relative index).

        @return either YAirQuality.AQIMODE_RELATIVE or YAirQuality.AQIMODE_UBA, according to the type of
        index reported by the get_currentValue function and callbacks (UBA index or relative index)

        On failure, throws an exception or returns YAirQuality.AQIMODE_INVALID.
        """
        json_val: Union[int, None] = await self._fromCache("aqiMode")
        if json_val is None:
            return YAirQuality.AQIMODE_INVALID
        return json_val

    async def set_aqiMode(self, newval: int) -> int:
        """
        Changes the the type of index reported by the get_currentValue function and callbacks (UBA index or
        relative index).
        Remember to call the saveToFlash() method of the module if the modification must be kept.

        @param newval : either YAirQuality.AQIMODE_RELATIVE or YAirQuality.AQIMODE_UBA, according to the
        the type of index reported by the get_currentValue function and callbacks (UBA index or relative index)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("aqiMode", rest_val)

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YAirQualityValueCallback) -> int:
            """
            Registers the callback function that is invoked on every change of advertised value.
            The callback is then invoked only during the execution of ySleep or yHandleEvents.
            This provides control over the time when the callback is triggered. For good responsiveness,
            remember to call one of these two functions periodically. The callback is called once juste after beeing
            registered, passing the current advertised value  of the function, provided that it is not an empty string.
            To unregister a callback, pass a None pointer as argument.

            @param callback : the callback function to call, or a None pointer. The callback function should take two
                    arguments: the function object of which the value has changed, and the character string describing
                    the new advertised value.
            @noreturn
            """
            return await super().registerValueCallback(callback)

    if not _IS_MICROPYTHON:
        async def registerTimedReportCallback(self, callback: YAirQualityTimedReportCallback) -> int:
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

    # --- (end of YAirQuality implementation)

