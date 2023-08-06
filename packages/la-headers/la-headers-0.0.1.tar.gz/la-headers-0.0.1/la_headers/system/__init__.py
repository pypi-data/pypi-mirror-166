from typing import Callable

from la_headers.system.android import ANDROID_SYSTEM, ANDROID_VERSION
from la_headers.system.linux import LINUX_SYSTEM, LINUX_VERSION
from la_headers.system.mac import MAC_SYSTEM, MAC_VERSION
from la_headers.system.windows import WINDOWS_SYSTEM, WINDOWS_VERSION
from la_headers.utility import find_best_function, find_best_option

_system = {
    "linux": LINUX_SYSTEM,
    "android": ANDROID_SYSTEM,
    "windows": WINDOWS_SYSTEM,
    "mac": MAC_SYSTEM,
}

_version = {
    "linux": LINUX_VERSION,
    "android": ANDROID_VERSION,
    "windows": WINDOWS_VERSION,
    "mac": MAC_VERSION,
}


def generate_system(os: str, os_version: str) -> str:
    """
    os:
        windows
        linux
        android
        mac

    os_version:
        major.minor.patch
    """

    version_options = _version[os]
    version_function = find_best_function(os_version, version_options) or (lambda _: "")
    version_formated = version_function(os_version)

    system_options = _system[os]
    best_option = find_best_option(os_version, system_options).format(
        os_version=version_formated
    )

    return best_option
