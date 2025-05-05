# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  Asyncio implementation of YBluetoothLink
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
Yoctopuce library: Asyncio implementation of YBluetoothLink
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
    YAPIContext, YAPI, YAPI_Exception, HwId, hwid2str, YFunction
)

# --- (YBluetoothLink class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YBluetoothLinkValueCallback = Union[Callable[['YBluetoothLink', str], Awaitable[None]], None]
    except TypeError:
        YBluetoothLinkValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YBluetoothLink(YFunction):
    """
    BluetoothLink function provides control over Bluetooth link
    and status for devices that are Bluetooth-enabled.

    """
    # --- (end of YBluetoothLink class start)
    if not _IS_MICROPYTHON:
        # --- (YBluetoothLink return codes)
        OWNADDRESS_INVALID: Final[str] = YAPI.INVALID_STRING
        PAIRINGPIN_INVALID: Final[str] = YAPI.INVALID_STRING
        REMOTEADDRESS_INVALID: Final[str] = YAPI.INVALID_STRING
        REMOTENAME_INVALID: Final[str] = YAPI.INVALID_STRING
        PREAMPLIFIER_INVALID: Final[int] = YAPI.INVALID_UINT
        VOLUME_INVALID: Final[int] = YAPI.INVALID_UINT
        LINKQUALITY_INVALID: Final[int] = YAPI.INVALID_UINT
        COMMAND_INVALID: Final[str] = YAPI.INVALID_STRING
        MUTE_FALSE: Final[int] = 0
        MUTE_TRUE: Final[int] = 1
        MUTE_INVALID: Final[int] = -1
        LINKSTATE_DOWN: Final[int] = 0
        LINKSTATE_FREE: Final[int] = 1
        LINKSTATE_SEARCH: Final[int] = 2
        LINKSTATE_EXISTS: Final[int] = 3
        LINKSTATE_LINKED: Final[int] = 4
        LINKSTATE_PLAY: Final[int] = 5
        LINKSTATE_INVALID: Final[int] = -1
        # --- (end of YBluetoothLink return codes)

    # --- (YBluetoothLink attributes declaration)
    _ownAddress: str
    _pairingPin: str
    _remoteAddress: str
    _remoteName: str
    _mute: int
    _preAmplifier: int
    _volume: int
    _linkState: int
    _linkQuality: int
    _command: str
    _valueCallback: YBluetoothLinkValueCallback
    # --- (end of YBluetoothLink attributes declaration)


    def __init__(self, yctx: YAPIContext, func: str):
        super().__init__(yctx, func)
        self._className = 'BluetoothLink'
        # --- (YBluetoothLink constructor)
        self._ownAddress = YBluetoothLink.OWNADDRESS_INVALID
        self._pairingPin = YBluetoothLink.PAIRINGPIN_INVALID
        self._remoteAddress = YBluetoothLink.REMOTEADDRESS_INVALID
        self._remoteName = YBluetoothLink.REMOTENAME_INVALID
        self._mute = YBluetoothLink.MUTE_INVALID
        self._preAmplifier = YBluetoothLink.PREAMPLIFIER_INVALID
        self._volume = YBluetoothLink.VOLUME_INVALID
        self._linkState = YBluetoothLink.LINKSTATE_INVALID
        self._linkQuality = YBluetoothLink.LINKQUALITY_INVALID
        self._command = YBluetoothLink.COMMAND_INVALID
        # --- (end of YBluetoothLink constructor)

    # --- (YBluetoothLink implementation)

    @staticmethod
    def FirstBluetoothLink() -> Union[YBluetoothLink, None]:
        """
        Starts the enumeration of Bluetooth sound controllers currently accessible.
        Use the method YBluetoothLink.nextBluetoothLink() to iterate on
        next Bluetooth sound controllers.

        @return a pointer to a YBluetoothLink object, corresponding to
                the first Bluetooth sound controller currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = YAPI._yHash.getFirstHardwareId('BluetoothLink')
        if not next_hwid:
            return None
        return YBluetoothLink.FindBluetoothLink(hwid2str(next_hwid))

    @staticmethod
    def FirstBluetoothLinkInContext(yctx: YAPIContext) -> Union[YBluetoothLink, None]:
        """
        Starts the enumeration of Bluetooth sound controllers currently accessible.
        Use the method YBluetoothLink.nextBluetoothLink() to iterate on
        next Bluetooth sound controllers.

        @param yctx : a YAPI context.

        @return a pointer to a YBluetoothLink object, corresponding to
                the first Bluetooth sound controller currently online, or a None pointer
                if there are none.
        """
        next_hwid: Union[HwId, None] = yctx._yHash.getFirstHardwareId('BluetoothLink')
        if not next_hwid:
            return None
        return YBluetoothLink.FindBluetoothLinkInContext(yctx, hwid2str(next_hwid))

    def nextBluetoothLink(self):
        """
        Continues the enumeration of Bluetooth sound controllers started using yFirstBluetoothLink().
        Caution: You can't make any assumption about the returned Bluetooth sound controllers order.
        If you want to find a specific a Bluetooth sound controller, use BluetoothLink.findBluetoothLink()
        and a hardwareID or a logical name.

        @return a pointer to a YBluetoothLink object, corresponding to
                a Bluetooth sound controller currently online, or a None pointer
                if there are no more Bluetooth sound controllers to enumerate.
        """
        next_hwid: Union[HwId, None] = None
        try:
            hwid: HwId = self._yapi._yHash.resolveHwID(self._className, self._func)
            next_hwid = self._yapi._yHash.getNextHardwareId(self._className, hwid)
        except YAPI_Exception:
            pass
        if not next_hwid:
            return None
        return YBluetoothLink.FindBluetoothLinkInContext(self._yapi, hwid2str(next_hwid))

    def _parseAttr(self, json_val: dict) -> None:
        if 'ownAddress' in json_val:
            self._ownAddress = json_val["ownAddress"]
        if 'pairingPin' in json_val:
            self._pairingPin = json_val["pairingPin"]
        if 'remoteAddress' in json_val:
            self._remoteAddress = json_val["remoteAddress"]
        if 'remoteName' in json_val:
            self._remoteName = json_val["remoteName"]
        if 'mute' in json_val:
            self._mute = json_val["mute"] > 0
        if 'preAmplifier' in json_val:
            self._preAmplifier = json_val["preAmplifier"]
        if 'volume' in json_val:
            self._volume = json_val["volume"]
        if 'linkState' in json_val:
            self._linkState = json_val["linkState"]
        if 'linkQuality' in json_val:
            self._linkQuality = json_val["linkQuality"]
        if 'command' in json_val:
            self._command = json_val["command"]
        super()._parseAttr(json_val)

    async def get_ownAddress(self) -> str:
        """
        Returns the MAC-48 address of the bluetooth interface, which is unique on the bluetooth network.

        @return a string corresponding to the MAC-48 address of the bluetooth interface, which is unique on
        the bluetooth network

        On failure, throws an exception or returns YBluetoothLink.OWNADDRESS_INVALID.
        """
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.OWNADDRESS_INVALID
        res = self._ownAddress
        return res

    async def get_pairingPin(self) -> str:
        """
        Returns an opaque string if a PIN code has been configured in the device to access
        the SIM card, or an empty string if none has been configured or if the code provided
        was rejected by the SIM card.

        @return a string corresponding to an opaque string if a PIN code has been configured in the device to access
                the SIM card, or an empty string if none has been configured or if the code provided
                was rejected by the SIM card

        On failure, throws an exception or returns YBluetoothLink.PAIRINGPIN_INVALID.
        """
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.PAIRINGPIN_INVALID
        res = self._pairingPin
        return res

    async def set_pairingPin(self, newval: str) -> int:
        """
        Changes the PIN code used by the module for bluetooth pairing.
        Remember to call the saveToFlash() method of the module to save the
        new value in the device flash.

        @param newval : a string corresponding to the PIN code used by the module for bluetooth pairing

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return await self._setAttr("pairingPin", rest_val)

    async def get_remoteAddress(self) -> str:
        """
        Returns the MAC-48 address of the remote device to connect to.

        @return a string corresponding to the MAC-48 address of the remote device to connect to

        On failure, throws an exception or returns YBluetoothLink.REMOTEADDRESS_INVALID.
        """
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.REMOTEADDRESS_INVALID
        res = self._remoteAddress
        return res

    async def set_remoteAddress(self, newval: str) -> int:
        """
        Changes the MAC-48 address defining which remote device to connect to.
        Remember to call the saveToFlash()
        method of the module if the modification must be kept.

        @param newval : a string corresponding to the MAC-48 address defining which remote device to connect to

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return await self._setAttr("remoteAddress", rest_val)

    async def get_remoteName(self) -> str:
        """
        Returns the bluetooth name the remote device, if found on the bluetooth network.

        @return a string corresponding to the bluetooth name the remote device, if found on the bluetooth network

        On failure, throws an exception or returns YBluetoothLink.REMOTENAME_INVALID.
        """
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.REMOTENAME_INVALID
        res = self._remoteName
        return res

    async def get_mute(self) -> int:
        """
        Returns the state of the mute function.

        @return either YBluetoothLink.MUTE_FALSE or YBluetoothLink.MUTE_TRUE, according to the state of the
        mute function

        On failure, throws an exception or returns YBluetoothLink.MUTE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.MUTE_INVALID
        res = self._mute
        return res

    async def set_mute(self, newval: int) -> int:
        """
        Changes the state of the mute function. Remember to call the matching module
        saveToFlash() method to save the setting permanently.

        @param newval : either YBluetoothLink.MUTE_FALSE or YBluetoothLink.MUTE_TRUE, according to the
        state of the mute function

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = "1" if newval > 0 else "0"
        return await self._setAttr("mute", rest_val)

    async def get_preAmplifier(self) -> int:
        """
        Returns the audio pre-amplifier volume, in per cents.

        @return an integer corresponding to the audio pre-amplifier volume, in per cents

        On failure, throws an exception or returns YBluetoothLink.PREAMPLIFIER_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.PREAMPLIFIER_INVALID
        res = self._preAmplifier
        return res

    async def set_preAmplifier(self, newval: int) -> int:
        """
        Changes the audio pre-amplifier volume, in per cents.
        Remember to call the saveToFlash()
        method of the module if the modification must be kept.

        @param newval : an integer corresponding to the audio pre-amplifier volume, in per cents

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("preAmplifier", rest_val)

    async def get_volume(self) -> int:
        """
        Returns the connected headset volume, in per cents.

        @return an integer corresponding to the connected headset volume, in per cents

        On failure, throws an exception or returns YBluetoothLink.VOLUME_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.VOLUME_INVALID
        res = self._volume
        return res

    async def set_volume(self, newval: int) -> int:
        """
        Changes the connected headset volume, in per cents.

        @param newval : an integer corresponding to the connected headset volume, in per cents

        @return YAPI.SUCCESS if the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(newval)
        return await self._setAttr("volume", rest_val)

    async def get_linkState(self) -> int:
        """
        Returns the bluetooth link state.

        @return a value among YBluetoothLink.LINKSTATE_DOWN, YBluetoothLink.LINKSTATE_FREE,
        YBluetoothLink.LINKSTATE_SEARCH, YBluetoothLink.LINKSTATE_EXISTS, YBluetoothLink.LINKSTATE_LINKED
        and YBluetoothLink.LINKSTATE_PLAY corresponding to the bluetooth link state

        On failure, throws an exception or returns YBluetoothLink.LINKSTATE_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.LINKSTATE_INVALID
        res = self._linkState
        return res

    async def get_linkQuality(self) -> int:
        """
        Returns the bluetooth receiver signal strength, in pourcents, or 0 if no connection is established.

        @return an integer corresponding to the bluetooth receiver signal strength, in pourcents, or 0 if
        no connection is established

        On failure, throws an exception or returns YBluetoothLink.LINKQUALITY_INVALID.
        """
        res: int
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.LINKQUALITY_INVALID
        res = self._linkQuality
        return res

    async def get_command(self) -> str:
        res: str
        if self._cacheExpiration <= YAPI.GetTickCount():
            if await self.load(self._yapi.GetCacheValidity()) != YAPI.SUCCESS:
                return YBluetoothLink.COMMAND_INVALID
        res = self._command
        return res

    async def set_command(self, newval: str) -> int:
        rest_val = newval
        return await self._setAttr("command", rest_val)

    @staticmethod
    def FindBluetoothLink(func: str) -> YBluetoothLink:
        """
        Retrieves a Bluetooth sound controller for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the Bluetooth sound controller is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YBluetoothLink.isOnline() to test if the Bluetooth sound controller is
        indeed online at a given time. In case of ambiguity when looking for
        a Bluetooth sound controller by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the Bluetooth sound controller, for instance
                MyDevice.bluetoothLink1.

        @return a YBluetoothLink object allowing you to drive the Bluetooth sound controller.
        """
        obj: Union[YBluetoothLink, None]
        obj = YFunction._FindFromCache("BluetoothLink", func)
        if obj is None:
            obj = YBluetoothLink(YAPI, func)
            YFunction._AddToCache("BluetoothLink", func, obj)
        return obj

    @staticmethod
    def FindBluetoothLinkInContext(yctx: YAPIContext, func: str) -> YBluetoothLink:
        """
        Retrieves a Bluetooth sound controller for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the Bluetooth sound controller is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YBluetoothLink.isOnline() to test if the Bluetooth sound controller is
        indeed online at a given time. In case of ambiguity when looking for
        a Bluetooth sound controller by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the Bluetooth sound controller, for instance
                MyDevice.bluetoothLink1.

        @return a YBluetoothLink object allowing you to drive the Bluetooth sound controller.
        """
        obj: Union[YBluetoothLink, None]
        obj = YFunction._FindFromCacheInContext(yctx, "BluetoothLink", func)
        if obj is None:
            obj = YBluetoothLink(yctx, func)
            YFunction._AddToCache("BluetoothLink", func, obj)
        return obj

    if not _IS_MICROPYTHON:
        async def registerValueCallback(self, callback: YBluetoothLinkValueCallback) -> int:
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

    async def connect(self) -> int:
        """
        Attempt to connect to the previously selected remote device.

        @return YAPI.SUCCESS when the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("C")

    async def disconnect(self) -> int:
        """
        Disconnect from the previously selected remote device.

        @return YAPI.SUCCESS when the call succeeds.

        On failure, throws an exception or returns a negative error code.
        """
        return await self.set_command("D")

    # --- (end of YBluetoothLink implementation)

