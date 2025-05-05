# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YSegmentedDisplay
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
Yoctopuce library: High-level API for YSegmentedDisplay
version: PATCH_WITH_VERSION
requires: yocto_segmenteddisplay_aio
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

from .yocto_segmenteddisplay_aio import YSegmentedDisplay as YSegmentedDisplay_aio
from .yocto_api import (
    YAPIContext, YAPI, YFunction
)

# --- (YSegmentedDisplay class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YSegmentedDisplayValueCallback = Union[Callable[['YSegmentedDisplay', str], Awaitable[None]], None]
    except TypeError:
        YSegmentedDisplayValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YSegmentedDisplay(YFunction):
    """
    The SegmentedDisplay class allows you to drive segmented displays.

    """
    _aio: YSegmentedDisplay_aio
    # --- (end of YSegmentedDisplay class start)
    if not _IS_MICROPYTHON:
        # --- (YSegmentedDisplay return codes)
        DISPLAYEDTEXT_INVALID: Final[str] = YAPI.INVALID_STRING
        DISPLAYMODE_DISCONNECTED: Final[int] = 0
        DISPLAYMODE_MANUAL: Final[int] = 1
        DISPLAYMODE_AUTO1: Final[int] = 2
        DISPLAYMODE_AUTO60: Final[int] = 3
        DISPLAYMODE_INVALID: Final[int] = -1
        # --- (end of YSegmentedDisplay return codes)


    # --- (YSegmentedDisplay implementation)

    @classmethod
    def FirstSegmentedDisplay(cls) -> Union[YSegmentedDisplay, None]:
        """
        Starts the enumeration of segmented displays currently accessible.
        Use the method YSegmentedDisplay.nextSegmentedDisplay() to iterate on
        next segmented displays.

        @return a pointer to a YSegmentedDisplay object, corresponding to
                the first segmented display currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YSegmentedDisplay_aio.FirstSegmentedDisplay())

    @classmethod
    def FirstSegmentedDisplayInContext(cls, yctx: YAPIContext) -> Union[YSegmentedDisplay, None]:
        """
        Starts the enumeration of segmented displays currently accessible.
        Use the method YSegmentedDisplay.nextSegmentedDisplay() to iterate on
        next segmented displays.

        @param yctx : a YAPI context.

        @return a pointer to a YSegmentedDisplay object, corresponding to
                the first segmented display currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YSegmentedDisplay_aio.FirstSegmentedDisplayInContext(yctx))

    def nextSegmentedDisplay(self):
        """
        Continues the enumeration of segmented displays started using yFirstSegmentedDisplay().
        Caution: You can't make any assumption about the returned segmented displays order.
        If you want to find a specific a segmented display, use SegmentedDisplay.findSegmentedDisplay()
        and a hardwareID or a logical name.

        @return a pointer to a YSegmentedDisplay object, corresponding to
                a segmented display currently online, or a None pointer
                if there are no more segmented displays to enumerate.
        """
        return self._proxy(type(self), self._aio.nextSegmentedDisplay())

    if not _DYNAMIC_HELPERS:
        def get_displayedText(self) -> str:
            """
            Returns the text currently displayed on the screen.

            @return a string corresponding to the text currently displayed on the screen

            On failure, throws an exception or returns YSegmentedDisplay.DISPLAYEDTEXT_INVALID.
            """
            return self._run(self._aio.get_displayedText())

    if not _DYNAMIC_HELPERS:
        def set_displayedText(self, newval: str) -> int:
            """
            Changes the text currently displayed on the screen.

            @param newval : a string corresponding to the text currently displayed on the screen

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_displayedText(newval))

    if not _DYNAMIC_HELPERS:
        def set_displayMode(self, newval: int) -> int:
            return self._run(self._aio.set_displayMode(newval))

    @classmethod
    def FindSegmentedDisplay(cls, func: str) -> YSegmentedDisplay:
        """
        Retrieves a segmented display for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the segmented display is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSegmentedDisplay.isOnline() to test if the segmented display is
        indeed online at a given time. In case of ambiguity when looking for
        a segmented display by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the segmented display, for instance
                MyDevice.segmentedDisplay.

        @return a YSegmentedDisplay object allowing you to drive the segmented display.
        """
        return cls._proxy(cls, YSegmentedDisplay_aio.FindSegmentedDisplay(func))

    @classmethod
    def FindSegmentedDisplayInContext(cls, yctx: YAPIContext, func: str) -> YSegmentedDisplay:
        """
        Retrieves a segmented display for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the segmented display is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YSegmentedDisplay.isOnline() to test if the segmented display is
        indeed online at a given time. In case of ambiguity when looking for
        a segmented display by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the segmented display, for instance
                MyDevice.segmentedDisplay.

        @return a YSegmentedDisplay object allowing you to drive the segmented display.
        """
        return cls._proxy(cls, YSegmentedDisplay_aio.FindSegmentedDisplayInContext(yctx, func))

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YSegmentedDisplayValueCallback) -> int:
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

    # --- (end of YSegmentedDisplay implementation)

