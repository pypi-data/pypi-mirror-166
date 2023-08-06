from typing import Callable

# fmt: off
LINUX_SYSTEM: tuple[str, str] = (
    ("0", "X11; Linux x86_64"),
)

LINUX_VERSION: tuple[str, Callable] = (
    ("0", lambda _: ""),
)
# fmt: on
