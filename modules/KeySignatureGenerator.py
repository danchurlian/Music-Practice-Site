from modules import MusicRenderer
import random

KEY_NAMES_BY_FIFTHS_NUMBER: dict = {
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

# Returns a 2-tuple of key names, 1st entry is major key name,
# 2nd entry is the relative minor key name. 
def get_key_signature_info(fifths_number: int) -> list:
    assert fifths_number in KEY_NAMES_BY_FIFTHS_NUMBER, \
        f"Invalid fifths_number {fifths_number}"
    return KEY_NAMES_BY_FIFTHS_NUMBER[fifths_number]


# This record class is used by the app module.
# It contains data about the generated key.
class KeySignatureInfo:
    def __init__(self, fifths_number: str, major_name: str, minor_name: str,
                 xml: str, svg: str):
        self.fifths_number = fifths_number
        self.major_name = major_name
        self.minor_name = minor_name
        self.xml = xml
        self.svg = svg



class KeySignatureGenerator:
    # This generates a KeySignatureInfo instance with random attributes.
    def generate():
        # Generate a random fifths number
        fifths_number: int = random.randint(-7, 7)

        # Get ansewrs based on the fifths number
        major_minor_names: list = get_key_signature_info(fifths_number)
        major_key_answer: str = f"{major_minor_names[0]} major" 
        minor_key_answer: str = f"{major_minor_names[1]} minor"
        total_xml: str = MusicRenderer.render_single_staff_template(
            f"""
<key>
    <fifths>{fifths_number}</fifths>
</key>

"""
        )
        svg: str = MusicRenderer.render_to_svg(total_xml)
        
        return KeySignatureInfo(
            fifths_number=fifths_number,
            major_name=major_key_answer, 
            minor_name=minor_key_answer,
            xml=total_xml,
            svg=svg,
            )