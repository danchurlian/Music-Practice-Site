from flask import Flask, render_template, request
import verovio
import os
import random
import math

from modules.NoteBuilder import NoteBuilder

app = Flask(__name__)
tk = verovio.toolkit()
tk.setResourcePath(os.path.join(os.path.dirname(verovio.__file__), "data"))
tk.setOptions({
    "inputFrom": "xml",
    "svgViewBox": True,
    "scale": 100,

    "adjustPageHeight": True,
    "adjustPageWidth": True,
    "pageMarginTop": 0,
    "pageMarginBottom": 0,
})

current_scale: str = ""
current_chord_answer: str = ""
current_pitch_answer: int = None

# assume that letter1 > letter2 (backwards for scale)
# only works for letters next to each other
def getHalfStepsAdjacentNotes(letter1: str, letter2: str):
    if (letter1 == "F" and letter2 == "E"):
        return 1
    elif (letter1 == "C" and letter2 == "B"):
        return 1
    else:
        return 2

# assume letter1 > letter2
def get_letter_distance(letter1: str, letter2: str):
    result: int = 0
    curr_ascii: int = ord(letter1)
    next_ascii = (curr_ascii - 65 - 1) % 7 + 65


    while curr_ascii != ord(letter2):
        curr_dist = getHalfStepsAdjacentNotes(chr(curr_ascii), chr(next_ascii)) 
        result += curr_dist
        # print(chr(curr_ascii), chr(next_ascii), curr_dist)
        curr_ascii = next_ascii
        next_ascii = (next_ascii - 65 - 1) % 7 + 65

    return result


# Returns a list of tuples that look like this ("A", 4, "sharp") or ("C", 5, None)
# 1st element represents the letter of the note.
# 2nd element represents the octave of the note.
# "None" accidental indicates natural.
def get_note_info_by_intervals(letter: str, accidental: str, intervals: list[int]):

    # Major [4, 3], 4 means 2 whole steps, 2 letters
    # 3 means 1 whole step, 1 half step, 2 letters
    # 1 whole step -> 1 letter up or down
    # half step is tricky
    # [C E G], [D F# A], [Db F Ab] These are test cases to try out

    curr_letter: str = letter
    curr_octave: int = 4
    note_info_list: list = []

    bonus: int = 0
    if (accidental == "sharp"):
        bonus = 1
    elif (accidental == "flat"):
        bonus = -1
    
    note_info_list.append((curr_letter, curr_octave, accidental))

    for i in range(len(intervals)):
        # Get the next letter based on the number of half steps
        prev_letter: str = curr_letter
        prev_num: int = ord(prev_letter) - 65
        interval: int = intervals[i]
        letter_offset: int = math.ceil(interval / 2)
        curr_letter_ascii = 65 + ((prev_num + letter_offset) % 7) # formula
        curr_letter = chr(curr_letter_ascii)

        # increment the octave when the current letter is "C"
        if (ord(prev_letter) < ord("C") and  curr_letter_ascii >= ord("C")):
            curr_octave += 1
        
        # Adjust accidentals if needed
        curr_accidental: str = None
        letter_dist: int = get_letter_distance(curr_letter, prev_letter)
        letter_dist -= bonus

        if (letter_dist - interval == 1):
            curr_accidental = "flat"
            bonus = -1
        elif (letter_dist - interval == 2):
            curr_accidental = "flat-flat"
            bonus = -2
        elif (letter_dist - interval == -2):
            curr_accidental = "double-sharp"
            bonus = 2
        elif (letter_dist - interval == -1):
            curr_accidental = "sharp"
            bonus = 1
        else:
            bonus = 0

        info = (curr_letter, curr_octave, curr_accidental)
        note_info_list.append(info)

    return note_info_list
    

def get_scale_xml(letter: str, mode: str, accidental: str = None) -> str:
    scale_map: dict = {
        "major": [2, 2, 1, 2, 2, 2, 1],
        "minor": [2, 1, 2, 2, 2, 2, 1],
        "harmonic minor": [2, 1, 2, 2, 1, 3, 1],
        "natural minor": [2, 1, 2, 2, 1, 2, 2],
        "dorian": [2, 1, 2, 2, 2, 1, 2],
        "phrygian": [1, 2, 2, 2, 1, 2, 2],
        "lydian": [2, 2, 2, 1, 2, 2, 1], 
        "mixolydian": [2, 2, 1, 2, 2, 1, 2],
        "locrian": [1, 2, 2, 1, 2, 2, 2],
    }
    assert (mode in scale_map), f"Invalid mode {mode}"
    SCALE_STEPS: list = scale_map[mode]
    
    # info_list: list = get_note_info_by_intervals(letter, accidental, SCALE_STEPS)
    # for info in info_list:
    #     (curr_letter, curr_octave, curr_accidental) = info
    #     note = NoteBuilder() \
    #         .set_step(curr_letter) \
    #         .set_octave(curr_octave) \
    #         .set_accidental(curr_accidental) \
    #         .build()
    #     result += note.get_xml()

    result: str = ""
    BASE_ASCII: int = 65
    TONIC_ASCII: int = ord(letter) - BASE_ASCII

    curr_letter: str = letter
    curr_octave: int = 4
    bonus: int = 1 if (accidental == "sharp") else -1 if (accidental == "flat") else 0

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
            letter_dist: int = getHalfStepsAdjacentNotes(curr_letter, prev_letter) - bonus

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


