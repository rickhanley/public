console.log("Javascript seen")

console.log("script.js Root:", root);
console.log("script.js Family:", family);




// chordformulas is an object of chord family types
// Major, Minor, Minor 7 etc with the intervals of
// the notes listed out - the chord formula.

let chordFormulas = {
    Major: [0, 4, 7],
    Minor: [0, 3, 7],
    Minor7: [0, 3, 7, 10],
    Major7: [0, 4, 7, 11],
    Seventh: [0, 4, 7, 10],
    Sus2: [0, 2, 7],
    Sus4: [0, 4, 7],
    Aug: [0, 4, 8],
    thirteenth: [0, 4, 7, 10, 14, 17, 21]
}
let chromaticScale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
// console.log(`Index of the root: ${chromaticScale.indexOf(root)}`);


// function to create an array of 12 notes rising chromatically
// from the given root. Takes in a chromatic scale starting at
// C. Starts looping from the index of the root note, and resets
// the j counter to 0 when it reaches 12 to go back to the start.
// The i counter makes sure we gather 12 notes total.

function scaleFromRoot(root, chromaticScale){
    let j = chromaticScale.indexOf(root);
    let userScale = [];

    for(let i = 0; i < 24; i++ ) {
        // if(j == 12) {
        //     j = 0;
        // };
        // console.log(`i: ${i}    j: ${j}`)
        userScale[i] = chromaticScale[j];
        j++;
    };
    return userScale;
};

let notes = scaleFromRoot(root, chromaticScale);

// function to return the notes for the given chord family.
// takes the chromatic scale as input starting from the root
// note as given by the user. Takes the chord family as input
// also so it knows which intervals to select from the scale.
// returns an array of chord tones.

function chordTones (notes, family) {
    let chord = [];
    if (family in chordFormulas) {
        // console.log(`Found ${family}`)
        for (note in chordFormulas[family])
            {
                // console.log(notes[chordFormulas[family][note]]);
                chord[note] = notes[chordFormulas[family][note]];
            }
        // console.log(chordFormulas[family])
    }
    return chord;
}


console.log(chordTones (notes, family));
