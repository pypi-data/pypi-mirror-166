from __future__ import annotations

from enum import IntEnum


class NotePosition(IntEnum):
    TOP = 0
    BOTTOM = 1


class NoteType(IntEnum):
    SHORT = 0
    LONG = 1


class NoteDirection(IntEnum):
    LEFT = 0
    RIGHT = 1


class NoteHitSound(IntEnum):
    NORMAL = 0
    SNARE = 1
    CLAP = 2
    FINAL = 3
