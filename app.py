from flask import Flask, render_template, request
import verovio
import os
import random

app = Flask(__name__)
tk = verovio.toolkit()
tk.setResourcePath(os.path.join(os.path.dirname(verovio.__file__), "data"))
tk.setOptions({
    "inputFrom": "xml",
})

current_scale: str = ""

# assume that letter1 > letter2 (backwards for scale)
def getHalfStepsAdjacentNotes(letter1: str, letter2: str):
    if (letter1 == "F" and letter2 == "E"):
        return 1
    elif (letter1 == "C" and letter2 == "B"):
        return 1
    else:
        return 2
    

def get_scale_xml(letter: str, mode: str) -> str:
    result: str = ""
    base: int = 65
    start_num: int = ord(letter) - base

    curr_letter: str = letter
    curr_octave: int = 4
    bonus: int = 0

    SCALE_STEPS: list = []
    if (mode == "major"):
        SCALE_STEPS = [2, 2, 1, 2, 2, 2, 1]
    elif (mode == "minor"):
        SCALE_STEPS = [2, 1, 2, 2, 2, 2, 1]
    else:
        raise ValueError("major or minor!")

    for i in range(8):
        # i is the scale-degree with 0-based indexing
        prev_letter: str = curr_letter
        curr_letter_ascii = base + ((start_num + i) % 7) # formula
        curr_letter = chr(curr_letter_ascii)

        # increment the octave when the current letter is "C"
        if (i > 0 and curr_letter == "C"):
            curr_octave += 1
        
        # Adjust accidentals if needed
        accidental_tag: str = ""
        if (i > 0):
            step: int = SCALE_STEPS[i-1] # step structure for the scale
            dist: int = getHalfStepsAdjacentNotes(curr_letter, prev_letter) - bonus

            if (dist > step):
                accidental_tag = "<accidental>flat</accidental>"
                bonus = -1
            elif (dist < step):
                accidental_tag = "<accidental>sharp</accidental>"
                bonus = 1
            else:
                bonus = 0

        note_xml: str = f"""
<note>
    <pitch>
        <step>{curr_letter}</step>
        <octave>{curr_octave}</octave>
    </pitch>
    {accidental_tag}
    <duration>1</duration>
    <type>quarter</type>
</note>
"""
        result += note_xml
    return result


def music_xml() -> str:
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
    <part-list>
        <score-part id="P1">
            <part-name>Scale</part-name>
            <part-abbreviation>Scale</part-abbreviation>
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

@app.route("/scales", methods=["GET", "POST"])
def scale_page():
    global current_scale

    answer_result: str = "Enter something..."
    if request.method == "POST":
        user_input: str = request.form.get('user_input')

        if (user_input == current_scale):
            answer_result = "You're right!"
        else:
            answer_result = "You're wrong!"


    # generating the rest of the page
    random_scale_letter: str = chr(random.randint(65, 71)) 
    random_mode: str = random.choice(["major", "minor"])
    real_answer: str = f"{random_scale_letter} {random_mode}"
    current_scale = real_answer


    xml: str = music_xml()
    xml = xml.replace("<NOTES />", get_scale_xml(random_scale_letter, random_mode))
    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)
    return render_template("scale_page.html", music_svg=music_svg, answer_result=answer_result)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
