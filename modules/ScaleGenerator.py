from .NoteBuilder import NoteBuilder
from .NoteInfoHandler import NoteInfoHandler

from modules import MusicRenderer

import random


# Keys are the scale modes. Each value is a list of intervals 
# from previous note to current note.
SCALE_MAP: dict = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "harmonic minor": [2, 1, 2, 2, 1, 3, 1],
    "natural minor": [2, 1, 2, 2, 1, 2, 2],
    "melodic minor": [2, 1, 2, 2, 2, 2, 1],
    "dorian": [2, 1, 2, 2, 2, 1, 2],
    "phrygian": [1, 2, 2, 2, 1, 2, 2],
    "lydian": [2, 2, 2, 1, 2, 2, 1], 
    "mixolydian": [2, 2, 1, 2, 2, 1, 2],
    "locrian": [1, 2, 2, 1, 2, 2, 2],
}


# Given a letter, accidental, and scale mode, format the name such as "F# minor"
def format_scale_name(letter: str, mode: str, accidental: str = None) -> str:
    result: str = ""
    if (accidental == "sharp"):
        result = f"{letter}# {mode}"
    elif (accidental == "flat"):
        result = f"{letter}b {mode}"
    else:
        result = f"{letter} {mode}"
    return result


def get_random_scale_info() -> tuple:
    # random letter and scale mode
    random_scale_letter: str = chr(random.randint(65, 71)) 
    random_accidental: str = random.choice(["sharp", "flat", None])
    key: str = (random_scale_letter, random_accidental)
    black_listed_notes: list = [("B", "sharp"), ("E", "sharp"), ("F", "flat")]

    # make sure to NOT choose 
    while (key in black_listed_notes):
        random_scale_letter = chr(random.randint(65, 71)) 
        random_accidental = random.choice(["sharp", "flat", None])
        key: str = (random_scale_letter, random_accidental)

    mode_map = {
        ("C", "flat"): ["major", "lydian"],
        ("C", "sharp"): ["major", "dorian", "phrygian", "mixolydian", "locrian", "minor"],
        ("D", "flat"): ["major", "dorian", "lydian", "mixolydian"],
        ("D", "sharp"): ["dorian", "phrygian", "locrian", "minor"],
        ("E", "flat"): ["major", "dorian", "phrygian", "lydian", "mixolydian", "minor"],
        ("F", "sharp"): ["major", "dorian", "phrygian", "lydian", "mixolydian", "locrian", "minor"],
        ("G", "flat"): ["major", "lydian", "mixolydian"],
        ("G", "sharp"): ["dorian", "phrygian", "mixolydian", "locrian", "minor"],
        ("A", "flat"): ["major", "dorian", "lydian", "mixolydian", "minor"],
        ("A", "sharp"): ["phrygian", "locrian", "minor"],
        ("B", "flat"): ["major", "dorian", "phrygian", "lydian", "mixolydian", "locrian", "minor"]
    }
    mode_list: list = mode_map[key] if key in mode_map else ["major", "dorian", "phrygian", "lydian", "mixolydian", "locrian", "minor"]

    # add other minor modes if possible
    if mode_list[-1] == "minor":
        mode_list = ["natural minor", "harmonic minor", "melodic minor"]

    random_mode: str = random.choice(mode_list)

    return (random_scale_letter, random_mode, random_accidental)


def get_xml(letter: str, scale_mode: str, accidental: str = None) -> str:
    assert scale_mode in SCALE_MAP, f"Invalid scale_mode {scale_mode}"
    
    SCALE_STEPS: list = SCALE_MAP[scale_mode]
    BASE_ASCII: int = 65
    TONIC_ASCII: int = ord(letter) - BASE_ASCII

    curr_letter: str = letter
    curr_octave: int = 4
    bonus: int = (1 if (accidental == "sharp")
        else -1 if (accidental == "flat")
        else 0)
    result: str = ""


    for i in range(8):
        # i is the scale-degree with 0-based indexing
        prev_letter: str = curr_letter
        curr_letter_ascii = BASE_ASCII + ((TONIC_ASCII + i) % 7) # formula
        curr_letter = chr(curr_letter_ascii)

        # increment the octave when the current letter is "C"
        if (i > 0 and curr_letter == "C"):
            curr_octave += 1
        
        # Adjust accidentals if needed
        curr_accidental: str = None
        if (i > 0):
            step: int = SCALE_STEPS[i-1] # step structure for the scale
            letter_dist: int = NoteInfoHandler.get_half_step_adjacent_notes(curr_letter, prev_letter) - bonus

            if (letter_dist - step == 1):
                curr_accidental = "flat"
                bonus = -1
            elif (letter_dist - step == 2):
                curr_accidental = "flat-flat"
                bonus = -2
            elif (letter_dist - step == -2):
                curr_accidental = "double-sharp"
                bonus = 2
            elif (letter_dist - step == -1):
                curr_accidental = "sharp"
                bonus = 1
            else:
                bonus = 0
        else:
            # sharpen or flatten the first note, the tonic (C# major / minor for instance)
            if (bonus == 1):
                curr_accidental = "sharp"
            elif (bonus == -1):
                curr_accidental = "flat"

        note = NoteBuilder() \
            .set_step(curr_letter) \
            .set_octave(curr_octave) \
            .set_accidental(curr_accidental) \
            .build()
        note_xml: str = note.get_xml()
        result += note_xml

    return result

class ScaleInfo(object):
    def __init__(self, start_letter: str,
                scale_mode: str, 
                start_accidental: str, 
                xml: str, svg: str):
        self.scale_mode: str = scale_mode
        self.start_letter: str = start_letter
        self.start_accidental: str = start_accidental
        self.xml: str = xml
        self.scale_name = format_scale_name(start_letter, 
            scale_mode, 
            start_accidental)
        self.svg = svg
        
        # Answer fields go here. They have to use hyphens
        # Use setattr() to add scale-answer to the thing
        setattr(self, "scale-answer", self.scale_name)


class ScaleGenerator:
    def generate() -> ScaleInfo:
        (start_letter, scale_mode, start_accidental) = get_random_scale_info()
        notes_xml: str = get_xml(
            start_letter, scale_mode, start_accidental
        )
        xml: str = MusicRenderer.render_single_staff_template(
            notes_xml=notes_xml
        ) 
        svg: str = MusicRenderer.render_to_svg(xml)

        return ScaleInfo(
            start_letter=start_letter, 
            scale_mode=scale_mode, 
            start_accidental=start_accidental, 
            xml=xml,
            svg=svg
        )