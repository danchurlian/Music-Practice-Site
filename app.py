from flask import Flask, render_template, request
from jinja2 import Environment, Template, PackageLoader
import verovio
import os
import random

from modules.NoteBuilder import NoteBuilder
from modules.NoteInfoHandler import NoteInfoHandler
from modules.ScaleGenerator import ScaleGenerator, ScaleInfo

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

jinja_env: Environment = Environment(
    loader=PackageLoader("app")
)

current_scale: str = ""
current_chord_answer: str = ""
current_pitch_answer: int = None
current_major_key_answer: str = ""
current_minor_key_answer: str = ""


# called by chord_page() and scale_page()
def music_single_staff_xml(notes_xml: str) -> str:
    template: Template = jinja_env.get_template("single_staff_template.xml")
    return template.render(attributes="<divisions>1</divisions>", notes=notes_xml)


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

# Used only to display the right answer in on the pitch audio page
def get_note_name_from_code(code: int) -> str:
    note_name_list: list = [
        None,
        "C or B#",
        "C# or Db",
        "D",
        "D# or Eb",
        "E or Fb",
        "F or E#",
        "F# or Gb",
        "G",
        "G# or Ab",
        "A",
        "A# or Bb",
        "B or Cb",
    ]
    result: str = None
    assert (code > 0 and code < len(note_name_list), f"Invalid note code {code}")
    result = note_name_list[code]
    return result


def get_key_signature_xml(fifths_number: int) -> str:
    template: Template = jinja_env.get_template("single_staff_template.xml") 
    return template.render(attributes=f"""
<divisions>1</divisions>
<key>
    <fifths>{fifths_number}</fifths>
</key>
    """)


def get_key_signature_info(fifths_number: int) -> list:
    map: dict = {
        -7: ["Cb", "Ab"],
        -6: ["Gb", "Eb"],
        -5: ["Db", "Bb"],
        -4: ["Ab", "F"],
        -3: ["Eb", "C"],
        -2: ["Bb", "G"],
        -1: ["F", "D"],
        0: ["C", "A"],
        1: ["G", "E"],
        2: ["D", "B"],
        3: ["A", "F#"],
        4: ["E", "C#"],
        5: ["B", "G#"],
        6: ["F#", "D#"],
        7: ["C#", "A#"],
    }
    assert fifths_number in map, f"Invalid fifths_number {fifths_number}"
    return map[fifths_number]





# WEB PAGE URL FUNCTIONS -------------------------------------------------------

# Generate a key signature based a single fifths_number from [-7, 7] inclusive.
@app.route("/key-signature", methods=["GET", "POST"])
def key_signature_page():
    global current_major_key_answer, current_minor_key_answer
    feedback_content: str = "Enter something!"

    # If the user responded, get the user's input.
    if request.method == "POST":
        user_major_input: str = request.form.get("major_key_name").strip()
        user_minor_input: str = request.form.get("minor_key_name").strip()
        print(f"User entered {user_major_input} {user_minor_input}")

        # Check if the user's input matches the global variables at the top
        # Change the feedback content depending correct or not.
        user_is_correct: bool = user_major_input == current_major_key_answer and user_minor_input == current_minor_key_answer
        feedback_content = "Correct!" if user_is_correct is True else "Wrong!"
        
        feedback_content += f" That was {current_major_key_answer} and {current_minor_key_answer}."

    else:
        current_major_key_answer = ""
        current_minor_key_answer = ""


    # Generate a random fifths number
    fifths_number: int = random.randint(-7, 7)
    accidental_using: str = "sharp" if fifths_number >= 0 else "flat"

    # Get ansewrs based on the fifths number
    key_sig_info = get_key_signature_info(fifths_number)
    major_key_answer: str = f"{key_sig_info[0]} major" 
    minor_key_answer: str = f"{key_sig_info[1]} minor"
    current_major_key_answer = major_key_answer
    current_minor_key_answer = minor_key_answer

    # Logging
    print(f"{abs(fifths_number)} {accidental_using}s")
    print(f"{current_major_key_answer} | {current_minor_key_answer}")

    # Render the key signature as an svg and render the html page 
    xml: str = get_key_signature_xml(fifths_number)
    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)
    return render_template("key_signature_page.html", feedback=feedback_content, music_svg=music_svg)


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

        feedback = "Correct!" if correct is True else "Wrong!"
        feedback += f" That was a(n) {get_note_name_from_code(current_pitch_answer)}." if current_pitch_answer is not None else ""
        
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

    # Generate the notes and render
    chord_info_list = NoteInfoHandler.get_note_info_by_intervals(*key, random_interval_list)
    notes_xml: str = create_chord(chord_info_list)

    xml: str = music_single_staff_xml(notes_xml)
    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)

    return render_template(
        "chord_page.html", 
        music_svg=music_svg, 
        feedback=feedback)


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
    scale_info: ScaleInfo = ScaleGenerator.generate()
    
    real_answer: str = format_scale_name(
        scale_info.start_letter,
        scale_info.scale_mode,
        scale_info.start_accidental)

    current_scale = real_answer

    # render the scale on the page
    notes_xml: str = scale_info.xml
    xml: str = music_single_staff_xml(notes_xml)
    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)

    return render_template(
        "scale_page.html", 
        music_svg=music_svg, 
        answer_result=answer_result)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
