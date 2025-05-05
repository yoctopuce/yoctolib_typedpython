# -*- coding: utf-8 -*-
# ********************************************************************
#
#  $Id: svn_id $
#
#  High-level API for YColorLedCluster
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
Yoctopuce library: High-level API for YColorLedCluster
version: PATCH_WITH_VERSION
requires: yocto_colorledcluster_aio
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

from .yocto_colorledcluster_aio import YColorLedCluster as YColorLedCluster_aio
from .yocto_api import (
    YAPIContext, YAPI, YFunction, xarray
)

# --- (YColorLedCluster class start)
if not _IS_MICROPYTHON:
    # For CPython, use strongly typed callback types
    try:
        YColorLedClusterValueCallback = Union[Callable[['YColorLedCluster', str], Awaitable[None]], None]
    except TypeError:
        YColorLedClusterValueCallback = Union[Callable, Awaitable]

# noinspection PyProtectedMember
class YColorLedCluster(YFunction):
    """
    The YColorLedCluster class allows you to drive a
    color LED cluster. Unlike the ColorLed class, the YColorLedCluster
    class allows to handle several LEDs at once. Color changes can be done using RGB
    coordinates as well as HSL coordinates.
    The module performs all conversions form RGB to HSL automatically. It is then
    self-evident to turn on a LED with a given hue and to progressively vary its
    saturation or lightness. If needed, you can find more information on the
    difference between RGB and HSL in the section following this one.

    """
    _aio: YColorLedCluster_aio
    # --- (end of YColorLedCluster class start)
    if not _IS_MICROPYTHON:
        # --- (YColorLedCluster return codes)
        ACTIVELEDCOUNT_INVALID: Final[int] = YAPI.INVALID_UINT
        MAXLEDCOUNT_INVALID: Final[int] = YAPI.INVALID_UINT
        DYNAMICLEDCOUNT_INVALID: Final[int] = YAPI.INVALID_UINT
        BLINKSEQMAXCOUNT_INVALID: Final[int] = YAPI.INVALID_UINT
        BLINKSEQMAXSIZE_INVALID: Final[int] = YAPI.INVALID_UINT
        COMMAND_INVALID: Final[str] = YAPI.INVALID_STRING
        LEDTYPE_RGB: Final[int] = 0
        LEDTYPE_RGBW: Final[int] = 1
        LEDTYPE_WS2811: Final[int] = 2
        LEDTYPE_INVALID: Final[int] = -1
        # --- (end of YColorLedCluster return codes)


    # --- (YColorLedCluster implementation)

    @classmethod
    def FirstColorLedCluster(cls) -> Union[YColorLedCluster, None]:
        """
        Starts the enumeration of RGB LED clusters currently accessible.
        Use the method YColorLedCluster.nextColorLedCluster() to iterate on
        next RGB LED clusters.

        @return a pointer to a YColorLedCluster object, corresponding to
                the first RGB LED cluster currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YColorLedCluster_aio.FirstColorLedCluster())

    @classmethod
    def FirstColorLedClusterInContext(cls, yctx: YAPIContext) -> Union[YColorLedCluster, None]:
        """
        Starts the enumeration of RGB LED clusters currently accessible.
        Use the method YColorLedCluster.nextColorLedCluster() to iterate on
        next RGB LED clusters.

        @param yctx : a YAPI context.

        @return a pointer to a YColorLedCluster object, corresponding to
                the first RGB LED cluster currently online, or a None pointer
                if there are none.
        """
        return cls._proxy(cls, YColorLedCluster_aio.FirstColorLedClusterInContext(yctx))

    def nextColorLedCluster(self):
        """
        Continues the enumeration of RGB LED clusters started using yFirstColorLedCluster().
        Caution: You can't make any assumption about the returned RGB LED clusters order.
        If you want to find a specific a RGB LED cluster, use ColorLedCluster.findColorLedCluster()
        and a hardwareID or a logical name.

        @return a pointer to a YColorLedCluster object, corresponding to
                a RGB LED cluster currently online, or a None pointer
                if there are no more RGB LED clusters to enumerate.
        """
        return self._proxy(type(self), self._aio.nextColorLedCluster())

    if not _DYNAMIC_HELPERS:
        def get_activeLedCount(self) -> int:
            """
            Returns the number of LEDs currently handled by the device.

            @return an integer corresponding to the number of LEDs currently handled by the device

            On failure, throws an exception or returns YColorLedCluster.ACTIVELEDCOUNT_INVALID.
            """
            return self._run(self._aio.get_activeLedCount())

    if not _DYNAMIC_HELPERS:
        def set_activeLedCount(self, newval: int) -> int:
            """
            Changes the number of LEDs currently handled by the device.
            Remember to call the matching module
            saveToFlash() method to save the setting permanently.

            @param newval : an integer corresponding to the number of LEDs currently handled by the device

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_activeLedCount(newval))

    if not _DYNAMIC_HELPERS:
        def get_ledType(self) -> int:
            """
            Returns the RGB LED type currently handled by the device.

            @return a value among YColorLedCluster.LEDTYPE_RGB, YColorLedCluster.LEDTYPE_RGBW and
            YColorLedCluster.LEDTYPE_WS2811 corresponding to the RGB LED type currently handled by the device

            On failure, throws an exception or returns YColorLedCluster.LEDTYPE_INVALID.
            """
            return self._run(self._aio.get_ledType())

    if not _DYNAMIC_HELPERS:
        def set_ledType(self, newval: int) -> int:
            """
            Changes the RGB LED type currently handled by the device.
            Remember to call the matching module
            saveToFlash() method to save the setting permanently.

            @param newval : a value among YColorLedCluster.LEDTYPE_RGB, YColorLedCluster.LEDTYPE_RGBW and
            YColorLedCluster.LEDTYPE_WS2811 corresponding to the RGB LED type currently handled by the device

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_ledType(newval))

    if not _DYNAMIC_HELPERS:
        def get_maxLedCount(self) -> int:
            """
            Returns the maximum number of LEDs that the device can handle.

            @return an integer corresponding to the maximum number of LEDs that the device can handle

            On failure, throws an exception or returns YColorLedCluster.MAXLEDCOUNT_INVALID.
            """
            return self._run(self._aio.get_maxLedCount())

    if not _DYNAMIC_HELPERS:
        def get_dynamicLedCount(self) -> int:
            """
            Returns the maximum number of LEDs that can perform autonomous transitions and sequences.

            @return an integer corresponding to the maximum number of LEDs that can perform autonomous
            transitions and sequences

            On failure, throws an exception or returns YColorLedCluster.DYNAMICLEDCOUNT_INVALID.
            """
            return self._run(self._aio.get_dynamicLedCount())

    if not _DYNAMIC_HELPERS:
        def get_blinkSeqMaxCount(self) -> int:
            """
            Returns the maximum number of sequences that the device can handle.

            @return an integer corresponding to the maximum number of sequences that the device can handle

            On failure, throws an exception or returns YColorLedCluster.BLINKSEQMAXCOUNT_INVALID.
            """
            return self._run(self._aio.get_blinkSeqMaxCount())

    if not _DYNAMIC_HELPERS:
        def get_blinkSeqMaxSize(self) -> int:
            """
            Returns the maximum length of sequences.

            @return an integer corresponding to the maximum length of sequences

            On failure, throws an exception or returns YColorLedCluster.BLINKSEQMAXSIZE_INVALID.
            """
            return self._run(self._aio.get_blinkSeqMaxSize())

    if not _DYNAMIC_HELPERS:
        def set_command(self, newval: str) -> int:
            return self._run(self._aio.set_command(newval))

    @classmethod
    def FindColorLedCluster(cls, func: str) -> YColorLedCluster:
        """
        Retrieves a RGB LED cluster for a given identifier.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the RGB LED cluster is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YColorLedCluster.isOnline() to test if the RGB LED cluster is
        indeed online at a given time. In case of ambiguity when looking for
        a RGB LED cluster by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        If a call to this object's is_online() method returns FALSE although
        you are certain that the matching device is plugged, make sure that you did
        call registerHub() at application initialization time.

        @param func : a string that uniquely characterizes the RGB LED cluster, for instance
                YRGBLED2.colorLedCluster.

        @return a YColorLedCluster object allowing you to drive the RGB LED cluster.
        """
        return cls._proxy(cls, YColorLedCluster_aio.FindColorLedCluster(func))

    @classmethod
    def FindColorLedClusterInContext(cls, yctx: YAPIContext, func: str) -> YColorLedCluster:
        """
        Retrieves a RGB LED cluster for a given identifier in a YAPI context.
        The identifier can be specified using several formats:

        - FunctionLogicalName
        - ModuleSerialNumber.FunctionIdentifier
        - ModuleSerialNumber.FunctionLogicalName
        - ModuleLogicalName.FunctionIdentifier
        - ModuleLogicalName.FunctionLogicalName


        This function does not require that the RGB LED cluster is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YColorLedCluster.isOnline() to test if the RGB LED cluster is
        indeed online at a given time. In case of ambiguity when looking for
        a RGB LED cluster by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.

        @param yctx : a YAPI context
        @param func : a string that uniquely characterizes the RGB LED cluster, for instance
                YRGBLED2.colorLedCluster.

        @return a YColorLedCluster object allowing you to drive the RGB LED cluster.
        """
        return cls._proxy(cls, YColorLedCluster_aio.FindColorLedClusterInContext(yctx, func))

    if not _IS_MICROPYTHON:
        def registerValueCallback(self, callback: YColorLedClusterValueCallback) -> int:
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
        def set_rgbColor(self, ledIndex: int, count: int, rgbValue: int) -> int:
            """
            Changes the current color of consecutive LEDs in the cluster, using a RGB color. Encoding is done
            as follows: 0xRRGGBB.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param rgbValue :  new color.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_rgbColor(ledIndex, count, rgbValue))

    if not _DYNAMIC_HELPERS:
        def set_rgbColorAtPowerOn(self, ledIndex: int, count: int, rgbValue: int) -> int:
            """
            Changes the  color at device startup of consecutive LEDs in the cluster, using a RGB color.
            Encoding is done as follows: 0xRRGGBB. Don't forget to call saveLedsConfigAtPowerOn()
            to make sure the modification is saved in the device flash memory.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param rgbValue :  new color.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_rgbColorAtPowerOn(ledIndex, count, rgbValue))

    if not _DYNAMIC_HELPERS:
        def set_hslColorAtPowerOn(self, ledIndex: int, count: int, hslValue: int) -> int:
            """
            Changes the  color at device startup of consecutive LEDs in the cluster, using a HSL color.
            Encoding is done as follows: 0xHHSSLL. Don't forget to call saveLedsConfigAtPowerOn()
            to make sure the modification is saved in the device flash memory.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param hslValue :  new color.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_hslColorAtPowerOn(ledIndex, count, hslValue))

    if not _DYNAMIC_HELPERS:
        def set_hslColor(self, ledIndex: int, count: int, hslValue: int) -> int:
            """
            Changes the current color of consecutive LEDs in the cluster, using a HSL color. Encoding is done
            as follows: 0xHHSSLL.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param hslValue :  new color.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_hslColor(ledIndex, count, hslValue))

    if not _DYNAMIC_HELPERS:
        def rgb_move(self, ledIndex: int, count: int, rgbValue: int, delay: int) -> int:
            """
            Allows you to modify the current color of a group of adjacent LEDs to another color, in a seamless and
            autonomous manner. The transition is performed in the RGB space.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param rgbValue :  new color (0xRRGGBB).
            @param delay    :  transition duration in ms

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.rgb_move(ledIndex, count, rgbValue, delay))

    if not _DYNAMIC_HELPERS:
        def hsl_move(self, ledIndex: int, count: int, hslValue: int, delay: int) -> int:
            """
            Allows you to modify the current color of a group of adjacent LEDs  to another color, in a seamless and
            autonomous manner. The transition is performed in the HSL space. In HSL, hue is a circular
            value (0..360 deg). There are always two paths to perform the transition: by increasing
            or by decreasing the hue. The module selects the shortest transition.
            If the difference is exactly 180 deg, the module selects the transition which increases
            the hue.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param hslValue :  new color (0xHHSSLL).
            @param delay    :  transition duration in ms

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.hsl_move(ledIndex, count, hslValue, delay))

    if not _DYNAMIC_HELPERS:
        def addRgbMoveToBlinkSeq(self, seqIndex: int, rgbValue: int, delay: int) -> int:
            """
            Adds an RGB transition to a sequence. A sequence is a transition list, which can
            be executed in loop by a group of LEDs.  Sequences are persistent and are saved
            in the device flash memory as soon as the saveBlinkSeq() method is called.

            @param seqIndex :  sequence index.
            @param rgbValue :  target color (0xRRGGBB)
            @param delay    :  transition duration in ms

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.addRgbMoveToBlinkSeq(seqIndex, rgbValue, delay))

    if not _DYNAMIC_HELPERS:
        def addHslMoveToBlinkSeq(self, seqIndex: int, hslValue: int, delay: int) -> int:
            """
            Adds an HSL transition to a sequence. A sequence is a transition list, which can
            be executed in loop by an group of LEDs.  Sequences are persistent and are saved
            in the device flash memory as soon as the saveBlinkSeq() method is called.

            @param seqIndex : sequence index.
            @param hslValue : target color (0xHHSSLL)
            @param delay    : transition duration in ms

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.addHslMoveToBlinkSeq(seqIndex, hslValue, delay))

    if not _DYNAMIC_HELPERS:
        def addMirrorToBlinkSeq(self, seqIndex: int) -> int:
            """
            Adds a mirror ending to a sequence. When the sequence will reach the end of the last
            transition, its running speed will automatically be reversed so that the sequence plays
            in the reverse direction, like in a mirror. After the first transition of the sequence
            is played at the end of the reverse execution, the sequence starts again in
            the initial direction.

            @param seqIndex : sequence index.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.addMirrorToBlinkSeq(seqIndex))

    if not _DYNAMIC_HELPERS:
        def addJumpToBlinkSeq(self, seqIndex: int, linkSeqIndex: int) -> int:
            """
            Adds to a sequence a jump to another sequence. When a pixel will reach this jump,
            it will be automatically relinked to the new sequence, and will run it starting
            from the beginning.

            @param seqIndex : sequence index.
            @param linkSeqIndex : index of the sequence to chain.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.addJumpToBlinkSeq(seqIndex, linkSeqIndex))

    if not _DYNAMIC_HELPERS:
        def addUnlinkToBlinkSeq(self, seqIndex: int) -> int:
            """
            Adds a to a sequence a hard stop code. When a pixel will reach this stop code,
            instead of restarting the sequence in a loop it will automatically be unlinked
            from the sequence.

            @param seqIndex : sequence index.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.addUnlinkToBlinkSeq(seqIndex))

    if not _DYNAMIC_HELPERS:
        def linkLedToBlinkSeq(self, ledIndex: int, count: int, seqIndex: int, offset: int) -> int:
            """
            Links adjacent LEDs to a specific sequence. These LEDs start to execute
            the sequence as soon as  startBlinkSeq is called. It is possible to add an offset
            in the execution: that way we  can have several groups of LED executing the same
            sequence, with a  temporal offset. A LED cannot be linked to more than one sequence.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param seqIndex :  sequence index.
            @param offset   :  execution offset in ms.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.linkLedToBlinkSeq(ledIndex, count, seqIndex, offset))

    if not _DYNAMIC_HELPERS:
        def linkLedToBlinkSeqAtPowerOn(self, ledIndex: int, count: int, seqIndex: int, offset: int) -> int:
            """
            Links adjacent LEDs to a specific sequence at device power-on. Don't forget to configure
            the sequence auto start flag as well and call saveLedsConfigAtPowerOn(). It is possible to add an offset
            in the execution: that way we  can have several groups of LEDs executing the same
            sequence, with a  temporal offset. A LED cannot be linked to more than one sequence.

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param seqIndex :  sequence index.
            @param offset   :  execution offset in ms.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.linkLedToBlinkSeqAtPowerOn(ledIndex, count, seqIndex, offset))

    if not _DYNAMIC_HELPERS:
        def linkLedToPeriodicBlinkSeq(self, ledIndex: int, count: int, seqIndex: int, periods: int) -> int:
            """
            Links adjacent LEDs to a specific sequence. These LED start to execute
            the sequence as soon as  startBlinkSeq is called. This function automatically
            introduces a shift between LEDs so that the specified number of sequence periods
            appears on the group of LEDs (wave effect).

            @param ledIndex :  index of the first affected LED.
            @param count    :  affected LED count.
            @param seqIndex :  sequence index.
            @param periods  :  number of periods to show on LEDs.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.linkLedToPeriodicBlinkSeq(ledIndex, count, seqIndex, periods))

    if not _DYNAMIC_HELPERS:
        def unlinkLedFromBlinkSeq(self, ledIndex: int, count: int) -> int:
            """
            Unlinks adjacent LEDs from a  sequence.

            @param ledIndex  :  index of the first affected LED.
            @param count     :  affected LED count.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.unlinkLedFromBlinkSeq(ledIndex, count))

    if not _DYNAMIC_HELPERS:
        def startBlinkSeq(self, seqIndex: int) -> int:
            """
            Starts a sequence execution: every LED linked to that sequence starts to
            run it in a loop. Note that a sequence with a zero duration can't be started.

            @param seqIndex :  index of the sequence to start.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.startBlinkSeq(seqIndex))

    if not _DYNAMIC_HELPERS:
        def stopBlinkSeq(self, seqIndex: int) -> int:
            """
            Stops a sequence execution. If started again, the execution
            restarts from the beginning.

            @param seqIndex :  index of the sequence to stop.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.stopBlinkSeq(seqIndex))

    if not _DYNAMIC_HELPERS:
        def resetBlinkSeq(self, seqIndex: int) -> int:
            """
            Stops a sequence execution and resets its contents. LEDs linked to this
            sequence are not automatically updated anymore.

            @param seqIndex :  index of the sequence to reset

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.resetBlinkSeq(seqIndex))

    if not _DYNAMIC_HELPERS:
        def set_blinkSeqStateAtPowerOn(self, seqIndex: int, autostart: int) -> int:
            """
            Configures a sequence to make it start automatically at device
            startup. Note that a sequence with a zero duration can't be started.
            Don't forget to call saveBlinkSeq() to make sure the
            modification is saved in the device flash memory.

            @param seqIndex :  index of the sequence to reset.
            @param autostart : 0 to keep the sequence turned off and 1 to start it automatically.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_blinkSeqStateAtPowerOn(seqIndex, autostart))

    if not _DYNAMIC_HELPERS:
        def set_blinkSeqSpeed(self, seqIndex: int, speed: int) -> int:
            """
            Changes the execution speed of a sequence. The natural execution speed is 1000 per
            thousand. If you configure a slower speed, you can play the sequence in slow-motion.
            If you set a negative speed, you can play the sequence in reverse direction.

            @param seqIndex :  index of the sequence to start.
            @param speed :     sequence running speed (-1000...1000).

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_blinkSeqSpeed(seqIndex, speed))

    if not _DYNAMIC_HELPERS:
        def saveLedsConfigAtPowerOn(self) -> int:
            """
            Saves the LEDs power-on configuration. This includes the start-up color or
            sequence binding for all LEDs. Warning: if some LEDs are linked to a sequence, the
            method saveBlinkSeq() must also be called to save the sequence definition.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.saveLedsConfigAtPowerOn())

    if not _DYNAMIC_HELPERS:
        def saveBlinkSeq(self, seqIndex: int) -> int:
            """
            Saves the definition of a sequence. Warning: only sequence steps and flags are saved.
            to save the LEDs startup bindings, the method saveLedsConfigAtPowerOn()
            must be called.

            @param seqIndex :  index of the sequence to start.

            @return YAPI.SUCCESS when the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.saveBlinkSeq(seqIndex))

    if not _DYNAMIC_HELPERS:
        def set_rgbColorBuffer(self, ledIndex: int, buff: xarray) -> int:
            """
            Sends a binary buffer to the LED RGB buffer, as is.
            First three bytes are RGB components for LED specified as parameter, the
            next three bytes for the next LED, etc.

            @param ledIndex : index of the first LED which should be updated
            @param buff : the binary buffer to send

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_rgbColorBuffer(ledIndex, buff))

    if not _DYNAMIC_HELPERS:
        def set_rgbColorArray(self, ledIndex: int, rgbList: list[int]) -> int:
            """
            Sends 24bit RGB colors (provided as a list of integers) to the LED RGB buffer, as is.
            The first number represents the RGB value of the LED specified as parameter, the second
            number represents the RGB value of the next LED, etc.

            @param ledIndex : index of the first LED which should be updated
            @param rgbList : a list of 24bit RGB codes, in the form 0xRRGGBB

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_rgbColorArray(ledIndex, rgbList))

    if not _DYNAMIC_HELPERS:
        def rgbArrayOfs_move(self, ledIndex: int, rgbList: list[int], delay: int) -> int:
            """
            Sets up a smooth RGB color transition to the specified pixel-by-pixel list of RGB
            color codes. The first color code represents the target RGB value of the first LED,
            the next color code represents the target value of the next LED, etc.

            @param ledIndex : index of the first LED which should be updated
            @param rgbList : a list of target 24bit RGB codes, in the form 0xRRGGBB
            @param delay   : transition duration in ms

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.rgbArrayOfs_move(ledIndex, rgbList, delay))

    if not _DYNAMIC_HELPERS:
        def rgbArray_move(self, rgbList: list[int], delay: int) -> int:
            """
            Sets up a smooth RGB color transition to the specified pixel-by-pixel list of RGB
            color codes. The first color code represents the target RGB value of the first LED,
            the next color code represents the target value of the next LED, etc.

            @param rgbList : a list of target 24bit RGB codes, in the form 0xRRGGBB
            @param delay   : transition duration in ms

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.rgbArray_move(rgbList, delay))

    if not _DYNAMIC_HELPERS:
        def set_hslColorBuffer(self, ledIndex: int, buff: xarray) -> int:
            """
            Sends a binary buffer to the LED HSL buffer, as is.
            First three bytes are HSL components for the LED specified as parameter, the
            next three bytes for the second LED, etc.

            @param ledIndex : index of the first LED which should be updated
            @param buff : the binary buffer to send

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_hslColorBuffer(ledIndex, buff))

    if not _DYNAMIC_HELPERS:
        def set_hslColorArray(self, ledIndex: int, hslList: list[int]) -> int:
            """
            Sends 24bit HSL colors (provided as a list of integers) to the LED HSL buffer, as is.
            The first number represents the HSL value of the LED specified as parameter, the second number represents
            the HSL value of the second LED, etc.

            @param ledIndex : index of the first LED which should be updated
            @param hslList : a list of 24bit HSL codes, in the form 0xHHSSLL

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.set_hslColorArray(ledIndex, hslList))

    if not _DYNAMIC_HELPERS:
        def hslArray_move(self, hslList: list[int], delay: int) -> int:
            """
            Sets up a smooth HSL color transition to the specified pixel-by-pixel list of HSL
            color codes. The first color code represents the target HSL value of the first LED,
            the second color code represents the target value of the second LED, etc.

            @param hslList : a list of target 24bit HSL codes, in the form 0xHHSSLL
            @param delay   : transition duration in ms

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.hslArray_move(hslList, delay))

    if not _DYNAMIC_HELPERS:
        def hslArrayOfs_move(self, ledIndex: int, hslList: list[int], delay: int) -> int:
            """
            Sets up a smooth HSL color transition to the specified pixel-by-pixel list of HSL
            color codes. The first color code represents the target HSL value of the first LED,
            the second color code represents the target value of the second LED, etc.

            @param ledIndex : index of the first LED which should be updated
            @param hslList : a list of target 24bit HSL codes, in the form 0xHHSSLL
            @param delay   : transition duration in ms

            @return YAPI.SUCCESS if the call succeeds.

            On failure, throws an exception or returns a negative error code.
            """
            return self._run(self._aio.hslArrayOfs_move(ledIndex, hslList, delay))

    if not _DYNAMIC_HELPERS:
        def get_rgbColorBuffer(self, ledIndex: int, count: int) -> xarray:
            """
            Returns a binary buffer with content from the LED RGB buffer, as is.
            First three bytes are RGB components for the first LED in the interval,
            the next three bytes for the second LED in the interval, etc.

            @param ledIndex : index of the first LED which should be returned
            @param count    : number of LEDs which should be returned

            @return a binary buffer with RGB components of selected LEDs.

            On failure, throws an exception or returns an empty binary buffer.
            """
            return self._run(self._aio.get_rgbColorBuffer(ledIndex, count))

    if not _DYNAMIC_HELPERS:
        def get_rgbColorArray(self, ledIndex: int, count: int) -> list[int]:
            """
            Returns a list on 24bit RGB color values with the current colors displayed on
            the RGB LEDs. The first number represents the RGB value of the first LED,
            the second number represents the RGB value of the second LED, etc.

            @param ledIndex : index of the first LED which should be returned
            @param count    : number of LEDs which should be returned

            @return a list of 24bit color codes with RGB components of selected LEDs, as 0xRRGGBB.

            On failure, throws an exception or returns an empty array.
            """
            return self._run(self._aio.get_rgbColorArray(ledIndex, count))

    if not _DYNAMIC_HELPERS:
        def get_rgbColorArrayAtPowerOn(self, ledIndex: int, count: int) -> list[int]:
            """
            Returns a list on 24bit RGB color values with the RGB LEDs startup colors.
            The first number represents the startup RGB value of the first LED,
            the second number represents the RGB value of the second LED, etc.

            @param ledIndex : index of the first LED  which should be returned
            @param count    : number of LEDs which should be returned

            @return a list of 24bit color codes with RGB components of selected LEDs, as 0xRRGGBB.

            On failure, throws an exception or returns an empty array.
            """
            return self._run(self._aio.get_rgbColorArrayAtPowerOn(ledIndex, count))

    if not _DYNAMIC_HELPERS:
        def get_linkedSeqArray(self, ledIndex: int, count: int) -> list[int]:
            """
            Returns a list on sequence index for each RGB LED. The first number represents the
            sequence index for the the first LED, the second number represents the sequence
            index for the second LED, etc.

            @param ledIndex : index of the first LED which should be returned
            @param count    : number of LEDs which should be returned

            @return a list of integers with sequence index

            On failure, throws an exception or returns an empty array.
            """
            return self._run(self._aio.get_linkedSeqArray(ledIndex, count))

    if not _DYNAMIC_HELPERS:
        def get_blinkSeqSignatures(self, seqIndex: int, count: int) -> list[int]:
            """
            Returns a list on 32 bit signatures for specified blinking sequences.
            Since blinking sequences cannot be read from the device, this can be used
            to detect if a specific blinking sequence is already programmed.

            @param seqIndex : index of the first blinking sequence which should be returned
            @param count    : number of blinking sequences which should be returned

            @return a list of 32 bit integer signatures

            On failure, throws an exception or returns an empty array.
            """
            return self._run(self._aio.get_blinkSeqSignatures(seqIndex, count))

    if not _DYNAMIC_HELPERS:
        def get_blinkSeqStateSpeed(self, seqIndex: int, count: int) -> list[int]:
            """
            Returns a list of integers with the current speed for specified blinking sequences.

            @param seqIndex : index of the first sequence speed which should be returned
            @param count    : number of sequence speeds which should be returned

            @return a list of integers, 0 for sequences turned off and 1 for sequences running

            On failure, throws an exception or returns an empty array.
            """
            return self._run(self._aio.get_blinkSeqStateSpeed(seqIndex, count))

    if not _DYNAMIC_HELPERS:
        def get_blinkSeqStateAtPowerOn(self, seqIndex: int, count: int) -> list[int]:
            """
            Returns a list of integers with the "auto-start at power on" flag state for specified blinking sequences.

            @param seqIndex : index of the first blinking sequence which should be returned
            @param count    : number of blinking sequences which should be returned

            @return a list of integers, 0 for sequences turned off and 1 for sequences running

            On failure, throws an exception or returns an empty array.
            """
            return self._run(self._aio.get_blinkSeqStateAtPowerOn(seqIndex, count))

    if not _DYNAMIC_HELPERS:
        def get_blinkSeqState(self, seqIndex: int, count: int) -> list[int]:
            """
            Returns a list of integers with the started state for specified blinking sequences.

            @param seqIndex : index of the first blinking sequence which should be returned
            @param count    : number of blinking sequences which should be returned

            @return a list of integers, 0 for sequences turned off and 1 for sequences running

            On failure, throws an exception or returns an empty array.
            """
            return self._run(self._aio.get_blinkSeqState(seqIndex, count))

    if not _DYNAMIC_HELPERS:
        def hsl2rgb(self, hslValue: int) -> int:
            return self._run(self._aio.hsl2rgb(hslValue))

    # --- (end of YColorLedCluster implementation)

