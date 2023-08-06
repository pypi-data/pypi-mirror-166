from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from deltadash.enums.event import EventType

# @dataclass
# class Event:
#    time_ms: int

# To conclude: There is no benefit to inheriting from a common `Event`
# as all of these do completely DIFFERENT things that cant be easily
# genericised. The only thing they have in common is that they all
# have a `time_ms` attribute, which is useless in most cases.


@dataclass
class FeverEvent:
    time_ms: int
    toggle: bool

    @cached_property
    def type(self) -> EventType:
        return EventType.FEVER_TOGGLE

    @staticmethod
    def from_str(string: str) -> FeverEvent:
        """Parses the comma-separated string of a fever event into a `FeverEvent` object."""
        _, time_ms, toggle = string.split(",")
        return FeverEvent(int(time_ms), toggle == "1")

    def into_str(self) -> str:
        """Returns the comma-separated string of a fever event."""
        return f"{self.type.value},{self.time_ms},{int(self.toggle)}"


@dataclass
class SpeedEvent:
    time_ms: int
    speed: float

    @cached_property
    def type(self) -> EventType:
        return EventType.SPEED_CHANGE

    @staticmethod
    def from_str(string: str) -> SpeedEvent:
        """Parses the comma-separated string of a speed event into a `SpeedEvent` object."""
        _, time_ms, speed = string.split(",")
        return SpeedEvent(int(time_ms), float(speed))

    def into_str(self) -> str:
        """Returns the comma-separated string of a speed event."""
        return f"{self.type.value},{self.time_ms},{self.speed}"


@dataclass
class BPMEvent:
    time_ms: int
    bpm: float

    @cached_property
    def type(self) -> EventType:
        return EventType.BPM_CHANGE

    @staticmethod
    def from_str(string: str) -> BPMEvent:
        """Parses the comma-separated string of a bpm event into a `BPMEvent` object."""
        _, time_ms, bpm = string.split(",")
        return BPMEvent(int(time_ms), float(bpm))

    def into_str(self) -> str:
        """Returns the comma-separated string of a bpm event."""
        return f"{self.type.value},{self.time_ms},{self.bpm}"
