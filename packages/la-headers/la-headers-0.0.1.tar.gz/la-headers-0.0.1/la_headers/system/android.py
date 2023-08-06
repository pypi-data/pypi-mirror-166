from typing import Callable

from packaging.version import Version

# fmt: off
ANDROID_SYSTEM: tuple[str, str] = (
    ("0", "Linux; Android {os_version}"),
)

ANDROID_VERSION: tuple[str, Callable] = (
    ("0", lambda v: str(Version(v).major)),
)
# fmt: on
