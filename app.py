from flask import Flask, render_template
import verovio
import os

app = Flask(__name__)
tk = verovio.toolkit()
tk.setResourcePath(os.path.join(os.path.dirname(verovio.__file__), "data"))
tk.setOptions({
    "inputFrom": "xml",
})


def get_scale_xml(letter: str, mode: str) -> str:
    result: str = ""
    base: int = 65
    start_num: int = ord(letter) - base
    curr_octave: int = 4

    # Major WWHWWWH OR 2212221, as length 7, do nothing at i == 0
    # possible each loop num half steps from previous note, then sharp/flatten if needed
    # creaitng a scale from the step model, more reliable

    # list of all possible scales and their note-octave pairs, hard-coding way no good

    for i in range(8):
        # i is the scale-degree with 0-based indexing
        curr_letter_ascii = base + ((start_num + i) % 7) # formula
        curr_letter: str = chr(curr_letter_ascii)
        if (i > 0 and curr_letter == "C"):
            curr_octave += 1 # go up a higher octave if needed

        note_xml: str = f"""
<note>
    <pitch>
        <step>{curr_letter}</step>
        <octave>{curr_octave}</octave>
    </pitch>
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

@app.route("/scales")
def scale_page():
    xml: str = music_xml()
    xml = xml.replace("<NOTES />", get_scale_xml("C", "major"))
    print(xml)
    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)
    return render_template("scale_page.html", music_svg=music_svg)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
