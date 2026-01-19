from flask import Flask, render_template
import verovio
import os

app = Flask(__name__)
tk = verovio.toolkit()
tk.setResourcePath(os.path.join(os.path.dirname(verovio.__file__), "data"))
tk.setOptions({
    "inputFrom": "xml",
})
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
            <note>
                <pitch>
                    <step>C</step>
                    <octave>4</octave>
                </pitch>
                <duration>1</duration>
                <type>quarter</type>
                <stem>up</stem>
            </note>
        </measure>
    </part>
</score-partwise>
"""

@app.route("/scales")
def scale_page():
    xml: str = music_xml()
    print(xml)
    tk.loadData(xml)
    music_svg: str = tk.renderToSVG(1)
    print(music_svg)
    return render_template("scale_page.html", music_svg=music_svg)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
