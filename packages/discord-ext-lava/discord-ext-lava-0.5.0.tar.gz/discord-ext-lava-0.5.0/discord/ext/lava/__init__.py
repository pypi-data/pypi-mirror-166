from __future__ import annotations

import logging
from typing import Final, Literal, NamedTuple

from .exceptions import *
from .node import *
from .objects import *
from .player import *
from .pool import *
from .queue import *
from .utils import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: Final[VersionInfo] = VersionInfo(major=0, minor=5, micro=0, releaselevel="final", serial=0)

__title__: Final[str] = "discord-ext-lava"
__author__: Final[str] = "Axelancerr"
__copyright__: Final[str] = "Copyright 2020-present Axelancerr"
__license__: Final[str] = "MIT"
__version__: Final[str] = "0.5.0"
__maintainer__: Final[str] = "Aaron Hennessey"
__source__: Final[str] = "https://github.com/Axelware/discord-ext-lava"

logging.getLogger("discord-ext-lava")
