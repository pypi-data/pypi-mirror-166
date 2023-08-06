from ctypes import byref, c_uint32

from .lib import load

quartz = load()


def main_display_id() -> int:
    return quartz.CGMainDisplayID()


def get_online_display_count() -> int:
    max_displays = c_uint32(5)
    display_count = c_uint32()

    while True:
        quartz.CGGetOnlineDisplayList(max_displays, None, byref(display_count))
        if display_count.value != max_displays.value:
            break
        max_displays *= 2

    return display_count.value


def get_online_display_list() -> list[int]:
    max_displays = c_uint32(get_online_display_count())
    online_displays = (c_uint32 * max_displays.value)()

    quartz.CGGetOnlineDisplayList(max_displays, online_displays, None)

    return list(online_displays)


def get_active_display_count() -> int:
    max_displays = c_uint32(5)
    display_count = c_uint32()

    while True:
        quartz.CGGetActiveDisplayList(max_displays, None, byref(display_count))
        if display_count.value != max_displays.value:
            break
        max_displays *= 2

    return display_count.value


def get_active_display_list() -> list[int]:
    max_displays = c_uint32(get_active_display_count())
    active_displays = (c_uint32 * max_displays.value)()

    quartz.CGGetActiveDisplayList(max_displays, active_displays, None)

    return list(active_displays)
