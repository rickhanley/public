circle_of_fifths = {
    "C": "guitar_neck",
    "G": "guitar_neck",
    "D": "guitar_neck",
    "A": "guitar_neck",
    "E": "guitar_neck",
    "B": "guitar_neck",
    "F#": "guitar_neck",
    "C#": "guitar_neck",
    "Db": "guitar_neck_flats",
    "Ab": "guitar_neck_flats",
    "Eb": "guitar_neck_flats",
    "Bb": "guitar_neck_flats",
    "F": "guitar_neck_flats",
        }

scales_dict = {
    "Major" : [-17,-15,-13,-12,-10,-8,-7,-5,-3,-1,0,2,4,5,7,9,11,12,14,16,17],
    "Minor" : [-17,-16,-14,-12,-10,-9,-7,-5,-4,-2,0,2,3,5,7,8,10,12,14,15,17],
    "Major Pentatonic": [-17,-15,-12,-10,-8,-5,-3,0,2,4,7,9,12,14,16,19],
    "Minor Pentatonic": [-17,-14,-12,-9,-7,-5,-2,0,3,5,7,10,12,15,17],
    "Whole Tone" : [-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18],
    "Jazz Melodic Minor": [-17,-15,-13,-12,-10,-9,-7,-5,-3,-1,0,2,3,5,7,9,11,12,14,15,17],
    "Dorian": [-17,-15,-14,-12,-10,-9,-7,-5,-3,-2,0,1,3,5,7,8,10,12,13,15,17],
    "Phrygian": [-17,-15,-14,-12,-10,-9,-7,-5,-3,-2,0,1,3,5,7,8,10,12,13,15,17],
    "Lydian": [-17,-15,-13,-12,-10,-8,-6,-5,-3,-1,0,2,4,5,7,9,10,12,14,16,17],
    "Mixolydian": [-17,-15,-14,-12,-10,-8,-7,-5,-3,-2,0,2,3,5,7,8,10,12,14,15,17],
    "Locrian": [-18,-16,-14,-12,-11,-9,-7,-6,-4,-2,0,1,3,5,6,8,10,12,13,15,17],
    "Harmonic Minor": [-17,-16,-13,-12,-10,-9,-7,-5,-4,-1,0,2,3,5,7,8,11,12,14,15,17],
    "Blues": [-17,-14,-12,-9,-8,-7,-6,-5,-2,0,3,4,5,6,7,10,12,15,16,17],
    "Diminished": [-18,-16,-15,-13,-12,-10,-9,-7,-6,-4,-3,-1,0,2,3,5,6,8,9,11,12,13,15,16,18],
    "Lydian b 7": [-17,-15,-14,-12,-10,-8,-6,-5,-3,-2,0,2,4,6,7,9,10,12,14,16,18]
    }
# use as a lookup so the root note can be found on the specified string and calculations of other notes in realtion to that can be performed
guitar_neck = {
    "1": ["E","F","F#","G","G#","A","A#","B","C","C#","D","D#","E","F","F#","G"],
    "2": ["B","C","C#","D","D#","E","F","F#","G","G#","A","A#","B","C","C#","D"],
    "3": ["G","G#","A","A#","B","C","C#","D","D#","E","F","F#","G","G#","A","A#"],
    "4": ["D","D#","E","F","F#","G","G#","A","A#","B","C","C#","D","D#","E","F"],
    "5": ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#","A","A#","B","C"],
    "6": ["E","F","F#","G","G#","A","A#","B","C","C#","D","D#","E","F","F#","G"],
}

guitar_neck_flats = {
    "1": ["E","F","Gb","G","Ab","A","Bb","B","C","Db","D","Eb","E","F","Gb","G"],
    "2": ["B","C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B","C","Db","D"],
    "3": ["G","Ab","A","Bb","B","C","Db","D","Eb","E","F","Gb","G","Ab","A","Gb"],
    "4": ["D","Eb","E","F","Gb","G","Ab","A","Bb","B","C","Db","D","Eb","E","F"],
    "5": ["A","Bb","B","C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B","C"],
    "6": ["E","F","Gb","G","Ab","A","Bb","B","C","Db","D","Eb","E","F","Gb","G"],
}

master_notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B","C","C#","D","D#","E","F","F#","G","G#","A","A#","B",]
master_notes_flats = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B","C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B",]

master_intervals = ["R","m2","M2","m3","M3","P4","b5","P5","m6","M6","m7","M7",
                    "R","b9","9","#9","M3","11","b5","P5","#5","13","m7","M7",
                    "R","b9","9","#9","M3","11","#11","P5","#5","13","m7","M7",
                    "R","b9","9","#9","M3","11","#11","P5","#5","13","m7","M7"]

master_intervals_extended = ["R","m2","M2","m3","M3","P4","b5","P5","m6","M6","m7","M7",
                             "R","b9","9","#9","M3","11","b5","P5","#5","13","m7","M7",
                             "R","b9","9","#9","M3","11","#11","P5","#5","13","m7","M7",
                             "R","b9","9","#9","M3","11","#11","P5","#5","13","m7","M7"]
