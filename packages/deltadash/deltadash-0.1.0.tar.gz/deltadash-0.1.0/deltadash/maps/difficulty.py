from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from deltadash import parser
from deltadash.enums.event import EventType
from deltadash.maps.event import BPMEvent
from deltadash.maps.event import FeverEvent
from deltadash.maps.event import SpeedEvent
from deltadash.maps.note import Note


@dataclass
class Difficulty:
    # Song Metadata
    artist: str
    title: str
    name: str
    mapper: str

    # Map Metadata
    preview_ms: int
    background_path: str
    thumbnail_path: str
    audio_path: str

    id: int
    set_id: int

    # Difficulty Settings
    speed: float
    health: float
    sensitivity: float

    # Difficulty contents
    notes: list[Note] = field(default_factory=list)

    # Events
    speed_events: list[SpeedEvent] = field(default_factory=list)
    bpm_events: list[BPMEvent] = field(default_factory=list)
    fever_events: list[FeverEvent] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        return f"{self.artist} - {self.title} [{self.name}]"

    @staticmethod
    def from_str(string: str) -> Difficulty:
        """Parses a string of a `.dd` file's contents into a `Difficulty` object."""

        sections = parser.ini.parse(string)

        # Song Metadata
        artist = sections["General"]["Artist"]
        title = sections["General"]["Title"]
        name = sections["General"]["DiffName"]
        mapper = sections["General"]["Mapper"]

        # Map Metadata
        preview_ms = int(sections["Metadata"]["PreviewPoint"])
        background_path = sections["Metadata"]["Background"]
        thumbnail_path = sections["Metadata"]["Thumbnail"]
        audio_path = sections["Metadata"]["Audio"]

        id = int(sections["Metadata"]["BeatmapID"])
        set_id = int(sections["Metadata"]["BeatmapsetID"])

        # Difficulty Settings
        speed = float(sections["Difficulty"]["Speed"])
        health = float(sections["Difficulty"]["Health"])
        sensitivity = float(
            sections["Difficulty"]["Sensivity"],
        )  # The typo is in the .dd files

        # This is a bit cursed but required if we want to use an ini parser.
        # In this case, the dictionary keys are the note string we are lookign
        # for, and the values are empty.
        notes = [Note.from_str(note) for note in sections["HitObjects"]]

        # Likewise for events.
        speed_events = []
        bpm_events = []
        fever_events = []

        for event in sections["Events"]:
            event_type = EventType(int(event.split(",")[0]))

            if event_type is EventType.SPEED_CHANGE:
                speed_events.append(SpeedEvent.from_str(event))
            elif event_type is EventType.BPM_CHANGE:
                bpm_events.append(BPMEvent.from_str(event))
            elif event_type is EventType.FEVER_TOGGLE:
                fever_events.append(FeverEvent.from_str(event))

        return Difficulty(
            artist,
            title,
            name,
            mapper,
            preview_ms,
            background_path,
            thumbnail_path,
            audio_path,
            id,
            set_id,
            speed,
            health,
            sensitivity,
            notes,
            speed_events,
            bpm_events,
            fever_events,
        )

    @staticmethod
    def from_file(path: str) -> Difficulty:
        """Parses a `.dd` file into a `Difficulty` object.

        Opens a `.dd` file, reading its contents fully at once and calls
        `Difficulty.from_str` to parse the contents into a `Difficulty` object.
        """
        with open(path) as file:
            return Difficulty.from_str(file.read())

    def into_str(self) -> str:
        """Constructs a valid `.dd` file str from the contents of the `Difficulty` object."""
        sections = {
            "General": {
                "Title": self.title,
                "Artist": self.artist,
                "Mapper": self.mapper,
                "DiffName": self.name,
            },
            "Metadata": {
                "PreviewPoint": self.preview_ms,
                "Background": self.background_path,
                "Thumbnail": self.thumbnail_path,
                "Audio": self.audio_path,
                "BeatmapID": self.id,
                "BeatmapsetID": self.set_id,
            },
            "Difficulty": {
                "Speed": self.speed,
                "Health": self.health,
                "Sensivity": self.sensitivity,  # The typo is in the .dd files
            },
        }

        section_str = "\n"
        section_str += "\n\n".join(
            parser.ini.into_section_str(section, contents)
            for section, contents in sections.items()
        )

        section_str += "\n\n[HitObjects]\n"
        section_str += "\n".join(note.into_str() for note in self.notes)

        section_str += "\n\n[Events]\n"
        section_str += "\n".join(
            event.into_str()
            for event in self.speed_events + self.bpm_events + self.fever_events
        )
        section_str += "\n"

        return section_str

    def into_file(self, path: str) -> None:
        """Writes the contents of the `Difficulty` object into a DeltaDash compliant
        `.dd` file.

        Internally, it just calls `Difficulty.into_str` and writes the result to the
        specified file.
        """

        with open(path, "w") as file:
            file.write(self.into_str())
