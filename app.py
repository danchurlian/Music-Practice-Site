from flask import Flask, render_template, request
from jinja2 import Environment, Template, PackageLoader
import verovio
import os
import random

from modules.NoteInfoHandler import NoteInfoHandler
from modules.ScaleGenerator import ScaleGenerator, ScaleInfo
from modules.ChordGenerator import ChordGenerator, ChordInfo
from modules.KeySignatureGenerator import (KeySignatureGenerator,
                                            KeySignatureInfo)
from modules.PitchIntervalGenerator import (PitchIntervalGenerator,
                                             PitchIntervalInfo)
# Config Flask
app = Flask(__name__)

# Config Verovio library
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


# Setup Jinja environment
jinja_env: Environment = Environment(
    loader=PackageLoader("app")
)


# Global variables for evaluating answers
current_scale: str = ""
current_chord_answer: str = ""
current_pitch_answer: int = None
current_major_key_answer: str = ""
current_minor_key_answer: str = ""
current_pitch_interval_answer: str = "'"

# called by chord_page() and scale_page()
def music_single_staff_xml(notes_xml: str) -> str:
    template: Template = jinja_env.get_template("single_staff_template.xml")
    return template.render(attributes="<divisions>1</divisions>", notes=notes_xml)


# WEB PAGE URL FUNCTIONS -------------------------------------------------------
@app.route("/pitch-intervals", methods=["GET", "POST"])
def pitch_interval_page():
    global current_pitch_interval_answer
    feedback: str = "You will hear two notes. Identify the interval between them."

    if (request.method == "POST"):
        # Add answer feedback feedback 
        user_input: str = request.form["user-response"]
        print(user_input)
        feedback = ("Correct! " if user_input == current_pitch_interval_answer else "Wrong! ") 
        feedback += f"The previous interval was '{current_pitch_interval_answer}'."

    info: PitchIntervalInfo = PitchIntervalGenerator.generate()
    current_pitch_interval_answer = info.answer
    return render_template("pitch_interval_page.html",
                           note_1=info.note_num_1, note_2=info.note_num_2,
                           feedback=feedback)


# Generate a key signature based a single fifths_number from [-7, 7] inclusive.
@app.route("/key-signature", methods=["GET", "POST"])
def key_signature_page():
    global current_major_key_answer, current_minor_key_answer
    feedback_content: str = ""

    # If the user responded, evaluate the user's input.
    if request.method == "POST":
        user_major_input: str = request.form.get("major-key-name").strip()
        user_minor_input: str = request.form.get("minor-key-name").strip()
        print(f"User entered {user_major_input} {user_minor_input}")

        # Check if the user's input matches the global variables at the top
        # Change the feedback content depending correct or not.
        user_is_correct: bool = user_major_input == current_major_key_answer and user_minor_input == current_minor_key_answer
        feedback_content = "Correct!" if user_is_correct is True else "Wrong!"
        
        feedback_content += f" That was {current_major_key_answer} and {current_minor_key_answer}."

    else:
        current_major_key_answer = ""
        current_minor_key_answer = ""

    # Generate a KeySignatureInfo
    key_signature_info: KeySignatureInfo = KeySignatureGenerator.generate()
    current_major_key_answer = key_signature_info.major_name 
    current_minor_key_answer = key_signature_info.minor_name
    fifths_number: int = key_signature_info.fifths_number

    # Render the key signature as an svg and render the html page 
    template: Template = jinja_env.get_template("single_staff_template.xml") 
    xml: str = template.render(attributes=f"""
<divisions>1</divisions>
<key>
    <fifths>{fifths_number}</fifths>
</key>
    """)

    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)
    return render_template("key_signature_page.html", feedback=feedback_content, music_svg=music_svg)


@app.route("/pitch-audio", methods=["GET", "POST"])
def pitch_audio_page():
    global current_pitch_answer
    feedback: str = ""

    if (request.method == "POST"):
        correct: bool = True
        user_input: str = request.form.get("user-answer")
        try:
            user_code: int = NoteInfoHandler.get_note_code(user_input)
            correct = user_code == current_pitch_answer
            print(f"User input {user_input} | note code {user_code}")
        except ValueError:
            correct = False 

        feedback = "Correct!" if correct is True else "Wrong!"
        feedback += (f" That was a(n) {NoteInfoHandler.get_note_name_from_code(current_pitch_answer)}." 
            if current_pitch_answer is not None 
            else "")
        
    reference_code: int = 1 # middle C
    random_code: int = random.randint(1, 12)
    current_pitch_answer = random_code
    audio_file_name: str = f"note{random_code}.mp3"
    
    return render_template("pitch_audio_page.html",
                            reference_code=reference_code, 
                            random_code=random_code,
                            feedback=feedback,
                            audio_file_name=audio_file_name,
                            )


@app.route("/chords", methods=["GET", "POST"])
def chord_page():
    global current_chord_answer

    # Handle user input
    feedback: str = ""
    if (request.method == "POST"):
        user_answer: str = request.form.get("chord-answer")
        if (current_chord_answer != ""):
            feedback = ("Correct!" if user_answer == current_chord_answer 
                        else "Wrong!")
            feedback += f" The correct answer was \"{current_chord_answer}\"."

    # Generate a chord and access its metadata
    chord_info: ChordInfo = ChordGenerator.generate()
    answer: str = chord_info.chord_name
    current_chord_answer = answer

    # Generate the notes and render
    notes_xml: str = chord_info.xml
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
    answer_result: str = ""
    if request.method == "POST":
        user_input: str = request.form.get("user-input")
        if (user_input == current_scale):
            answer_result = f"Correct! That was \"{current_scale}\"."
        else:
            answer_result = f"Wrong! The previous scale answer was \"{current_scale}\"."

    # generate random scale
    scale_info: ScaleInfo = ScaleGenerator.generate()

    real_answer: str = scale_info.scale_name 
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
