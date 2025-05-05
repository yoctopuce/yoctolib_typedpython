# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YPwmOutput
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
Yoctopuce library: High-level API for YPwmOutput
version: PATCH_WITH_VERSION
requires: yocto_pwmoutput_aio
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

from .yocto_pwmoutput_aio import YPwmOutput as YPwmOutput_aio
from .yocto_api import (
    YAPIContext, YAPI, YFunction
)

# --- (YPwmOutput class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YPwmOutputValueCallback = Union[Callable[['YPwmOutput', str], Awaitable[None]], None]
    except TypeError:
        YPwmOutputValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YPwmOutput(YFunction):
    """
    The YPwmOutput class allows you to drive a pulse-width modulated output (PWM).
    You can configure the frequency as well as the duty cycle, and set up progressive
    transitions.

    """
    _aio: YPwmOutput_aio
    # --- (end of YPwmOutput class start)
    if not _IS_MICROPYTHON:
        # --- (YPwmOutput return codes)
        FREQUENCY_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        PERIOD_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        DUTYCYCLE_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        PULSEDURATION_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        PWMTRANSITION_INVALID: Final[str] = YAPI.INVALID_STRING
        DUTYCYCLEATPOWERON_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        ENABLED_FALSE: Final[int] = 0
        ENABLED_TRUE: Final[int] = 1
        ENABLED_INVALID: Final[int] = -1
        INVERTEDOUTPUT_FALSE: Final[int] = 0
        INVERTEDOUTPUT_TRUE: Final[int] = 1
        INVERTEDOUTPUT_INVALID: Final[int] = -1
        ENABLEDATPOWERON_FALSE: Final[int] = 0
        ENABLEDATPOWERON_TRUE: Final[int] = 1
        ENABLEDATPOWERON_INVALID: Final[int] = -1
        # --- (end of YPwmOutput return codes)


    # --- (YPwmOutput implementation)

    @classmethod
    def FirstPwmOutput(cls) -> Union[YPwmOutput, None]:
        """
        Starts the enumeration of PWM generators currently accessible.
        Use the method YPwmOutput.nextPwmOutput() to iterate on
        next PWM generators.

        @return a pointer to a YPwmOutput object, corresponding to
                the first PWM generator currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YPwmOutput_aio.FirstPwmOutput())

    @classmethod
    def FirstPwmOutputInContext(cls, yctx: YAPIContext) -> Union[YPwmOutput, None]:
        """
        Starts the enumeration of PWM generators currently accessible.
        Use the method YPwmOutput.nextPwmOutput() to iterate on
        next PWM generators.

        @param yctx : a YAPI context.

        @return a pointer to a YPwmOutput object, corresponding to
                the first PWM generator currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YPwmOutput_aio.FirstPwmOutputInContext(yctx))

    def nextPwmOutput(self):
        """
        Continues the enumeration of PWM generators started using yFirstPwmOutput().
        Caution: You can't make any assumption about the returned PWM generators order.
        If you want to find a specific a PWM generator, use PwmOutput.findPwmOutput()
        and a hardwareID or a logical name.

        @return a pointer to a YPwmOutput object, corresponding to
                a PWM generator currently online, or a None pointer
                if there are no more PWM generators to enumerate.
        """
        return self._proxy(type(self), self._aio.nextPwmOutput())

    if not _DYNAMIC_HELPERS:
        def get_enabled(self) -> int:
            """
            Returns the state of the PWM generators.

            @return either YPwmOutput.ENABLED_FALSE or YPwmOutput.ENABLED_TRUE, according to the state of the PWM generators

            On failure, throws an exception or returns YPwmOutput.ENABLED_INVALID.
            """
            return self._run(self._aio.get_enabled())

    if not _DYNAMIC_HELPERS:
        def set_enabled(self, newval: int) -> int:
            """
            Stops or starts the PWM.

            @param newval : either YPwmOutput.ENABLED_FALSE or YPwmOutput.ENABLED_TRUE

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_enabled(newval))

    if not _DYNAMIC_HELPERS:
        def set_frequency(self, newval: float) -> int:
            """
            Changes the PWM frequency. The duty cycle is kept unchanged thanks to an
            automatic pulse width change, in other words, the change will not be applied
            before the end of the current period. This can significantly affect reaction
            time at low frequencies. If you call the matching module saveToFlash()
            method, the frequency will be kept after a device power cycle.
            To stop the PWM signal, do not set the frequency to zero, use the set_enabled()
            method instead.

            @param newval : a floating point number corresponding to the PWM frequency

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_frequency(newval))

    if not _DYNAMIC_HELPERS:
        def get_frequency(self) -> float:
            """
            Returns the PWM frequency in Hz.

            @return a floating point number corresponding to the PWM frequency in Hz

            On failure, throws an exception or returns YPwmOutput.FREQUENCY_INVALID.
            """
            return self._run(self._aio.get_frequency())

    if not _DYNAMIC_HELPERS:
        def set_period(self, newval: float) -> int:
            """
            Changes the PWM period in milliseconds. Caution: in order to avoid  random truncation of
            the current pulse, the change will not be applied
            before the end of the current period. This can significantly affect reaction
            time at low frequencies. If you call the matching module saveToFlash()
            method, the frequency will be kept after a device power cycle.

            @param newval : a floating point number corresponding to the PWM period in milliseconds

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_period(newval))

    if not _DYNAMIC_HELPERS:
        def get_period(self) -> float:
            """
            Returns the PWM period in milliseconds.

            @return a floating point number corresponding to the PWM period in milliseconds

            On failure, throws an exception or returns YPwmOutput.PERIOD_INVALID.
            """
            return self._run(self._aio.get_period())

    if not _DYNAMIC_HELPERS:
        def set_dutyCycle(self, newval: float) -> int:
            """
            Changes the PWM duty cycle, in per cents.

            @param newval : a floating point number corresponding to the PWM duty cycle, in per cents

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_dutyCycle(newval))

    if not _DYNAMIC_HELPERS:
        def get_dutyCycle(self) -> float:
            """
            Returns the PWM duty cycle, in per cents.

            @return a floating point number corresponding to the PWM duty cycle, in per cents

            On failure, throws an exception or returns YPwmOutput.DUTYCYCLE_INVALID.
            """
            return self._run(self._aio.get_dutyCycle())

    if not _DYNAMIC_HELPERS:
        def set_pulseDuration(self, newval: float) -> int:
            """
            Changes the PWM pulse length, in milliseconds. A pulse length cannot be longer than period,
            otherwise it is truncated.

            @param newval : a floating point number corresponding to the PWM pulse length, in milliseconds

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_pulseDuration(newval))

    if not _DYNAMIC_HELPERS:
        def get_pulseDuration(self) -> float:
            """
            Returns the PWM pulse length in milliseconds, as a floating point number.

            @return a floating point number corresponding to the PWM pulse length in milliseconds, as a
            floating point number

            On failure, throws an exception or returns YPwmOutput.PULSEDURATION_INVALID.
            """
            return self._run(self._aio.get_pulseDuration())

    if not _DYNAMIC_HELPERS:
        def set_pwmTransition(self, newval: str) -> int:
            return self._run(self._aio.set_pwmTransition(newval))

    if not _DYNAMIC_HELPERS:
        def get_invertedOutput(self) -> int:
            """
            Returns true if the output signal is configured as inverted, and false otherwise.

            @return either YPwmOutput.INVERTEDOUTPUT_FALSE or YPwmOutput.INVERTEDOUTPUT_TRUE, according to true
            if the output signal is configured as inverted, and false otherwise

            On failure, throws an exception or returns YPwmOutput.INVERTEDOUTPUT_INVALID.
            """
            return self._run(self._aio.get_invertedOutput())

    if not _DYNAMIC_HELPERS:
        def set_invertedOutput(self, newval: int) -> int:
            """
            Changes the inversion mode of the output signal.
            Remember to call the matching module saveToFlash() method if you want
            the change to be kept after power cycle.

            @param newval : either YPwmOutput.INVERTEDOUTPUT_FALSE or YPwmOutput.INVERTEDOUTPUT_TRUE, according
            to the inversion mode of the output signal

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_invertedOutput(newval))

    if not _DYNAMIC_HELPERS:
        def get_enabledAtPowerOn(self) -> int:
            """
            Returns the state of the PWM at device power on.

            @return either YPwmOutput.ENABLEDATPOWERON_FALSE or YPwmOutput.ENABLEDATPOWERON_TRUE, according to
            the state of the PWM at device power on

            On failure, throws an exception or returns YPwmOutput.ENABLEDATPOWERON_INVALID.
            """
            return self._run(self._aio.get_enabledAtPowerOn())

    if not _DYNAMIC_HELPERS:
        def set_enabledAtPowerOn(self, newval: int) -> int:
            """
            Changes the state of the PWM at device power on. Remember to call the matching module saveToFlash()
            method, otherwise this call will have no effect.

            @param newval : either YPwmOutput.ENABLEDATPOWERON_FALSE or YPwmOutput.ENABLEDATPOWERON_TRUE,
            according to the state of the PWM at device power on

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_enabledAtPowerOn(newval))

    if not _DYNAMIC_HELPERS:
        def set_dutyCycleAtPowerOn(self, newval: float) -> int:
            """
            Changes the PWM duty cycle at device power on. Remember to call the matching
            module saveToFlash() method, otherwise this call will have no effect.

            @param newval : a floating point number corresponding to the PWM duty cycle at device power on

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_dutyCycleAtPowerOn(newval))

    if not _DYNAMIC_HELPERS:
        def get_dutyCycleAtPowerOn(self) -> float:
            """
            Returns the PWM generators duty cycle at device power on as a floating point number between 0 and 100.

            @return a floating point number corresponding to the PWM generators duty cycle at device power on
            as a floating point number between 0 and 100

            On failure, throws an exception or returns YPwmOutput.DUTYCYCLEATPOWERON_INVALID.
            """
            return self._run(self._aio.get_dutyCycleAtPowerOn())

    @classmethod
    def FindPwmOutput(cls, func: str) -> YPwmOutput:
        """
        Retrieves a PWM generator for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the PWM generator is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPwmOutput.isOnline() to test if the PWM generator is
        indeed online at a given time. In case of ambiguity when looking for
        a PWM generator by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the PWM generator, for instance
                YPWMTX01.pwmOutput1.

        @return a YPwmOutput object allowing you to drive the PWM generator.
        """
        return cls._proxy(cls, YPwmOutput_aio.FindPwmOutput(func))

    @classmethod
    def FindPwmOutputInContext(cls, yctx: YAPIContext, func: str) -> YPwmOutput:
        """
        Retrieves a PWM generator for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the PWM generator is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPwmOutput.isOnline() to test if the PWM generator is
        indeed online at a given time. In case of ambiguity when looking for
        a PWM generator by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the PWM generator, for instance
                YPWMTX01.pwmOutput1.

        @return a YPwmOutput object allowing you to drive the PWM generator.
        """
        return cls._proxy(cls, YPwmOutput_aio.FindPwmOutputInContext(yctx, func))

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YPwmOutputValueCallback) -> int:
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
        def pulseDurationMove(self, ms_target: float, ms_duration: int) -> int:
            """
            Performs a smooth transition of the pulse duration toward a given value.
            Any period, frequency, duty cycle or pulse width change will cancel any ongoing transition process.

            @param ms_target   : new pulse duration at the end of the transition
                    (floating-point number, representing the pulse duration in milliseconds)
            @param ms_duration : total duration of the transition, in milliseconds

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.pulseDurationMove(ms_target, ms_duration))

    if not _DYNAMIC_HELPERS:
        def dutyCycleMove(self, target: float, ms_duration: int) -> int:
            """
            Performs a smooth change of the duty cycle toward a given value.
            Any period, frequency, duty cycle or pulse width change will cancel any ongoing transition process.

            @param target      : new duty cycle at the end of the transition
                    (percentage, floating-point number between 0 and 100)
            @param ms_duration : total duration of the transition, in milliseconds

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.dutyCycleMove(target, ms_duration))

    if not _DYNAMIC_HELPERS:
        def frequencyMove(self, target: float, ms_duration: int) -> int:
            """
            Performs a smooth frequency change toward a given value.
            Any period, frequency, duty cycle or pulse width change will cancel any ongoing transition process.

            @param target      : new frequency at the end of the transition (floating-point number)
            @param ms_duration : total duration of the transition, in milliseconds

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.frequencyMove(target, ms_duration))

    if not _DYNAMIC_HELPERS:
        def phaseMove(self, target: float, ms_duration: int) -> int:
            """
            Performs a smooth transition toward a specified value of the phase shift between this channel
            and the other channel. The phase shift is executed by slightly changing the frequency
            temporarily during the specified duration. This function only makes sense when both channels
            are running, either at the same frequency, or at a multiple of the channel frequency.
            Any period, frequency, duty cycle or pulse width change will cancel any ongoing transition process.

            @param target      : phase shift at the end of the transition, in milliseconds (floating-point number)
            @param ms_duration : total duration of the transition, in milliseconds

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.phaseMove(target, ms_duration))

    if not _DYNAMIC_HELPERS:
        def triggerPulsesByDuration(self, ms_target: float, n_pulses: int) -> int:
            """
            Trigger a given number of pulses of specified duration, at current frequency.
            At the end of the pulse train, revert to the original state of the PWM generator.

            @param ms_target : desired pulse duration
                    (floating-point number, representing the pulse duration in milliseconds)
            @param n_pulses  : desired pulse count

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.triggerPulsesByDuration(ms_target, n_pulses))

    if not _DYNAMIC_HELPERS:
        def triggerPulsesByDutyCycle(self, target: float, n_pulses: int) -> int:
            """
            Trigger a given number of pulses of specified duration, at current frequency.
            At the end of the pulse train, revert to the original state of the PWM generator.

            @param target   : desired duty cycle for the generated pulses
                    (percentage, floating-point number between 0 and 100)
            @param n_pulses : desired pulse count

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.triggerPulsesByDutyCycle(target, n_pulses))

    if not _DYNAMIC_HELPERS:
        def triggerPulsesByFrequency(self, target: float, n_pulses: int) -> int:
            """
            Trigger a given number of pulses at the specified frequency, using current duty cycle.
            At the end of the pulse train, revert to the original state of the PWM generator.

            @param target   : desired frequency for the generated pulses (floating-point number)
            @param n_pulses : desired pulse count

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.triggerPulsesByFrequency(target, n_pulses))

    # --- (end of YPwmOutput implementation)

