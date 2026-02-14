import math

class NoteInfoHandler:
    # PRECONDITION: letter1 > letter2
    # PRECONDITION: only works for letters next to each other
    def get_half_step_adjacent_notes(letter1: str, letter2: str):
        if (letter1 == "F" and letter2 == "E"):
            return 1
        elif (letter1 == "C" and letter2 == "B"):
            return 1
        else:
            return 2


    # Returns the number of half-steps between letter1 and letter2
    # PRECONDITION: letter1 > letter2
    def get_letter_distance(letter1: str, letter2: str):
        result: int = 0
        curr_ascii: int = ord(letter1)
        next_ascii = (curr_ascii - 65 - 1) % 7 + 65

        while curr_ascii != ord(letter2):
            curr_dist = NoteInfoHandler.get_half_step_adjacent_notes(chr(curr_ascii), chr(next_ascii)) 
            result += curr_dist
            curr_ascii = next_ascii
            next_ascii = (next_ascii - 65 - 1) % 7 + 65

        return result
    
    # Returns a list of tuples that look like this ("A", 4, "sharp") or ("C", 5, None)
    # 1st element represents the letter of the note.
    # 2nd element represents the octave of the note.
    # "None" accidental indicates natural.
    def get_note_info_by_intervals(letter: str, accidental: str, intervals: list[int]):

        # Major [4, 3], 4 means 2 whole steps, 2 letters
        # 3 means 1 whole step, 1 half step, 2 letters
        # 1 whole step -> 1 letter up or down
        # half step is tricky
        # [C E G], [D F# A], [Db F Ab] These are test cases to try out

        curr_letter: str = letter
        curr_octave: int = 4
        note_info_list: list = []

        bonus: int = 0
        if (accidental == "sharp"):
            bonus = 1
        elif (accidental == "flat"):
            bonus = -1
        
        note_info_list.append((curr_letter, curr_octave, accidental))

        for i in range(len(intervals)):
            # Get the next letter based on the number of half steps
            prev_letter: str = curr_letter
            prev_num: int = ord(prev_letter) - 65
            interval: int = intervals[i]
            letter_offset: int = math.ceil(interval / 2)
            curr_letter_ascii = 65 + ((prev_num + letter_offset) % 7) # formula
            curr_letter = chr(curr_letter_ascii)

            # increment the octave when the current letter is "C"
            if (ord(prev_letter) < ord("C") and  curr_letter_ascii >= ord("C")):
                curr_octave += 1
            
            # Adjust accidentals if needed
            curr_accidental: str = None
            letter_dist: int = NoteInfoHandler.get_letter_distance(curr_letter, prev_letter)
            letter_dist -= bonus

            if (letter_dist - interval == 1):
                curr_accidental = "flat"
                bonus = -1
            elif (letter_dist - interval == 2):
                curr_accidental = "flat-flat"
                bonus = -2
            elif (letter_dist - interval == -2):
                curr_accidental = "double-sharp"
                bonus = 2
            elif (letter_dist - interval == -1):
                curr_accidental = "sharp"
                bonus = 1
            else:
                bonus = 0

            info = (curr_letter, curr_octave, curr_accidental)
            note_info_list.append(info)

        return note_info_list