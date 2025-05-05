# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YRelay
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
Yoctopuce library: Asyncio implementation of YRelay
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
    YAPIContext, YAPI, YAPI_Exception, HwId, hwid2str, YFunction, YModule
)

# --- (YRelay class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YRelayValueCallback = Union[Callable[['YRelay', str], Awaitable[None]], None]
    except TypeError:
        YRelayValueCallback = Union[Callable, Awaitable]
if _IS_MICROPYTHON:
    from collections import namedtuple
    YDelayedPulse = namedtuple("YDelayedPulse", ('target', 'ms', 'moving'))
else:
    from typing import NamedTuple
    class YDelayedPulse(NamedTuple):
        target: int
        ms: int
        moving: int


# noinspection PyProtectedMember
class YRelay(YFunction):
    """
    The YRelay class allows you to drive a Yoctopuce relay or optocoupled output.
    It can be used to simply switch the output on or off, but also to automatically generate short
    pulses of determined duration.
    On devices with two output for each relay (double throw), the two outputs are named A and B,
    with output A corresponding to the idle position (normally closed) and the output B corresponding to the
    active state (normally open).

    """
    # --- (end of YRelay class start)
    if not _IS_MICROPYTHON:
        # --- (YRelay return codes)
        MAXTIMEONSTATEA_INVALID: Final[int] = YAPI.INVALID_LONG
        MAXTIMEONSTATEB_INVALID: Final[int] = YAPI.INVALID_LONG
        PULSETIMER_INVALID: Final[int] = YAPI.INVALID_LONG
        DELAYEDPULSETIMER_INVALID: Final[None] = None
        COUNTDOWN_INVALID: Final[int] = YAPI.INVALID_LONG
        STATE_A: Final[int] = 0
        STATE_B: Final[int] = 1
        STATE_INVALID: Final[int] = -1
        STATEATPOWERON_UNCHANGED: Final[int] = 0
        STATEATPOWERON_A: Final[int] = 1
        STATEATPOWERON_B: Final[int] = 2
        STATEATPOWERON_INVALID: Final[int] = -1
        OUTPUT_OFF: Final[int] = 0
        OUTPUT_ON: Final[int] = 1
        OUTPUT_INVALID: Final[int] = -1
        # --- (end of YRelay return codes)

    # --- (YRelay attributes declaration)
    _state: int
    _stateAtPowerOn: int
    _maxTimeOnStateA: int
    _maxTimeOnStateB: int
    _output: int
    _pulseTimer: int
    _delayedPulseTimer: YDelayedPulse
    _countdown: int
    _valueCallback: YRelayValueCallback
    _firm: int
    # --- (end of YRelay attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'Relay'
        # --- (YRelay constructor)
        self._state = YRelay.STATE_INVALID
        self._stateAtPowerOn = YRelay.STATEATPOWERON_INVALID
        self._maxTimeOnStateA = YRelay.MAXTIMEONSTATEA_INVALID
        self._maxTimeOnStateB = YRelay.MAXTIMEONSTATEB_INVALID
        self._output = YRelay.OUTPUT_INVALID
        self._pulseTimer = YRelay.PULSETIMER_INVALID
        self._delayedPulseTimer = YRelay.DELAYEDPULSETIMER_INVALID
        self._countdown = YRelay.COUNTDOWN_INVALID
        self._firm = 0
        # --- (end of YRelay constructor)

    # --- (YRelay implementation)

    @staticmethod
    def FirstRelay() -> Union[YRelay, None]:
        """
        Starts the enumeration of relays currently accessible.
        Use the method YRelay.nextRelay() to iterate on
        next relays.

        @return a pointer to a YRelay object, corresponding to
                the first relay currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('Relay')
        if not next_hwid:
            return None
        return YRelay.FindRelay(hwid2str(next_hwid))

    @staticmethod
    def FirstRelayInContext(yctx: YAPIContext) -> Union[YRelay, None]:
        """
        Starts the enumeration of relays currently accessible.
        Use the method YRelay.nextRelay() to iterate on
        next relays.

        @param yctx : a YAPI context.

        @return a pointer to a YRelay object, corresponding to
                the first relay currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('Relay')
        if not next_hwid:
            return None
        return YRelay.FindRelayInContext(yctx, hwid2str(next_hwid))

    def nextRelay(self):
        """
        Continues the enumeration of relays started using yFirstRelay().
        Caution: You can't make any assumption about the returned relays order.
        If you want to find a specific a relay, use Relay.findRelay()
        and a hardwareID or a logical name.

        @return a pointer to a YRelay object, corresponding to
                a relay currently online, or a None pointer
                if there are no more relays to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YRelay.FindRelayInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'state' in json_val:
            self._state = json_val["state"] > 0
        if 'stateAtPowerOn' in json_val:
            self._stateAtPowerOn = json_val["stateAtPowerOn"]
        if 'maxTimeOnStateA' in json_val:
            self._maxTimeOnStateA = json_val["maxTimeOnStateA"]
        if 'maxTimeOnStateB' in json_val:
            self._maxTimeOnStateB = json_val["maxTimeOnStateB"]
        if 'output' in json_val:
            self._output = json_val["output"] > 0
        if 'pulseTimer' in json_val:
            self._pulseTimer = json_val["pulseTimer"]
        if 'delayedPulseTimer' in json_val:
            self._delayedPulseTimer = json_val["delayedPulseTimer"]
        if 'countdown' in json_val:
            self._countdown = json_val["countdown"]
        super()._parseAttr(json_val)

    async def get_state(self) -> int:
        """
        Returns the state of the relays (A for the idle position, B for the active position).

        @return either YRelay.STATE_A or YRelay.STATE_B, according to the state of the relays (A for the
        idle position, B for the active position)

        On failure, throws an exception or returns YRelay.STATE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.STATE_INVALID
        res = self._state
        return res

    async def set_state(self, newval: int) -> int:
        """
        Changes the state of the relays (A for the idle position, B for the active position).

        @param newval : either YRelay.STATE_A or YRelay.STATE_B, according to the state of the relays (A
        for the idle position, B for the active position)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return await self._setAttr("state", rest_val)

    async def get_stateAtPowerOn(self) -> int:
        """
        Returns the state of the relays at device startup (A for the idle position,
        B for the active position, UNCHANGED to leave the relay state as is).

        @return a value among YRelay.STATEATPOWERON_UNCHANGED, YRelay.STATEATPOWERON_A and
        YRelay.STATEATPOWERON_B corresponding to the state of the relays at device startup (A for the idle position,
                B for the active position, UNCHANGED to leave the relay state as is)

        On failure, throws an exception or returns YRelay.STATEATPOWERON_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.STATEATPOWERON_INVALID
        res = self._stateAtPowerOn
        return res

    async def set_stateAtPowerOn(self, newval: int) -> int:
        """
        Changes the state of the relays at device startup (A for the idle position,
        B for the active position, UNCHANGED to leave the relay state as is).
        Remember to call the matching module saveToFlash()
        method, otherwise this call will have no effect.

        @param newval : a value among YRelay.STATEATPOWERON_UNCHANGED, YRelay.STATEATPOWERON_A and
        YRelay.STATEATPOWERON_B corresponding to the state of the relays at device startup (A for the idle position,
                B for the active position, UNCHANGED to leave the relay state as is)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("stateAtPowerOn", rest_val)

    async def get_maxTimeOnStateA(self) -> int:
        """
        Returns the maximum time (ms) allowed for the relay to stay in state
        A before automatically switching back in to B state. Zero means no time limit.

        @return an integer corresponding to the maximum time (ms) allowed for the relay to stay in state
                A before automatically switching back in to B state

        On failure, throws an exception or returns YRelay.MAXTIMEONSTATEA_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.MAXTIMEONSTATEA_INVALID
        res = self._maxTimeOnStateA
        return res

    async def set_maxTimeOnStateA(self, newval: int) -> int:
        """
        Changes the maximum time (ms) allowed for the relay to stay in state A
        before automatically switching back in to B state. Use zero for no time limit.
        Remember to call the saveToFlash()
        method of the module if the modification must be kept.

        @param newval : an integer corresponding to the maximum time (ms) allowed for the relay to stay in state A
                before automatically switching back in to B state

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("maxTimeOnStateA", rest_val)

    async def get_maxTimeOnStateB(self) -> int:
        """
        Retourne the maximum time (ms) allowed for the relay to stay in state B
        before automatically switching back in to A state. Zero means no time limit.

        @return an integer

        On failure, throws an exception or returns YRelay.MAXTIMEONSTATEB_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.MAXTIMEONSTATEB_INVALID
        res = self._maxTimeOnStateB
        return res

    async def set_maxTimeOnStateB(self, newval: int) -> int:
        """
        Changes the maximum time (ms) allowed for the relay to stay in state B before
        automatically switching back in to A state. Use zero for no time limit.
        Remember to call the saveToFlash()
        method of the module if the modification must be kept.

        @param newval : an integer corresponding to the maximum time (ms) allowed for the relay to stay in
        state B before
                automatically switching back in to A state

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("maxTimeOnStateB", rest_val)

    async def get_output(self) -> int:
        """
        Returns the output state of the relays, when used as a simple switch (single throw).

        @return either YRelay.OUTPUT_OFF or YRelay.OUTPUT_ON, according to the output state of the relays,
        when used as a simple switch (single throw)

        On failure, throws an exception or returns YRelay.OUTPUT_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.OUTPUT_INVALID
        res = self._output
        return res

    async def set_output(self, newval: int) -> int:
        """
        Changes the output state of the relays, when used as a simple switch (single throw).

        @param newval : either YRelay.OUTPUT_OFF or YRelay.OUTPUT_ON, according to the output state of the
        relays, when used as a simple switch (single throw)

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return await self._setAttr("output", rest_val)

    async def get_pulseTimer(self) -> int:
        """
        Returns the number of milliseconds remaining before the relays is returned to idle position
        (state A), during a measured pulse generation. When there is no ongoing pulse, returns zero.

        @return an integer corresponding to the number of milliseconds remaining before the relays is
        returned to idle position
                (state A), during a measured pulse generation

        On failure, throws an exception or returns YRelay.PULSETIMER_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.PULSETIMER_INVALID
        res = self._pulseTimer
        return res

    async def set_pulseTimer(self, newval: int) -> int:
        rest_val = str(newval)
        return await self._setAttr("pulseTimer", rest_val)

    async def pulse(self, ms_duration) -> int:
        """
        Sets the relay to output B (active) for a specified duration, then brings it
        automatically back to output A (idle state).

        @param ms_duration : pulse duration, in milliseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(ms_duration)
        return await self._setAttr("pulseTimer", rest_val)

    async def get_delayedPulseTimer(self) -> YDelayedPulse:
        res: Union[YDelayedPulse, None]
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.DELAYEDPULSETIMER_INVALID
        res = self._delayedPulseTimer
        return res

    async def set_delayedPulseTimer(self, newval: YDelayedPulse) -> int:
        rest_val = str(newval.target) + ":" + str(newval.ms)
        return await self._setAttr("delayedPulseTimer", rest_val)

    async def delayedPulse(self, ms_delay, ms_duration) -> int:
        """
        Schedules a pulse.

        @param ms_delay : waiting time before the pulse, in milliseconds
        @param ms_duration : pulse duration, in milliseconds

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(ms_delay) + ":" + str(ms_duration)
        return await self._setAttr("delayedPulseTimer", rest_val)

    async def get_countdown(self) -> int:
        """
        Returns the number of milliseconds remaining before a pulse (delayedPulse() call)
        When there is no scheduled pulse, returns zero.

        @return an integer corresponding to the number of milliseconds remaining before a pulse (delayedPulse() call)
                When there is no scheduled pulse, returns zero

        On failure, throws an exception or returns YRelay.COUNTDOWN_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YRelay.COUNTDOWN_INVALID
        res = self._countdown
        return res

    @staticmethod
    def FindRelay(func: str) -> YRelay:
        """
        Retrieves a relay for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the relay is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRelay.isOnline() to test if the relay is
        indeed online at a given time. In case of ambiguity when looking for
        a relay by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the relay, for instance
                YLTCHRL1.relay1.

        @return a YRelay object allowing you to drive the relay.
        """
        obj: Union[YRelay, None]
        obj = YFunction._FindFromCache("Relay", func)
        if obj is None:
            obj = YRelay(YAPI, func)
            YFunction._AddToCache("Relay", func, obj)
        return obj

    @staticmethod
    def FindRelayInContext(yctx: YAPIContext, func: str) -> YRelay:
        """
        Retrieves a relay for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the relay is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YRelay.isOnline() to test if the relay is
        indeed online at a given time. In case of ambiguity when looking for
        a relay by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the relay, for instance
                YLTCHRL1.relay1.

        @return a YRelay object allowing you to drive the relay.
        """
        obj: Union[YRelay, None]
        obj = YFunction._FindFromCacheInContext(yctx, "Relay", func)
        if obj is None:
            obj = YRelay(yctx, func)
            YFunction._AddToCache("Relay", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YRelayValueCallback) -> int:
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

    async def toggle(self) -> int:
        """
        Switch the relay to the opposite state.

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        sta: int
        fw: str
        mo: Union[YModule, None]
        if self._firm == 0:
            mo = await self.get_module()
            fw = await mo.get_firmwareRelease()
            if fw == YModule.FIRMWARERELEASE_INVALID:
                return YRelay.STATE_INVALID
            self._firm = YAPI._atoi(fw)
        if self._firm < 34921:
            sta = await self.get_state()
            if sta == YRelay.STATE_INVALID:
                return YRelay.STATE_INVALID
            if sta == YRelay.STATE_B:
                await self.set_state(YRelay.STATE_A)
            else:
                await self.set_state(YRelay.STATE_B)
            return YAPI.SUCCESS
        else:
            return await self._setAttr("state", "X")

    # --- (end of YRelay implementation)

