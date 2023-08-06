from __future__ import annotations

from dataclasses import dataclass

from deltadash.enums.note import NoteDirection
from deltadash.enums.note import NoteHitSound
from deltadash.enums.note import NotePosition
from deltadash.enums.note import NoteType


@dataclass
class Note:
    time_ms: int
    position: NotePosition
    type: NoteType
    direction: NoteDirection
    hitsound: NoteHitSound
    length_ms: int

    @staticmethod
    def from_str(string: str) -> Note:
        """Parses the comma-separated string of a note into a `Note` object."""
        time_ms, position, type, direction, hitsound, length_ms = string.split(",")

        return Note(
            int(time_ms),
            NotePosition(int(position)),
            NoteType(int(type)),
            NoteDirection(int(direction)),
            NoteHitSound(int(hitsound)),
            int(length_ms),
        )

    def into_str(self) -> str:
        """Returns the comma-separated string of a note."""
        return (
            f"{self.time_ms},{self.position.value},{self.type.value},{self.direction.value},"
            f"{self.hitsound.value},{self.length_ms}"
        )
