from __future__ import annotations

from enum import IntEnum


class EventType(IntEnum):
    FEVER_TOGGLE = 0
    BPM_CHANGE = 1
    SPEED_CHANGE = 2
