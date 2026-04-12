from .NoteInfoHandler import NoteInfoHandler
from .NoteBuilder import NoteBuilder
from modules import MusicRenderer

import random

POSSIBLE_CHORDS_BY_ROOT: dict = {
    ("C", "flat"): ["major", "major 7th", "dominant 7th", "augmented"],
    ("C", "sharp"): ["major", "major 7th", "dominant 7th", "minor", "minor 7th", "diminished", "diminished 7th", "half-diminished 7th"],
    ("D", "flat"): ["major", "major 7th", "dominant 7th", "augmented"],
    ("D", "sharp"): ["minor", "minor 7th", "diminished", "diminished 7th", "half-diminished 7th"],
    ("E", "flat"): ["major", "major 7th", "dominant 7th", "minor", "augmented", "diminished"],
    ("E", "sharp"): ["diminished", "diminished 7th", "half-diminished 7th"],
    ("F", "flat"): ["augmented"],
    ("G", "flat"): ["major", "major 7th", "dominant 7th", "augmented"],
    ("G", "sharp"): ["minor", "minor 7th", "diminished", "diminished 7th", "half-diminished 7th"],
    ("A", "flat"): ["major", "major 7th", "dominant 7th", "minor", "minor 7th",  "augmented"],
    ("A", "sharp"): ["minor", "minor 7th", "diminished", "diminished 7th", "half-diminished 7th"],
    ("B", "sharp"): ["diminished", "diminished 7th", "half-diminished 7th"],
}

INTERVALS_BY_CHORD_TYPE: dict = {
    "major": [4, 3],
    "minor": [3, 4],
    "augmented": [4, 4],
    "diminished": [3, 3],
    "diminished 7th": [3, 3, 3],
    "half-diminished 7th": [3, 3, 4],
    "major 7th": [4, 3, 4],
    "dominant 7th": [4, 3, 3],
    "minor 7th": [3, 4, 3],
}


# Returns a tuple of root note letter, accidental, type of chord, and interval list
def get_random_info() -> tuple:
    random_letter: str = chr(64 + random.randint(1, 7))
    random_accidental: int = random.choice(["flat", "sharp", None])
    root_note_data: tuple = (random_letter, random_accidental)

    # Get a random chord and generate the intervals
    possible_chord_list: list = (
        list(INTERVALS_BY_CHORD_TYPE.keys()) 
        if (root_note_data not in POSSIBLE_CHORDS_BY_ROOT) 
        else POSSIBLE_CHORDS_BY_ROOT[root_note_data]
    )
    random_chord_type: str = random.choice(possible_chord_list)
    random_interval_list: list = INTERVALS_BY_CHORD_TYPE[random_chord_type]
    return root_note_data, random_chord_type, random_interval_list


# Returns the name of the chord.
# Example: Ab minor, B diminished 7th
def format_chord_name(letter: str, accidental: str, chord_type: str) -> str:
    result: str = f"{letter}"
    if (accidental == "sharp"):
        result += "#"
    elif (accidental == "flat"):
        result += "b"
    
    result += f" {chord_type}"
    return result


# Returns an xml string containing a series of note elements.
# chord_info is a list of note_info tuples, which include
# the letter, octave, and accidental.
def get_xml(note_info_list: list[tuple]) -> str:
    result_xml: str = ""
    for i, info in enumerate(note_info_list):
        # Unpack from the info tuple
        (step, octave, *rest) = info
        accidental: str = rest[0] if len(rest) > 0 else None
            
        should_add_chord_tag: bool = (i > 0)
        new_note = NoteBuilder() \
            .set_step(step) \
            .set_octave(octave) \
            .set_note_type("whole") \
            .set_accidental(accidental) \
            .set_is_chord(should_add_chord_tag) \
            .build()

        result_xml += new_note.get_xml()
    return result_xml


class ChordInfo:
    def __init__(self, chord_name: str, xml: str, svg: str):
        self.intervals = None
        self.chord_name = chord_name
        self.xml = xml
        self.svg = svg


class ChordGenerator:
    def generate():
        # Get random info and get xml, return a chord info generator
        start_note_data, chord_type, random_interval_list = get_random_info()
        chord_info_list = NoteInfoHandler.get_note_info_by_intervals(*start_note_data, random_interval_list)
        notes_xml: str = get_xml(chord_info_list)
        total_xml: str = MusicRenderer.render_single_staff_template(
            notes_xml=notes_xml)
        svg: str = MusicRenderer.render_to_svg(total_xml)

        return ChordInfo(chord_name=format_chord_name(
            *start_note_data, chord_type), 
            xml=notes_xml,
            svg=svg,
        )