from __future__ import annotations


__all__ = (
    "VolumeData",
    "Volume"
)

VolumeData = float


class Volume:

    __slots__ = ("level",)

    def __init__(
        self,
        *,
        level: float = 100.0
    ) -> None:

        if level < 0.0 or level > 500.0:
            raise ValueError("'level' must be more than or equal to 0.0 and less than or equal to 500.0.")

        self.level: float = level

    def __repr__(self) -> str:
        return f"<discord.ext.lava.Volume level={self.level}>"

    def _construct_payload(self) -> VolumeData:
        return self.level / 100.0
