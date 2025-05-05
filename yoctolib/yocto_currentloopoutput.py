# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YCurrentLoopOutput
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
Yoctopuce library: High-level API for YCurrentLoopOutput
version: PATCH_WITH_VERSION
requires: yocto_currentloopoutput_aio
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

from .yocto_currentloopoutput_aio import YCurrentLoopOutput as YCurrentLoopOutput_aio
from .yocto_api import (
    YAPIContext, YAPI, YFunction
)

# --- (YCurrentLoopOutput class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YCurrentLoopOutputValueCallback = Union[Callable[['YCurrentLoopOutput', str], Awaitable[None]], None]
    except TypeError:
        YCurrentLoopOutputValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YCurrentLoopOutput(YFunction):
    """
    The YCurrentLoopOutput class allows you to drive a 4-20mA output
    by regulating the current flowing through the current loop.
    It can also provide information about the power state of the current loop.

    """
    _aio: YCurrentLoopOutput_aio
    # --- (end of YCurrentLoopOutput class start)
    if not _IS_MICROPYTHON:
        # --- (YCurrentLoopOutput return codes)
        CURRENT_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        CURRENTTRANSITION_INVALID: Final[str] = YAPI.INVALID_STRING
        CURRENTATSTARTUP_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        LOOPPOWER_NOPWR: Final[int] = 0
        LOOPPOWER_LOWPWR: Final[int] = 1
        LOOPPOWER_POWEROK: Final[int] = 2
        LOOPPOWER_INVALID: Final[int] = -1
        # --- (end of YCurrentLoopOutput return codes)


    # --- (YCurrentLoopOutput implementation)

    @classmethod
    def FirstCurrentLoopOutput(cls) -> Union[YCurrentLoopOutput, None]:
        """
        Starts the enumeration of 4-20mA outputs currently accessible.
        Use the method YCurrentLoopOutput.nextCurrentLoopOutput() to iterate on
        next 4-20mA outputs.

        @return a pointer to a YCurrentLoopOutput object, corresponding to
                the first 4-20mA output currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YCurrentLoopOutput_aio.FirstCurrentLoopOutput())

    @classmethod
    def FirstCurrentLoopOutputInContext(cls, yctx: YAPIContext) -> Union[YCurrentLoopOutput, None]:
        """
        Starts the enumeration of 4-20mA outputs currently accessible.
        Use the method YCurrentLoopOutput.nextCurrentLoopOutput() to iterate on
        next 4-20mA outputs.

        @param yctx : a YAPI context.

        @return a pointer to a YCurrentLoopOutput object, corresponding to
                the first 4-20mA output currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YCurrentLoopOutput_aio.FirstCurrentLoopOutputInContext(yctx))

    def nextCurrentLoopOutput(self):
        """
        Continues the enumeration of 4-20mA outputs started using yFirstCurrentLoopOutput().
        Caution: You can't make any assumption about the returned 4-20mA outputs order.
        If you want to find a specific a 4-20mA output, use CurrentLoopOutput.findCurrentLoopOutput()
        and a hardwareID or a logical name.

        @return a pointer to a YCurrentLoopOutput object, corresponding to
                a 4-20mA output currently online, or a None pointer
                if there are no more 4-20mA outputs to enumerate.
        """
        return self._proxy(type(self), self._aio.nextCurrentLoopOutput())

    if not _DYNAMIC_HELPERS:
        def set_current(self, newval: float) -> int:
            """
            Changes the current loop, the valid range is from 3 to 21mA. If the loop is
            not properly powered, the  target current is not reached and
            loopPower is set to LOWPWR.

            @param newval : a floating point number corresponding to the current loop, the valid range is from 3 to 21mA

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_current(newval))

    if not _DYNAMIC_HELPERS:
        def get_current(self) -> float:
            """
            Returns the loop current set point in mA.

            @return a floating point number corresponding to the loop current set point in mA

            On failure, throws an exception or returns YCurrentLoopOutput.CURRENT_INVALID.
            """
            return self._run(self._aio.get_current())

    if not _DYNAMIC_HELPERS:
        def set_currentTransition(self, newval: str) -> int:
            return self._run(self._aio.set_currentTransition(newval))

    if not _DYNAMIC_HELPERS:
        def set_currentAtStartUp(self, newval: float) -> int:
            """
            Changes the loop current at device start up. Remember to call the matching
            module saveToFlash() method, otherwise this call has no effect.

            @param newval : a floating point number corresponding to the loop current at device start up

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_currentAtStartUp(newval))

    if not _DYNAMIC_HELPERS:
        def get_currentAtStartUp(self) -> float:
            """
            Returns the current in the loop at device startup, in mA.

            @return a floating point number corresponding to the current in the loop at device startup, in mA

            On failure, throws an exception or returns YCurrentLoopOutput.CURRENTATSTARTUP_INVALID.
            """
            return self._run(self._aio.get_currentAtStartUp())

    if not _DYNAMIC_HELPERS:
        def get_loopPower(self) -> int:
            """
            Returns the loop powerstate.  POWEROK: the loop
            is powered. NOPWR: the loop in not powered. LOWPWR: the loop is not
            powered enough to maintain the current required (insufficient voltage).

            @return a value among YCurrentLoopOutput.LOOPPOWER_NOPWR, YCurrentLoopOutput.LOOPPOWER_LOWPWR and
            YCurrentLoopOutput.LOOPPOWER_POWEROK corresponding to the loop powerstate

            On failure, throws an exception or returns YCurrentLoopOutput.LOOPPOWER_INVALID.
            """
            return self._run(self._aio.get_loopPower())

    @classmethod
    def FindCurrentLoopOutput(cls, func: str) -> YCurrentLoopOutput:
        """
        Retrieves a 4-20mA output for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the 4-20mA output is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCurrentLoopOutput.isOnline() to test if the 4-20mA output is
        indeed online at a given time. In case of ambiguity when looking for
        a 4-20mA output by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the 4-20mA output, for instance
                TX420MA1.currentLoopOutput.

        @return a YCurrentLoopOutput object allowing you to drive the 4-20mA output.
        """
        return cls._proxy(cls, YCurrentLoopOutput_aio.FindCurrentLoopOutput(func))

    @classmethod
    def FindCurrentLoopOutputInContext(cls, yctx: YAPIContext, func: str) -> YCurrentLoopOutput:
        """
        Retrieves a 4-20mA output for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the 4-20mA output is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YCurrentLoopOutput.isOnline() to test if the 4-20mA output is
        indeed online at a given time. In case of ambiguity when looking for
        a 4-20mA output by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the 4-20mA output, for instance
                TX420MA1.currentLoopOutput.

        @return a YCurrentLoopOutput object allowing you to drive the 4-20mA output.
        """
        return cls._proxy(cls, YCurrentLoopOutput_aio.FindCurrentLoopOutputInContext(yctx, func))

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YCurrentLoopOutputValueCallback) -> int:
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
        def currentMove(self, mA_target: float, ms_duration: int) -> int:
            """
            Performs a smooth transition of current flowing in the loop. Any current explicit
            change cancels any ongoing transition process.

            @param mA_target   : new current value at the end of the transition
                    (floating-point number, representing the end current in mA)
            @param ms_duration : total duration of the transition, in milliseconds

            @return YAPI.SUCCESS when the call succeeds.
            """
            return self._run(self._aio.currentMove(mA_target, ms_duration))

    # --- (end of YCurrentLoopOutput implementation)

