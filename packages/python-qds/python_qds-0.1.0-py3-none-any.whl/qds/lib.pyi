from ctypes import c_uint32, pointer

def load() -> QuartzDisplayServices: ...

class QuartzDisplayServices:
    def CGMainDisplayID(self) -> int: ...
    def CGGetOnlineDisplayList(
        self,
        maxDisplays: c_uint32,
        onlineDisplays: pointer[c_uint32],
        displayCount: pointer[c_uint32],
    ): ...
    def CGGetActiveDisplayList(
        self,
        maxDisplays: c_uint32,
        activeDisplays: pointer[c_uint32],
        displayCount: pointer[c_uint32],
    ): ...
