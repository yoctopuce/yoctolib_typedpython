# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YStepperMotor
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
Yoctopuce library: Asyncio implementation of YStepperMotor
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
    YAPIContext, YAPI, YAPI_Exception, HwId, hwid2str, YFunction, xarray
)

# --- (YStepperMotor class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YStepperMotorValueCallback = Union[Callable[['YStepperMotor', str], Awaitable[None]], None]
    except TypeError:
        YStepperMotorValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YStepperMotor(YFunction):
    """
    The YStepperMotor class allows you to drive a stepper motor.

    """
    # --- (end of YStepperMotor class start)
    if not _IS_MICROPYTHON:
        # --- (YStepperMotor return codes)
        DIAGS_INVALID: Final[int] = YAPI.INVALID_UINT
        STEPPOS_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        SPEED_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        PULLINSPEED_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        MAXACCEL_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        MAXSPEED_INVALID: Final[float] = YAPI.INVALID_DOUBLE
        OVERCURRENT_INVALID: Final[int] = YAPI.INVALID_UINT
        TCURRSTOP_INVALID: Final[int] = YAPI.INVALID_UINT
        TCURRRUN_INVALID: Final[int] = YAPI.INVALID_UINT
        ALERTMODE_INVALID: Final[str] = YAPI.INVALID_STRING
        AUXMODE_INVALID: Final[str] = YAPI.INVALID_STRING
        AUXSIGNAL_INVALID: Final[int] = YAPI.INVALID_INT
        COMMAND_INVALID: Final[str] = YAPI.INVALID_STRING
        MOTORSTATE_ABSENT: Final[int] = 0
        MOTORSTATE_ALERT: Final[int] = 1
        MOTORSTATE_HI_Z: Final[int] = 2
        MOTORSTATE_STOP: Final[int] = 3
        MOTORSTATE_RUN: Final[int] = 4
        MOTORSTATE_BATCH: Final[int] = 5
        MOTORSTATE_INVALID: Final[int] = -1
        STEPPING_MICROSTEP16: Final[int] = 0
        STEPPING_MICROSTEP8: Final[int] = 1
        STEPPING_MICROSTEP4: Final[int] = 2
        STEPPING_HALFSTEP: Final[int] = 3
        STEPPING_FULLSTEP: Final[int] = 4
        STEPPING_INVALID: Final[int] = -1
        # --- (end of YStepperMotor return codes)

    # --- (YStepperMotor attributes declaration)
    _motorState: int
    _diags: int
    _stepPos: float
    _speed: float
    _pullinSpeed: float
    _maxAccel: float
    _maxSpeed: float
    _stepping: int
    _overcurrent: int
    _tCurrStop: int
    _tCurrRun: int
    _alertMode: str
    _auxMode: str
    _auxSignal: int
    _command: str
    _valueCallback: YStepperMotorValueCallback
    # --- (end of YStepperMotor attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'StepperMotor'
        # --- (YStepperMotor constructor)
        self._motorState = YStepperMotor.MOTORSTATE_INVALID
        self._diags = YStepperMotor.DIAGS_INVALID
        self._stepPos = YStepperMotor.STEPPOS_INVALID
        self._speed = YStepperMotor.SPEED_INVALID
        self._pullinSpeed = YStepperMotor.PULLINSPEED_INVALID
        self._maxAccel = YStepperMotor.MAXACCEL_INVALID
        self._maxSpeed = YStepperMotor.MAXSPEED_INVALID
        self._stepping = YStepperMotor.STEPPING_INVALID
        self._overcurrent = YStepperMotor.OVERCURRENT_INVALID
        self._tCurrStop = YStepperMotor.TCURRSTOP_INVALID
        self._tCurrRun = YStepperMotor.TCURRRUN_INVALID
        self._alertMode = YStepperMotor.ALERTMODE_INVALID
        self._auxMode = YStepperMotor.AUXMODE_INVALID
        self._auxSignal = YStepperMotor.AUXSIGNAL_INVALID
        self._command = YStepperMotor.COMMAND_INVALID
        # --- (end of YStepperMotor constructor)

    # --- (YStepperMotor implementation)

    @staticmethod
    def FirstStepperMotor() -> Union[YStepperMotor, None]:
        """
        Starts the enumeration of stepper motors currently accessible.
        Use the method YStepperMotor.nextStepperMotor() to iterate on
        next stepper motors.

        @return a pointer to a YStepperMotor object, corresponding to
                the first stepper motor currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('StepperMotor')
        if not next_hwid:
            return None
        return YStepperMotor.FindStepperMotor(hwid2str(next_hwid))

    @staticmethod
    def FirstStepperMotorInContext(yctx: YAPIContext) -> Union[YStepperMotor, None]:
        """
        Starts the enumeration of stepper motors currently accessible.
        Use the method YStepperMotor.nextStepperMotor() to iterate on
        next stepper motors.

        @param yctx : a YAPI context.

        @return a pointer to a YStepperMotor object, corresponding to
                the first stepper motor currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('StepperMotor')
        if not next_hwid:
            return None
        return YStepperMotor.FindStepperMotorInContext(yctx, hwid2str(next_hwid))

    def nextStepperMotor(self):
        """
        Continues the enumeration of stepper motors started using yFirstStepperMotor().
        Caution: You can't make any assumption about the returned stepper motors order.
        If you want to find a specific a stepper motor, use StepperMotor.findStepperMotor()
        and a hardwareID or a logical name.

        @return a pointer to a YStepperMotor object, corresponding to
                a stepper motor currently online, or a None pointer
                if there are no more stepper motors to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YStepperMotor.FindStepperMotorInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'motorState' in json_val:
            self._motorState = json_val["motorState"]
        if 'diags' in json_val:
            self._diags = json_val["diags"]
        if 'stepPos' in json_val:
            self._stepPos = json_val["stepPos"] / 16.0
        if 'speed' in json_val:
            self._speed = round(json_val["speed"] / 65.536) / 1000.0
        if 'pullinSpeed' in json_val:
            self._pullinSpeed = round(json_val["pullinSpeed"] / 65.536) / 1000.0
        if 'maxAccel' in json_val:
            self._maxAccel = round(json_val["maxAccel"] / 65.536) / 1000.0
        if 'maxSpeed' in json_val:
            self._maxSpeed = round(json_val["maxSpeed"] / 65.536) / 1000.0
        if 'stepping' in json_val:
            self._stepping = json_val["stepping"]
        if 'overcurrent' in json_val:
            self._overcurrent = json_val["overcurrent"]
        if 'tCurrStop' in json_val:
            self._tCurrStop = json_val["tCurrStop"]
        if 'tCurrRun' in json_val:
            self._tCurrRun = json_val["tCurrRun"]
        if 'alertMode' in json_val:
            self._alertMode = json_val["alertMode"]
        if 'auxMode' in json_val:
            self._auxMode = json_val["auxMode"]
        if 'auxSignal' in json_val:
            self._auxSignal = json_val["auxSignal"]
        if 'command' in json_val:
            self._command = json_val["command"]
        super()._parseAttr(json_val)

    async def get_motorState(self) -> int:
        """
        Returns the motor working state.

        @return a value among YStepperMotor.MOTORSTATE_ABSENT, YStepperMotor.MOTORSTATE_ALERT,
        YStepperMotor.MOTORSTATE_HI_Z, YStepperMotor.MOTORSTATE_STOP, YStepperMotor.MOTORSTATE_RUN and
        YStepperMotor.MOTORSTATE_BATCH corresponding to the motor working state

        On failure, throws an exception or returns YStepperMotor.MOTORSTATE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.MOTORSTATE_INVALID
        res = self._motorState
        return res

    async def get_diags(self) -> int:
        """
        Returns the stepper motor controller diagnostics, as a bitmap.

        @return an integer corresponding to the stepper motor controller diagnostics, as a bitmap

        On failure, throws an exception or returns YStepperMotor.DIAGS_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.DIAGS_INVALID
        res = self._diags
        return res

    async def set_stepPos(self, newval: float) -> int:
        """
        Changes the current logical motor position, measured in steps.
        This command does not cause any motor move, as its purpose is only to set up
        the origin of the position counter. The fractional part of the position,
        that corresponds to the physical position of the rotor, is not changed.
        To trigger a motor move, use methods moveTo() or moveRel()
        instead.

        @param newval : a floating point number corresponding to the current logical motor position, measured in steps

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "%.2f" % (round(newval * 100.0, 1)/100.0)
        return await self._setAttr("stepPos", rest_val)

    async def get_stepPos(self) -> float:
        """
        Returns the current logical motor position, measured in steps.
        The value may include a fractional part when micro-stepping is in use.

        @return a floating point number corresponding to the current logical motor position, measured in steps

        On failure, throws an exception or returns YStepperMotor.STEPPOS_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.STEPPOS_INVALID
        res = self._stepPos
        return res

    async def get_speed(self) -> float:
        """
        Returns current motor speed, measured in steps per second.
        To change speed, use method changeSpeed().

        @return a floating point number corresponding to current motor speed, measured in steps per second

        On failure, throws an exception or returns YStepperMotor.SPEED_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.SPEED_INVALID
        res = self._speed
        return res

    async def set_pullinSpeed(self, newval: float) -> int:
        """
        Changes the motor speed immediately reachable from stop state, measured in steps per second.

        @param newval : a floating point number corresponding to the motor speed immediately reachable from
        stop state, measured in steps per second

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return await self._setAttr("pullinSpeed", rest_val)

    async def get_pullinSpeed(self) -> float:
        """
        Returns the motor speed immediately reachable from stop state, measured in steps per second.

        @return a floating point number corresponding to the motor speed immediately reachable from stop
        state, measured in steps per second

        On failure, throws an exception or returns YStepperMotor.PULLINSPEED_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.PULLINSPEED_INVALID
        res = self._pullinSpeed
        return res

    async def set_maxAccel(self, newval: float) -> int:
        """
        Changes the maximal motor acceleration, measured in steps per second^2.

        @param newval : a floating point number corresponding to the maximal motor acceleration, measured
        in steps per second^2

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return await self._setAttr("maxAccel", rest_val)

    async def get_maxAccel(self) -> float:
        """
        Returns the maximal motor acceleration, measured in steps per second^2.

        @return a floating point number corresponding to the maximal motor acceleration, measured in steps per second^2

        On failure, throws an exception or returns YStepperMotor.MAXACCEL_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.MAXACCEL_INVALID
        res = self._maxAccel
        return res

    async def set_maxSpeed(self, newval: float) -> int:
        """
        Changes the maximal motor speed, measured in steps per second.

        @param newval : a floating point number corresponding to the maximal motor speed, measured in steps per second

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(int(round(newval * 65536.0, 1)))
        return await self._setAttr("maxSpeed", rest_val)

    async def get_maxSpeed(self) -> float:
        """
        Returns the maximal motor speed, measured in steps per second.

        @return a floating point number corresponding to the maximal motor speed, measured in steps per second

        On failure, throws an exception or returns YStepperMotor.MAXSPEED_INVALID.
        """
        res: float
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.MAXSPEED_INVALID
        res = self._maxSpeed
        return res

    async def get_stepping(self) -> int:
        """
        Returns the stepping mode used to drive the motor.

        @return a value among YStepperMotor.STEPPING_MICROSTEP16, YStepperMotor.STEPPING_MICROSTEP8,
        YStepperMotor.STEPPING_MICROSTEP4, YStepperMotor.STEPPING_HALFSTEP and
        YStepperMotor.STEPPING_FULLSTEP corresponding to the stepping mode used to drive the motor

        On failure, throws an exception or returns YStepperMotor.STEPPING_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.STEPPING_INVALID
        res = self._stepping
        return res

    async def set_stepping(self, newval: int) -> int:
        """
        Changes the stepping mode used to drive the motor.

        @param newval : a value among YStepperMotor.STEPPING_MICROSTEP16,
        YStepperMotor.STEPPING_MICROSTEP8, YStepperMotor.STEPPING_MICROSTEP4,
        YStepperMotor.STEPPING_HALFSTEP and YStepperMotor.STEPPING_FULLSTEP corresponding to the stepping
        mode used to drive the motor

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("stepping", rest_val)

    async def get_overcurrent(self) -> int:
        """
        Returns the overcurrent alert and emergency stop threshold, measured in mA.

        @return an integer corresponding to the overcurrent alert and emergency stop threshold, measured in mA

        On failure, throws an exception or returns YStepperMotor.OVERCURRENT_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.OVERCURRENT_INVALID
        res = self._overcurrent
        return res

    async def set_overcurrent(self, newval: int) -> int:
        """
        Changes the overcurrent alert and emergency stop threshold, measured in mA.

        @param newval : an integer corresponding to the overcurrent alert and emergency stop threshold, measured in mA

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("overcurrent", rest_val)

    async def get_tCurrStop(self) -> int:
        """
        Returns the torque regulation current when the motor is stopped, measured in mA.

        @return an integer corresponding to the torque regulation current when the motor is stopped, measured in mA

        On failure, throws an exception or returns YStepperMotor.TCURRSTOP_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.TCURRSTOP_INVALID
        res = self._tCurrStop
        return res

    async def set_tCurrStop(self, newval: int) -> int:
        """
        Changes the torque regulation current when the motor is stopped, measured in mA.

        @param newval : an integer corresponding to the torque regulation current when the motor is
        stopped, measured in mA

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("tCurrStop", rest_val)

    async def get_tCurrRun(self) -> int:
        """
        Returns the torque regulation current when the motor is running, measured in mA.

        @return an integer corresponding to the torque regulation current when the motor is running, measured in mA

        On failure, throws an exception or returns YStepperMotor.TCURRRUN_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.TCURRRUN_INVALID
        res = self._tCurrRun
        return res

    async def set_tCurrRun(self, newval: int) -> int:
        """
        Changes the torque regulation current when the motor is running, measured in mA.

        @param newval : an integer corresponding to the torque regulation current when the motor is
        running, measured in mA

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("tCurrRun", rest_val)

    async def get_alertMode(self) -> str:
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.ALERTMODE_INVALID
        res = self._alertMode
        return res

    async def set_alertMode(self, newval: str) -> int:
        rest_val = newval
        return await self._setAttr("alertMode", rest_val)

    async def get_auxMode(self) -> str:
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.AUXMODE_INVALID
        res = self._auxMode
        return res

    async def set_auxMode(self, newval: str) -> int:
        rest_val = newval
        return await self._setAttr("auxMode", rest_val)

    async def get_auxSignal(self) -> int:
        """
        Returns the current value of the signal generated on the auxiliary output.

        @return an integer corresponding to the current value of the signal generated on the auxiliary output

        On failure, throws an exception or returns YStepperMotor.AUXSIGNAL_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.AUXSIGNAL_INVALID
        res = self._auxSignal
        return res

    async def set_auxSignal(self, newval: int) -> int:
        """
        Changes the value of the signal generated on the auxiliary output.
        Acceptable values depend on the auxiliary output signal type configured.

        @param newval : an integer corresponding to the value of the signal generated on the auxiliary output

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("auxSignal", rest_val)

    async def get_command(self) -> str:
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YStepperMotor.COMMAND_INVALID
        res = self._command
        return res

    async def set_command(self, newval: str) -> int:
        rest_val = newval
        return await self._setAttr("command", rest_val)

    @staticmethod
    def FindStepperMotor(func: str) -> YStepperMotor:
        """
        Retrieves a stepper motor for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the stepper motor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YStepperMotor.isOnline() to test if the stepper motor is
        indeed online at a given time. In case of ambiguity when looking for
        a stepper motor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the stepper motor, for instance
                MyDevice.stepperMotor1.

        @return a YStepperMotor object allowing you to drive the stepper motor.
        """
        obj: Union[YStepperMotor, None]
        obj = YFunction._FindFromCache("StepperMotor", func)
        if obj is None:
            obj = YStepperMotor(YAPI, func)
            YFunction._AddToCache("StepperMotor", func, obj)
        return obj

    @staticmethod
    def FindStepperMotorInContext(yctx: YAPIContext, func: str) -> YStepperMotor:
        """
        Retrieves a stepper motor for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the stepper motor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YStepperMotor.isOnline() to test if the stepper motor is
        indeed online at a given time. In case of ambiguity when looking for
        a stepper motor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the stepper motor, for instance
                MyDevice.stepperMotor1.

        @return a YStepperMotor object allowing you to drive the stepper motor.
        """
        obj: Union[YStepperMotor, None]
        obj = YFunction._FindFromCacheInContext(yctx, "StepperMotor", func)
        if obj is None:
            obj = YStepperMotor(yctx, func)
            YFunction._AddToCache("StepperMotor", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YStepperMotorValueCallback) -> int:
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

    async def sendCommand(self, command: str) -> int:
        id: str
        url: str
        retBin: xarray
        res: int
        id = await self.get_functionId()
        id = id[12: 12 + 1]
        url = "cmd.txt?%s=%s" % (id, command)
        # //may throw an exception
        retBin = await self._download(url)
        res = retBin[0]
        if res < 58:
            if not (res == 48):
                self._throw(YAPI.DEVICE_BUSY, "Motor command pipeline is full, try again later")
                return YAPI.DEVICE_BUSY
        else:
            if not (res == 48):
                self._throw(YAPI.IO_ERROR, "Motor command failed permanently")
                return YAPI.IO_ERROR
        return YAPI.SUCCESS

    async def reset(self) -> int:
        """
        Reinitialize the controller and clear all alert flags.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("Z")

    async def findHomePosition(self, speed: float) -> int:
        """
        Starts the motor backward at the specified speed, to search for the motor home position.

        @param speed : desired speed, in steps per second.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.sendCommand("H%d" % (int(round(1000*speed))))

    async def changeSpeed(self, speed: float) -> int:
        """
        Starts the motor at a given speed. The time needed to reach the requested speed
        will depend on the acceleration parameters configured for the motor.

        @param speed : desired speed, in steps per second. The minimal non-zero speed
                is 0.001 pulse per second.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.sendCommand("R%d" % (int(round(1000*speed))))

    async def moveTo(self, absPos: float) -> int:
        """
        Starts the motor to reach a given absolute position. The time needed to reach the requested
        position will depend on the acceleration and max speed parameters configured for
        the motor.

        @param absPos : absolute position, measured in steps from the origin.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.sendCommand("M%d" % (int(round(16*absPos))))

    async def moveRel(self, relPos: float) -> int:
        """
        Starts the motor to reach a given relative position. The time needed to reach the requested
        position will depend on the acceleration and max speed parameters configured for
        the motor.

        @param relPos : relative position, measured in steps from the current position.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.sendCommand("m%d" % (int(round(16*relPos))))

    async def moveRelSlow(self, relPos: float, maxSpeed: float) -> int:
        """
        Starts the motor to reach a given relative position, keeping the speed under the
        specified limit. The time needed to reach the requested position will depend on
        the acceleration parameters configured for the motor.

        @param relPos : relative position, measured in steps from the current position.
        @param maxSpeed : limit speed, in steps per second.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.sendCommand("m%d@%d" % (int(round(16*relPos)), int(round(1000*maxSpeed))))

    async def pause(self, waitMs: int) -> int:
        """
        Keep the motor in the same state for the specified amount of time, before processing next command.

        @param waitMs : wait time, specified in milliseconds.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.sendCommand("_%d" % waitMs)

    async def emergencyStop(self) -> int:
        """
        Stops the motor with an emergency alert, without taking any additional precaution.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("!")

    async def alertStepOut(self) -> int:
        """
        Move one step in the direction opposite the direction set when the most recent alert was raised.
        The move occurs even if the system is still in alert mode (end switch depressed). Caution.
        use this function with great care as it may cause mechanical damages !

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command(".")

    async def alertStepDir(self, dir: int) -> int:
        """
        Move one single step in the selected direction without regards to end switches.
        The move occurs even if the system is still in alert mode (end switch depressed). Caution.
        use this function with great care as it may cause mechanical damages !

        @param dir : Value +1 or -1, according to the desired direction of the move

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        if not (dir != 0):
            self._throw(YAPI.INVALID_ARGUMENT, "direction must be +1 or -1")
            return YAPI.INVALID_ARGUMENT
        if dir > 0:
            return await self.set_command(".+")
        return await self.set_command(".-")

    async def abortAndBrake(self) -> int:
        """
        Stops the motor smoothly as soon as possible, without waiting for ongoing move completion.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("B")

    async def abortAndHiZ(self) -> int:
        """
        Turn the controller into Hi-Z mode immediately, without waiting for ongoing move completion.

        @return YAPI.SUCCESS if the call succeeds.
                On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("z")

    # --- (end of YStepperMotor implementation)