def music_xml() -> str:
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
    <part-list>
        <score-part id="P1">
        </score-part>
    </part-list>
    <part id="P1">
        <measure number="1">
            <attributes>
                <divisions>1</divisions>
                <key>
                    <fifths>0</fifths>
                </key>
                <time>
                    <beats>4</beats>
                    <beat-type>4</beat-type>
                </time>
                <staves>1</staves>
                <clef number="1">
                    <sign>G</sign>
                    <line>2</line>
                </clef>
            </attributes>
            <NOTES />
        </measure>
    </part>
</score-partwise>
"""

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
        mode_list.extend(["harmonic minor", "natural minor"])

    random_mode: str = random.choice(mode_list)

    return (random_scale_letter, random_mode, random_accidental)


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

def format_chord_name(letter: str, accidental: str, chord_name: str):
    result: str = f"{letter}"
    if (accidental == "sharp"):
        result += "#"
    elif (accidental == "flat"):
        result += "b"
    
    result += f" {chord_name}"

    return result



def create_chord(chord_info: list[tuple]) -> str:
    result_xml: str = ""
    for i, info in enumerate(chord_info):
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

# note_name can be "C#" or "Db" or "A"
def get_note_code(note_name: str) -> int:
    map: dict = {
        "B#": 1,
        "C": 1,
        "C#": 2,
        "Db": 2,
        "D": 3,
        "D#": 4,
        "Eb": 4,
        "E": 5,
        "Fb": 5,
        "E#": 6,
        "F": 6,
        "F#": 7,
        "Gb": 7,
        "G": 8,
        "G#": 9,
        "Ab": 9,
        "A": 10,
        "A#": 11,
        "Bb": 11,
        "B": 12,
        "Cb": 12,
    }
    if (note_name not in map):
        raise ValueError()
    return map[note_name]


@app.route("/pitch-audio", methods=["GET", "POST"])
def pitch_audio_page():
    global current_pitch_answer
    feedback: str = ""

    if (request.method == "POST"):
        correct: bool = True
        user_input: str = request.form.get("user_answer")
        try:
            user_code: int = get_note_code(user_input)
            correct = user_code == current_pitch_answer
            print(f"User input {user_input} | note code {user_code}")
        except ValueError:
            correct = False 

        if (correct is True):
            feedback = f"Correct! That was a(n) \"{user_input}\"."
        else:
            feedback = "Wrong!"
        
    reference_code: int = 1 # middle C
    random_code: int = random.randint(1, 12)
    current_pitch_answer = random_code
    audio_file_name: str = f"note{random_code}.mp3"
    
    return render_template("pitch_audio_page.html", reference_code=reference_code, random_code=random_code, feedback=feedback, audio_file_name=audio_file_name)

@app.route("/chords", methods=["GET", "POST"])
def chord_page():
    global current_chord_answer

    # Handle user input
    feedback: str = "Enter something in!"
    if (request.method == "POST"):
        user_answer: str = request.form.get("chord_answer")
        if (current_chord_answer != ""):
            feedback = "Correct!" if user_answer == current_chord_answer else "Wrong!"
            feedback += f" The correct answer was \"{current_chord_answer}\"."

    possible_chords: dict = {
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

    interval_map: dict = {
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
    random_letter: str = chr(64 + random.randint(1, 7))
    random_accidental: int = random.choice(["flat", "sharp", None])
    key = (random_letter, random_accidental)
    
    # Get a random chord and generate the intervals
    possible_chord_list: list = list(interval_map.keys()) if (key not in possible_chords) else possible_chords[key]
    random_chord_name: str = random.choice(possible_chord_list)

    random_interval_list: list = interval_map[random_chord_name]
    answer: str = format_chord_name(*key, random_chord_name)
    current_chord_answer = answer

    # Generate the notes
    chord_info_list = get_note_info_by_intervals(*key, random_interval_list)
    notes_xml: str = create_chord(chord_info_list)

    xml_template: str = music_xml().replace("<NOTES />", notes_xml)
    tk.loadData(xml_template)
    music_svg: str = tk.renderToSVG(1)
    return render_template("chord_page.html", music_svg=music_svg, feedback=feedback)


@app.route("/scales", methods=["GET", "POST"])
def scale_page():
    global current_scale

    # evaluate user input
    answer_result: str = "Enter something..."
    if request.method == "POST":
        user_input: str = request.form.get('user_input')

        if (user_input == current_scale):
            answer_result = f"You're right! That was \"{current_scale}\"."
        else:
            answer_result = f"You're wrong! The previous scale answer was \"{current_scale}\"."

    # generate random scale
    (random_scale_letter, random_mode, random_accidental) = get_random_scale_info()
    real_answer: str = format_scale_name(random_scale_letter, random_mode, random_accidental) 
    current_scale = real_answer

    # render the scale on the page
    xml: str = music_xml()
    xml = xml.replace("<NOTES />", get_scale_xml(random_scale_letter, random_mode, random_accidental))
    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)
    return render_template("scale_page.html", music_svg=music_svg, answer_result=answer_result)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
