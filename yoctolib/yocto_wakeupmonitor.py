# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YWakeUpMonitor
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
Yoctopuce library: High-level API for YWakeUpMonitor
version: PATCH_WITH_VERSION
requires: yocto_wakeupmonitor_aio
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

from .yocto_wakeupmonitor_aio import YWakeUpMonitor as YWakeUpMonitor_aio
from .yocto_api import (
    YAPIContext, YAPI, YFunction
)

# --- (YWakeUpMonitor class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YWakeUpMonitorValueCallback = Union[Callable[['YWakeUpMonitor', str], Awaitable[None]], None]
    except TypeError:
        YWakeUpMonitorValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YWakeUpMonitor(YFunction):
    """
    The YWakeUpMonitor class handles globally all wake-up sources, as well
    as automated sleep mode.

    """
    _aio: YWakeUpMonitor_aio
    # --- (end of YWakeUpMonitor class start)
    if not _IS_MICROPYTHON:
        # --- (YWakeUpMonitor return codes)
        POWERDURATION_INVALID: Final[int] = YAPI.INVALID_UINT
        SLEEPCOUNTDOWN_INVALID: Final[int] = YAPI.INVALID_UINT
        NEXTWAKEUP_INVALID: Final[int] = YAPI.INVALID_LONG
        RTCTIME_INVALID: Final[int] = YAPI.INVALID_LONG
        WAKEUPREASON_USBPOWER: Final[int] = 0
        WAKEUPREASON_EXTPOWER: Final[int] = 1
        WAKEUPREASON_ENDOFSLEEP: Final[int] = 2
        WAKEUPREASON_EXTSIG1: Final[int] = 3
        WAKEUPREASON_SCHEDULE1: Final[int] = 4
        WAKEUPREASON_SCHEDULE2: Final[int] = 5
        WAKEUPREASON_SCHEDULE3: Final[int] = 6
        WAKEUPREASON_INVALID: Final[int] = -1
        WAKEUPSTATE_SLEEPING: Final[int] = 0
        WAKEUPSTATE_AWAKE: Final[int] = 1
        WAKEUPSTATE_INVALID: Final[int] = -1
        # --- (end of YWakeUpMonitor return codes)


    # --- (YWakeUpMonitor implementation)

    @classmethod
    def FirstWakeUpMonitor(cls) -> Union[YWakeUpMonitor, None]:
        """
        Starts the enumeration of wake-up monitors currently accessible.
        Use the method YWakeUpMonitor.nextWakeUpMonitor() to iterate on
        next wake-up monitors.

        @return a pointer to a YWakeUpMonitor object, corresponding to
                the first wake-up monitor currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YWakeUpMonitor_aio.FirstWakeUpMonitor())

    @classmethod
    def FirstWakeUpMonitorInContext(cls, yctx: YAPIContext) -> Union[YWakeUpMonitor, None]:
        """
        Starts the enumeration of wake-up monitors currently accessible.
        Use the method YWakeUpMonitor.nextWakeUpMonitor() to iterate on
        next wake-up monitors.

        @param yctx : a YAPI context.

        @return a pointer to a YWakeUpMonitor object, corresponding to
                the first wake-up monitor currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YWakeUpMonitor_aio.FirstWakeUpMonitorInContext(yctx))

    def nextWakeUpMonitor(self):
        """
        Continues the enumeration of wake-up monitors started using yFirstWakeUpMonitor().
        Caution: You can't make any assumption about the returned wake-up monitors order.
        If you want to find a specific a wake-up monitor, use WakeUpMonitor.findWakeUpMonitor()
        and a hardwareID or a logical name.

        @return a pointer to a YWakeUpMonitor object, corresponding to
                a wake-up monitor currently online, or a None pointer
                if there are no more wake-up monitors to enumerate.
        """
        return self._proxy(type(self), self._aio.nextWakeUpMonitor())

    if not _DYNAMIC_HELPERS:
        def get_powerDuration(self) -> int:
            """
            Returns the maximal wake up time (in seconds) before automatically going to sleep.

            @return an integer corresponding to the maximal wake up time (in seconds) before automatically going to sleep

            On failure, throws an exception or returns YWakeUpMonitor.POWERDURATION_INVALID.
            """
            return self._run(self._aio.get_powerDuration())

    if not _DYNAMIC_HELPERS:
        def set_powerDuration(self, newval: int) -> int:
            """
            Changes the maximal wake up time (seconds) before automatically going to sleep.
            Remember to call the saveToFlash() method of the module if the
            modification must be kept.

            @param newval : an integer corresponding to the maximal wake up time (seconds) before automatically
            going to sleep

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_powerDuration(newval))

    if not _DYNAMIC_HELPERS:
        def get_sleepCountdown(self) -> int:
            """
            Returns the delay before the  next sleep period.

            @return an integer corresponding to the delay before the  next sleep period

            On failure, throws an exception or returns YWakeUpMonitor.SLEEPCOUNTDOWN_INVALID.
            """
            return self._run(self._aio.get_sleepCountdown())

    if not _DYNAMIC_HELPERS:
        def set_sleepCountdown(self, newval: int) -> int:
            """
            Changes the delay before the next sleep period.

            @param newval : an integer corresponding to the delay before the next sleep period

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_sleepCountdown(newval))

    if not _DYNAMIC_HELPERS:
        def get_nextWakeUp(self) -> int:
            """
            Returns the next scheduled wake up date/time (UNIX format).

            @return an integer corresponding to the next scheduled wake up date/time (UNIX format)

            On failure, throws an exception or returns YWakeUpMonitor.NEXTWAKEUP_INVALID.
            """
            return self._run(self._aio.get_nextWakeUp())

    if not _DYNAMIC_HELPERS:
        def set_nextWakeUp(self, newval: int) -> int:
            """
            Changes the days of the week when a wake up must take place.

            @param newval : an integer corresponding to the days of the week when a wake up must take place

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_nextWakeUp(newval))

    if not _DYNAMIC_HELPERS:
        def get_wakeUpReason(self) -> int:
            """
            Returns the latest wake up reason.

            @return a value among YWakeUpMonitor.WAKEUPREASON_USBPOWER, YWakeUpMonitor.WAKEUPREASON_EXTPOWER,
            YWakeUpMonitor.WAKEUPREASON_ENDOFSLEEP, YWakeUpMonitor.WAKEUPREASON_EXTSIG1,
            YWakeUpMonitor.WAKEUPREASON_SCHEDULE1, YWakeUpMonitor.WAKEUPREASON_SCHEDULE2 and
            YWakeUpMonitor.WAKEUPREASON_SCHEDULE3 corresponding to the latest wake up reason

            On failure, throws an exception or returns YWakeUpMonitor.WAKEUPREASON_INVALID.
            """
            return self._run(self._aio.get_wakeUpReason())

    if not _DYNAMIC_HELPERS:
        def get_wakeUpState(self) -> int:
            """
            Returns  the current state of the monitor.

            @return either YWakeUpMonitor.WAKEUPSTATE_SLEEPING or YWakeUpMonitor.WAKEUPSTATE_AWAKE, according
            to  the current state of the monitor

            On failure, throws an exception or returns YWakeUpMonitor.WAKEUPSTATE_INVALID.
            """
            return self._run(self._aio.get_wakeUpState())

    if not _DYNAMIC_HELPERS:
        def set_wakeUpState(self, newval: int) -> int:
            return self._run(self._aio.set_wakeUpState(newval))

    @classmethod
    def FindWakeUpMonitor(cls, func: str) -> YWakeUpMonitor:
        """
        Retrieves a wake-up monitor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the wake-up monitor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YWakeUpMonitor.isOnline() to test if the wake-up monitor is
        indeed online at a given time. In case of ambiguity when looking for
        a wake-up monitor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the wake-up monitor, for instance
                YHUBGSM5.wakeUpMonitor.

        @return a YWakeUpMonitor object allowing you to drive the wake-up monitor.
        """
        return cls._proxy(cls, YWakeUpMonitor_aio.FindWakeUpMonitor(func))

    @classmethod
    def FindWakeUpMonitorInContext(cls, yctx: YAPIContext, func: str) -> YWakeUpMonitor:
        """
        Retrieves a wake-up monitor for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the wake-up monitor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YWakeUpMonitor.isOnline() to test if the wake-up monitor is
        indeed online at a given time. In case of ambiguity when looking for
        a wake-up monitor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the wake-up monitor, for instance
                YHUBGSM5.wakeUpMonitor.

        @return a YWakeUpMonitor object allowing you to drive the wake-up monitor.
        """
        return cls._proxy(cls, YWakeUpMonitor_aio.FindWakeUpMonitorInContext(yctx, func))

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YWakeUpMonitorValueCallback) -> int:
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

    if not _DYNAMIC_HELPERS:
        def wakeUp(self) -> int:
            """
            Forces a wake up.
            """
            return self._run(self._aio.wakeUp())

    if not _DYNAMIC_HELPERS:
        def sleep(self, secBeforeSleep: int) -> int:
            """
            Goes to sleep until the next wake up condition is met,  the
            RTC time must have been set before calling this function.

            @param secBeforeSleep : number of seconds before going into sleep mode,

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.sleep(secBeforeSleep))

    if not _DYNAMIC_HELPERS:
        def sleepFor(self, secUntilWakeUp: int, secBeforeSleep: int) -> int:
            """
            Goes to sleep for a specific duration or until the next wake up condition is met, the
            RTC time must have been set before calling this function. The count down before sleep
            can be canceled with resetSleepCountDown.

            @param secUntilWakeUp : number of seconds before next wake up
            @param secBeforeSleep : number of seconds before going into sleep mode

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.sleepFor(secUntilWakeUp, secBeforeSleep))

    if not _DYNAMIC_HELPERS:
        def sleepUntil(self, wakeUpTime: int, secBeforeSleep: int) -> int:
            """
            Go to sleep until a specific date is reached or until the next wake up condition is met, the
            RTC time must have been set before calling this function. The count down before sleep
            can be canceled with resetSleepCountDown.

            @param wakeUpTime : wake-up datetime (UNIX format)
            @param secBeforeSleep : number of seconds before going into sleep mode

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.sleepUntil(wakeUpTime, secBeforeSleep))

    if not _DYNAMIC_HELPERS:
        def resetSleepCountDown(self) -> int:
            """
            Resets the sleep countdown.

            @return YAPI.SUCCESS if the call succeeds.
                    On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.resetSleepCountDown())

    # --- (end of YWakeUpMonitor implementation)

