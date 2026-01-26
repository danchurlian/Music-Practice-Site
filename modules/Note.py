class Note(object):
    def __init__(self, step: str, octave: int, note_type: str, is_chord: bool, accidental: str):
        self.step = step
        self.octave = octave
        self.note_type = note_type
        self.is_chord = is_chord
        self.accidental = accidental
    
    def __repr__(self):
        return f"{self.step} {self.octave} {self.note_type} {self.is_chord}"

    def get_xml(self) -> str:
        return f"""
<note>
    {"<chord />" if self.is_chord is True else ""}
    <pitch>
        <step>{self.step}</step>
        <octave>{self.octave}</octave>
    </pitch>
    {f"<accidental>{self.accidental}</accidental>" if self.accidental is not None else ""}
    <type>{self.note_type}</type>
</note>
"""