from __future__ import annotations

from collections import defaultdict


def parse(contents: str) -> dict[str, dict[str, str]]:
    """Parse a .ini file into a dictionary of sections and key-value pairs."""
    sections = defaultdict(dict)
    section = None
    for line in contents.splitlines():
        if line.startswith("["):
            section = line.strip("[]")
        elif section is not None and line:
            value_pair = line.split(":", 1)
            # Cursed but we need this for HitObjects
            if len(value_pair) == 2:
                key, value = value_pair
                sections[section][key] = value
            else:
                key = value_pair[0]
                value = ""
            sections[section][key] = value

    return dict(sections)


def into_section_str(name: str, contents: dict[str, str]) -> str:
    """Convert a section dictionary into a string."""
    section = f"[{name}]\n"
    section += "\n".join(f"{key}:{value}" for key, value in contents.items())

    return section
