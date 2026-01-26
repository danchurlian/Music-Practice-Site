from .Note import Note

class NoteBuilder(object):
    def __init__(self):
        self.step = "C"
        self.octave = 4
        self.note_type = "quarter"
        self.accidental = None 
        self.is_chord = False
    
    def set_step(self, step: str):
        self.step = step
        return self

    def set_octave(self, octave: int):
        self.octave = octave
        return self

    def set_note_type(self, note_type: str):
        self.note_type = note_type
        return self

    def set_is_chord(self, is_chord: bool):
        self.is_chord = is_chord
        return self

    def set_accidental(self, accidental: str):
        self.accidental = accidental
        return self

    def build(self):
        return Note(self.step, self.octave, self.note_type, self.is_chord, self.accidental)