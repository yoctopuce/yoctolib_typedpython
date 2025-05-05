# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YMultiCellWeighScale
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
Yoctopuce library: High-level API for YMultiCellWeighScale
version: PATCH_WITH_VERSION
requires: yocto_multicellweighscale_aio
requires: yocto_api
"""
from __future__ import annotations

import sys

# On MicroPython, code below will be wiped out at compile time
if sys.implementation.name != "micropython":
    # In CPython, enable edit-time type checking, including Final declaration
    from typing import Union, Final
    from collections.abc import Callable, Awaitable
    from .yocto_api import _IS_MICROPYTHON, _DYNAMIC_HELPERS
else:
    # In our micropython VM, common generic types are global built-ins
    # Others such as TypeVar should be avoided when using micropython,
    # as they produce overhead in runtime code
    # Final is translated into const() expressions before compilation
    _IS_MICROPYTHON: Final[bool] = True # noqa
    _DYNAMIC_HELPERS: Final[bool] = True # noqa

from .yocto_multicellweighscale_aio import YMultiCellWeighScale as YMultiCellWeighScale_aio
from .yocto_api import (
    YAPIContext, YAPI, YSensor, YMeasure
)

# --- (YMultiCellWeighScale class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YMultiCellWeighScaleValueCallback = Union[Callable[['YMultiCellWeighScale', str], Awaitable[None]], None]
        YMultiCellWeighScaleTimedReportCallback = Union[Callable[['YMultiCellWeighScale', YMeasure], Awaitable[None]], None]
    except TypeError:
        YMultiCellWeighScaleValueCallback = Union[Callable, Awaitable]
        YMultiCellWeighScaleTimedReportCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YMultiCellWeighScale(YSensor):
    """
    The YMultiCellWeighScale class provides a weight measurement from a set of ratiometric
    sensors. It can be used to control the bridge excitation parameters, in order to avoid
    measure shifts caused by temperature variation in the electronics, and can also
    automatically apply an additional correction factor based on temperature to
    compensate for offsets in the load cells themselves.

    """
    _aio: YMultiCellWeighScale_aio
    # --- (end of YMultiCellWeighScale class start)
    if not _IS_MICROPYTHON:
        # --- (YMultiCellWeighScale return codes)
        CELLCOUNT_INVALID: Final[int] = YAPI.INVALID_UINT
        TEMPAVGADAPTRATIO_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        TEMPCHGADAPTRATIO_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        COMPTEMPAVG_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        COMPTEMPCHG_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        COMPENSATION_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        ZEROTRACKING_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        COMMAND_INVALID: Final[str] = YAPI.INVALID_STRING
        EXTERNALSENSE_FALSE: Final[int] = 0
        EXTERNALSENSE_TRUE: Final[int] = 1
        EXTERNALSENSE_INVALID: Final[int] = -1
        EXCITATION_OFF: Final[int] = 0
        EXCITATION_DC: Final[int] = 1
        EXCITATION_AC: Final[int] = 2
        EXCITATION_INVALID: Final[int] = -1
        # --- (end of YMultiCellWeighScale return codes)


    # --- (YMultiCellWeighScale implementation)

    @classmethod
    def FirstMultiCellWeighScale(cls) -> Union[YMultiCellWeighScale, None]:
        """
        Starts the enumeration of multi-cell weighing scale sensors currently accessible.
        Use the method YMultiCellWeighScale.nextMultiCellWeighScale() to iterate on
        next multi-cell weighing scale sensors.

        @return a pointer to a YMultiCellWeighScale object, corresponding to
                the first multi-cell weighing scale sensor currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YMultiCellWeighScale_aio.FirstMultiCellWeighScale())

    @classmethod
    def FirstMultiCellWeighScaleInContext(cls, yctx: YAPIContext) -> Union[YMultiCellWeighScale, None]:
        """
        Starts the enumeration of multi-cell weighing scale sensors currently accessible.
        Use the method YMultiCellWeighScale.nextMultiCellWeighScale() to iterate on
        next multi-cell weighing scale sensors.

        @param yctx : a YAPI context.

        @return a pointer to a YMultiCellWeighScale object, corresponding to
                the first multi-cell weighing scale sensor currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YMultiCellWeighScale_aio.FirstMultiCellWeighScaleInContext(yctx))

    def nextMultiCellWeighScale(self):
        """
        Continues the enumeration of multi-cell weighing scale sensors started using yFirstMultiCellWeighScale().
        Caution: You can't make any assumption about the returned multi-cell weighing scale sensors order.
        If you want to find a specific a multi-cell weighing scale sensor, use
        MultiCellWeighScale.findMultiCellWeighScale()
        and a hardwareID or a logical name.

        @return a pointer to a YMultiCellWeighScale object, corresponding to
                a multi-cell weighing scale sensor currently online, or a None pointer
                if there are no more multi-cell weighing scale sensors to enumerate.
        """
        return self._proxy(type(self), self._aio.nextMultiCellWeighScale())

    if not _DYNAMIC_HELPERS:
        def set_unit(self, newval: str) -> int:
            """
            Changes the measuring unit for the weight.
            Remember to call the saveToFlash() method of the module if the
            modification must be kept.

            @param newval : a string corresponding to the measuring unit for the weight

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_unit(newval))

    if not _DYNAMIC_HELPERS:
        def get_cellCount(self) -> int:
            """
            Returns the number of load cells in use.

            @return an integer corresponding to the number of load cells in use

            On failure, throws an exception or returns YMultiCellWeighScale.CELLCOUNT_INVALID.
            """
            return self._run(self._aio.get_cellCount())

    if not _DYNAMIC_HELPERS:
        def set_cellCount(self, newval: int) -> int:
            """
            Changes the number of load cells in use. Remember to call the saveToFlash()
            method of the module if the modification must be kept.

            @param newval : an integer corresponding to the number of load cells in use

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_cellCount(newval))

    if not _DYNAMIC_HELPERS:
        def get_externalSense(self) -> int:
            """
            Returns true if entry 4 is used as external sense for 6-wires load cells.

            @return either YMultiCellWeighScale.EXTERNALSENSE_FALSE or YMultiCellWeighScale.EXTERNALSENSE_TRUE,
            according to true if entry 4 is used as external sense for 6-wires load cells

            On failure, throws an exception or returns YMultiCellWeighScale.EXTERNALSENSE_INVALID.
            """
            return self._run(self._aio.get_externalSense())

    if not _DYNAMIC_HELPERS:
        def set_externalSense(self, newval: int) -> int:
            """
            Changes the configuration to tell if entry 4 is used as external sense for
            6-wires load cells. Remember to call the saveToFlash() method of the
            module if the modification must be kept.

            @param newval : either YMultiCellWeighScale.EXTERNALSENSE_FALSE or
            YMultiCellWeighScale.EXTERNALSENSE_TRUE, according to the configuration to tell if entry 4 is used
            as external sense for
                    6-wires load cells

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_externalSense(newval))

    if not _DYNAMIC_HELPERS:
        def get_excitation(self) -> int:
            """
            Returns the current load cell bridge excitation method.

            @return a value among YMultiCellWeighScale.EXCITATION_OFF, YMultiCellWeighScale.EXCITATION_DC and
            YMultiCellWeighScale.EXCITATION_AC corresponding to the current load cell bridge excitation method

            On failure, throws an exception or returns YMultiCellWeighScale.EXCITATION_INVALID.
            """
            return self._run(self._aio.get_excitation())

    if not _DYNAMIC_HELPERS:
        def set_excitation(self, newval: int) -> int:
            """
            Changes the current load cell bridge excitation method.
            Remember to call the saveToFlash() method of the module if the
            modification must be kept.

            @param newval : a value among YMultiCellWeighScale.EXCITATION_OFF,
            YMultiCellWeighScale.EXCITATION_DC and YMultiCellWeighScale.EXCITATION_AC corresponding to the
            current load cell bridge excitation method

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_excitation(newval))

    if not _DYNAMIC_HELPERS:
        def set_tempAvgAdaptRatio(self, newval: float) -> int:
            """
            Changes the averaged temperature update rate, in per mille.
            The purpose of this adaptation ratio is to model the thermal inertia of the load cell.
            The averaged temperature is updated every 10 seconds, by applying this adaptation rate
            to the difference between the measures ambient temperature and the current compensation
            temperature. The standard rate is 0.2 per mille, and the maximal rate is 65 per mille.
            Remember to call the saveToFlash() method of the module if the
            modification must be kept.

            @param newval : a floating point number corresponding to the averaged temperature update rate, in per mille

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_tempAvgAdaptRatio(newval))

    if not _DYNAMIC_HELPERS:
        def get_tempAvgAdaptRatio(self) -> float:
            """
            Returns the averaged temperature update rate, in per mille.
            The purpose of this adaptation ratio is to model the thermal inertia of the load cell.
            The averaged temperature is updated every 10 seconds, by applying this adaptation rate
            to the difference between the measures ambient temperature and the current compensation
            temperature. The standard rate is 0.2 per mille, and the maximal rate is 65 per mille.

            @return a floating point number corresponding to the averaged temperature update rate, in per mille

            On failure, throws an exception or returns YMultiCellWeighScale.TEMPAVGADAPTRATIO_INVALID.
            """
            return self._run(self._aio.get_tempAvgAdaptRatio())

    if not _DYNAMIC_HELPERS:
        def set_tempChgAdaptRatio(self, newval: float) -> int:
            """
            Changes the temperature change update rate, in per mille.
            The temperature change is updated every 10 seconds, by applying this adaptation rate
            to the difference between the measures ambient temperature and the current temperature used for
            change compensation. The standard rate is 0.6 per mille, and the maximal rate is 65 per mille.
            Remember to call the saveToFlash() method of the module if the
            modification must be kept.

            @param newval : a floating point number corresponding to the temperature change update rate, in per mille

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_tempChgAdaptRatio(newval))

    if not _DYNAMIC_HELPERS:
        def get_tempChgAdaptRatio(self) -> float:
            """
            Returns the temperature change update rate, in per mille.
            The temperature change is updated every 10 seconds, by applying this adaptation rate
            to the difference between the measures ambient temperature and the current temperature used for
            change compensation. The standard rate is 0.6 per mille, and the maximal rate is 65 per mille.

            @return a floating point number corresponding to the temperature change update rate, in per mille

            On failure, throws an exception or returns YMultiCellWeighScale.TEMPCHGADAPTRATIO_INVALID.
            """
            return self._run(self._aio.get_tempChgAdaptRatio())

    if not _DYNAMIC_HELPERS:
        def get_compTempAvg(self) -> float:
            """
            Returns the current averaged temperature, used for thermal compensation.

            @return a floating point number corresponding to the current averaged temperature, used for thermal compensation

            On failure, throws an exception or returns YMultiCellWeighScale.COMPTEMPAVG_INVALID.
            """
            return self._run(self._aio.get_compTempAvg())

    if not _DYNAMIC_HELPERS:
        def get_compTempChg(self) -> float:
            """
            Returns the current temperature variation, used for thermal compensation.

            @return a floating point number corresponding to the current temperature variation, used for
            thermal compensation

            On failure, throws an exception or returns YMultiCellWeighScale.COMPTEMPCHG_INVALID.
            """
            return self._run(self._aio.get_compTempChg())

    if not _DYNAMIC_HELPERS:
        def get_compensation(self) -> float:
            """
            Returns the current current thermal compensation value.

            @return a floating point number corresponding to the current current thermal compensation value

            On failure, throws an exception or returns YMultiCellWeighScale.COMPENSATION_INVALID.
            """
            return self._run(self._aio.get_compensation())

    if not _DYNAMIC_HELPERS:
        def set_zeroTracking(self, newval: float) -> int:
            """
            Changes the zero tracking threshold value. When this threshold is larger than
            zero, any measure under the threshold will automatically be ignored and the
            zero compensation will be updated.
            Remember to call the saveToFlash() method of the module if the
            modification must be kept.

            @param newval : a floating point number corresponding to the zero tracking threshold value

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_zeroTracking(newval))

    if not _DYNAMIC_HELPERS:
        def get_zeroTracking(self) -> float:
            """
            Returns the zero tracking threshold value. When this threshold is larger than
            zero, any measure under the threshold will automatically be ignored and the
            zero compensation will be updated.

            @return a floating point number corresponding to the zero tracking threshold value

            On failure, throws an exception or returns YMultiCellWeighScale.ZEROTRACKING_INVALID.
            """
            return self._run(self._aio.get_zeroTracking())

    if not _DYNAMIC_HELPERS:
        def set_command(self, newval: str) -> int:
            return self._run(self._aio.set_command(newval))

    @classmethod
    def FindMultiCellWeighScale(cls, func: str) -> YMultiCellWeighScale:
        """
        Retrieves a multi-cell weighing scale sensor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the multi-cell weighing scale sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YMultiCellWeighScale.isOnline() to test if the multi-cell weighing scale sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a multi-cell weighing scale sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the multi-cell weighing scale sensor, for instance
                YWMBRDG1.multiCellWeighScale.

        @return a YMultiCellWeighScale object allowing you to drive the multi-cell weighing scale sensor.
        """
        return cls._proxy(cls, YMultiCellWeighScale_aio.FindMultiCellWeighScale(func))

    @classmethod
    def FindMultiCellWeighScaleInContext(cls, yctx: YAPIContext, func: str) -> YMultiCellWeighScale:
        """
        Retrieves a multi-cell weighing scale sensor for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the multi-cell weighing scale sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YMultiCellWeighScale.isOnline() to test if the multi-cell weighing scale sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a multi-cell weighing scale sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the multi-cell weighing scale sensor, for instance
                YWMBRDG1.multiCellWeighScale.

        @return a YMultiCellWeighScale object allowing you to drive the multi-cell weighing scale sensor.
        """
        return cls._proxy(cls, YMultiCellWeighScale_aio.FindMultiCellWeighScaleInContext(yctx, func))

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YMultiCellWeighScaleValueCallback) -> int:
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
            return super().registerValueCallback(callback)

    if not _IS_MICROPYTHON:
        def registerTimedReportCallback(self, callback: YMultiCellWeighScaleTimedReportCallback) -> int:
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
        def tare(self) -> int:
            """
            Adapts the load cell signal bias (stored in the corresponding genericSensor)
            so that the current signal corresponds to a zero weight. Remember to call the
            saveToFlash() method of the module if the modification must be kept.

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.tare())

    if not _DYNAMIC_HELPERS:
        def setupSpan(self, currWeight: float, maxWeight: float) -> int:
            """
            Configures the load cells span parameters (stored in the corresponding genericSensors)
            so that the current signal corresponds to the specified reference weight.

            @param currWeight : reference weight presently on the load cell.
            @param maxWeight : maximum weight to be expected on the load cell.

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.setupSpan(currWeight, maxWeight))

    # --- (end of YMultiCellWeighScale implementation)

