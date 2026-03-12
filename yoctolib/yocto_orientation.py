# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YOrientation
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
Yoctopuce library: High-level API for YOrientation
version: PATCH_WITH_VERSION
requires: yocto_orientation_aio
requires: yocto_api
provides: YOrientation
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

from .yocto_orientation_aio import YOrientation as YOrientation_aio
from .yocto_api import (
    YAPIContext, YAPI, YAPI_aio, YSensor, YMeasure
)

# --- (YOrientation class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YOrientationValueCallback = Union[Callable[['YOrientation', str], Any], None]
        YOrientationTimedReportCallback = Union[Callable[['YOrientation', YMeasure], Any], None]
    except TypeError:
        YOrientationValueCallback = Union[Callable, Awaitable]
        YOrientationTimedReportCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YOrientation(YSensor):
    """
    The YOrientation class allows you to read and configure Yoctopuce orientation sensors.
    It inherits from YSensor class the core functions to read measurements,
    to register callback functions, and to access the autonomous datalogger.

    """
    _aio: YOrientation_aio
    # --- (end of YOrientation class start)
    if not _IS_MICROPYTHON:
        # --- (YOrientation return codes)
        COMMAND_INVALID: Final[str] = YAPI.INVALID_STRING
        ZEROOFFSET_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        # --- (end of YOrientation return codes)


    # --- (YOrientation implementation)

    @classmethod
    def FindOrientation(cls, func: str) -> YOrientation:
        """
        Retrieves an orientation sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the orientation sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YOrientation.isOnline() to test if the orientation sensor is
        indeed online at a given time. In case of ambiguity when looking for
        an orientation sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the orientation sensor, for instance
                MyDevice.orientation.

        @return a YOrientation object allowing you to drive the orientation sensor.
        """
        return cls._proxy(cls, YOrientation_aio.FindOrientationInContext(YAPI_aio, func))

    @classmethod
    def FindOrientationInContext(cls, yctx: YAPIContext, func: str) -> YOrientation:
        """
        Retrieves an orientation sensor for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the orientation sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YOrientation.isOnline() to test if the orientation sensor is
        indeed online at a given time. In case of ambiguity when looking for
        an orientation sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the orientation sensor, for instance
                MyDevice.orientation.

        @return a YOrientation object allowing you to drive the orientation sensor.
        """
        return cls._proxy(cls, YOrientation_aio.FindOrientationInContext(yctx._aio, func))

    @classmethod
    def FirstOrientation(cls) -> Union[YOrientation, None]:
        """
        Starts the enumeration of orientation sensors currently accessible.
        Use the method YOrientation.nextOrientation() to iterate on
        next orientation sensors.

        @return a pointer to a YOrientation object, corresponding to
                the first orientation sensor currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YOrientation_aio.FirstOrientationInContext(YAPI_aio))

    @classmethod
    def FirstOrientationInContext(cls, yctx: YAPIContext) -> Union[YOrientation, None]:
        """
        Starts the enumeration of orientation sensors currently accessible.
        Use the method YOrientation.nextOrientation() to iterate on
        next orientation sensors.

        @param yctx : a YAPI context.

        @return a pointer to a YOrientation object, corresponding to
                the first orientation sensor currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YOrientation_aio.FirstOrientationInContext(yctx._aio))

    def nextOrientation(self) -> Union[YOrientation, None]:
        """
        Continues the enumeration of orientation sensors started using yFirstOrientation().
        Caution: You can't make any assumption about the returned orientation sensors order.
        If you want to find a specific an orientation sensor, use Orientation.findOrientation()
        and a hardwareID or a logical name.

        @return a pointer to a YOrientation object, corresponding to
                an orientation sensor currently online, or a None pointer
                if there are no more orientation sensors to enumerate.
        """
        return self._proxy(type(self), self._aio.nextOrientation())

    if not _DYNAMIC_HELPERS:
        def set_command(self, newval: str) -> int:
            return self._run(self._aio.set_command(newval))

    if not _DYNAMIC_HELPERS:
        def set_zeroOffset(self, newval: float) -> int:
            """
            Sets an offset between the orientation reported by the sensor and the actual orientation. This
            can typically be used  to compensate for mechanical offset. This offset can also be set
            automatically using the zero() method.
            Remember to call the saveToFlash() method of the module if the modification must be kept.
            On failure, throws an exception or returns a negative error code.

            @param newval : a floating point number

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_zeroOffset(newval))

    if not _DYNAMIC_HELPERS:
        def get_zeroOffset(self) -> float:
            """
            Returns the Offset between the orientation reported by the sensor and the actual orientation.

            @return a floating point number corresponding to the Offset between the orientation reported by the
            sensor and the actual orientation

            On failure, throws an exception or returns YOrientation.ZEROOFFSET_INVALID.
            """
            return self._run(self._aio.get_zeroOffset())

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YOrientationValueCallback) -> int:
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
        def registerTimedReportCallback(self, callback: YOrientationTimedReportCallback) -> int:
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

    if not _DYNAMIC_HELPERS:
        def zero(self) -> int:
            """
            Reset the sensor's zero to current position by automatically setting a new offset.
            Remember to call the saveToFlash() method of the module if the modification must be kept.

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.zero())

    if not _DYNAMIC_HELPERS:
        def set_calibration(self, offsetValues: list[float]) -> int:
            """
            Modifies the calibration of the MA600A sensor using an array of 32
            values representing the offset in degrees between the true values and
            those measured regularly every 11.25 degrees starting from zero. The calibration
            is applied immediately and is stored permanently in the MA600A sensor.
            Before calculating the offset values, remember to clear any previous
            calibration using the clearCalibration function and set
            the zero offset  to 0. After a calibration change, the sensor will stop
            measurements for about one second.
            Do not confuse this function with the generic calibrateFromPoints function,
            which works at the YSensor level and is not necessarily well suited to
            a sensor returning circular values.

            @param offsetValues : array of 32 floating point values in the [-11.25..+11.25] range

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_calibration(offsetValues))

    if not _DYNAMIC_HELPERS:
        def get_Calibration(self, offsetValues: list[float]) -> int:
            """
            Retrieves offset correction data points previously entered using the method
            set_calibration.

            @param offsetValues : array of 32 floating point numbers, that will be filled by the
                    function with the offset values for the correction points.

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.get_Calibration(offsetValues))

    if not _DYNAMIC_HELPERS:
        def clearCalibration(self) -> int:
            """
            Cancels any calibration set with set_calibration. This function
            is equivalent to calling set_calibration with only zeros.

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.clearCalibration())

    # --- (end of YOrientation implementation)

