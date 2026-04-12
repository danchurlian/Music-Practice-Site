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
current_chord_answer: str = ""
current_pitch_answer: int = None
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
@app.route("/key-signature")
def key_signature_page():
    return render_template("key_signature_page.html")

@app.route("/key-signature-generate")
def key_signature_generate():
    info: KeySignatureInfo = KeySignatureGenerator.generate()
    return info.__dict__


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


@app.route("/chord-generate")
def chord_generate() -> str:
    chord_info: ChordInfo = ChordGenerator.generate()
    return chord_info.__dict__


@app.route("/scale-generate")
def fetch_scale_svg() -> str:
    scale_info: ScaleInfo = ScaleGenerator.generate()
    scale_info.xml = music_single_staff_xml(scale_info.xml)
    return scale_info.__dict__


@app.route("/scales")
def scale_page():
    return render_template("scale_page.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
