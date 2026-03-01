import random

INTERVAL_MAPPING: list = [
    "perfect unison",
    "minor 2nd",
    "major 2nd",
    "minor 3rd",
    "major 3rd",
    "perfect 4th",
    "tritone",
    "perfect 5th",
    "minor 6th",
    "major 6th",
    "minor 7th",
    "major 7th",
    "perfect octave"
]

class PitchIntervalInfo:
    def __init__(self, note_num_1: int, note_num_2: int, answer: str):
        self.note_num_1 = note_num_1
        self.note_num_2 = note_num_2
        self.answer = answer

class PitchIntervalGenerator:
    def generate():
        note_num_1: int = random.randint(1, 13) 
        note_num_2: int = random.randint(1, 13) 

        diff: int = abs(note_num_1 - note_num_2) 
        answer: str = INTERVAL_MAPPING[diff]
        return PitchIntervalInfo(note_num_1, note_num_2, answer)