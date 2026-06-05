# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YAirQuality
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
Yoctopuce library: High-level API for YAirQuality
version: PATCH_WITH_VERSION
requires: yocto_airquality_aio
requires: yocto_api
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
    _DYNAMIC_HELPERS = False
else:
    # In our micropython VM, common generic types are global built-ins
    # Others such as TypeVar should be avoided when using micropython,
    # as they produce overhead in runtime code
    # Final is translated into const() expressions before compilation
    _IS_MICROPYTHON: Final[bool] = True # noqa
    _DYNAMIC_HELPERS: Final[bool] = True # noqa

from .yocto_airquality_aio import YAirQuality as YAirQuality_aio
from .yocto_api import (
    YAPIContext, YAPI, YAPI_aio, YSensor, YMeasure
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
    _aio: YAirQuality_aio
    # --- (end of YAirQuality class start)
    if not _IS_MICROPYTHON:
        # --- (YAirQuality return codes)
        UBAINDEX_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        RELATIVEINDEX_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        AQIMODE_RELATIVE: Final[int] = 0
        AQIMODE_UBA: Final[int] = 1
        AQIMODE_INVALID: Final[int] = -1
        # --- (end of YAirQuality return codes)


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
        return cls._proxy(cls, YAirQuality_aio.FindAirQualityInContext(YAPI_aio, func))

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
        return cls._proxy(cls, YAirQuality_aio.FindAirQualityInContext(yctx._aio, func))

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
        return cls._proxy(cls, YAirQuality_aio.FirstAirQualityInContext(YAPI_aio))

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
        return cls._proxy(cls, YAirQuality_aio.FirstAirQualityInContext(yctx._aio))

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
        return self._proxy(type(self), self._aio.nextAirQuality())

    if not _DYNAMIC_HELPERS:
        def get_ubaIndex(self) -> float:
            """
            Returns the current air quality index, according to UBA (from 1 to 5).

            @return a floating point number corresponding to the current air quality index, according to UBA (from 1 to 5)

            On failure, throws an exception or returns YAirQuality.UBAINDEX_INVALID.
            """
            return self._run(self._aio.get_ubaIndex())

    if not _DYNAMIC_HELPERS:
        def get_relativeIndex(self) -> float:
            """
            Returns the relative air quality index, according to ScioSense (from 0 to 500).
            A value below 100 indicates better-than-average air quality compared to the past 24 hours,
            while a value above 100 indicates poorer-than-average air quality compared to the past 24 hours.

            @return a floating point number corresponding to the relative air quality index, according to
            ScioSense (from 0 to 500)

            On failure, throws an exception or returns YAirQuality.RELATIVEINDEX_INVALID.
            """
            return self._run(self._aio.get_relativeIndex())

    if not _DYNAMIC_HELPERS:
        def get_aqiMode(self) -> int:
            """
            Returns the type of index reported by the get_currentValue function and callbacks (UBA index or relative index).

            @return either YAirQuality.AQIMODE_RELATIVE or YAirQuality.AQIMODE_UBA, according to the type of
            index reported by the get_currentValue function and callbacks (UBA index or relative index)

            On failure, throws an exception or returns YAirQuality.AQIMODE_INVALID.
            """
            return self._run(self._aio.get_aqiMode())

    if not _DYNAMIC_HELPERS:
        def set_aqiMode(self, newval: int) -> int:
            """
            Changes the the type of index reported by the get_currentValue function and callbacks (UBA index or
            relative index).
            Remember to call the saveToFlash() method of the module if the modification must be kept.

            @param newval : either YAirQuality.AQIMODE_RELATIVE or YAirQuality.AQIMODE_UBA, according to the
            the type of index reported by the get_currentValue function and callbacks (UBA index or relative index)

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_aqiMode(newval))

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YAirQualityValueCallback) -> int:
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
            return super().registerValueCallback(callback)

    if not _IS_MICROPYTHON:
        def registerTimedReportCallback(self, callback: YAirQualityTimedReportCallback) -> int:
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
            return super().registerTimedReportCallback(callback)

    # --- (end of YAirQuality implementation)

