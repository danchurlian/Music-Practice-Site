import {playAudio} from "./audio-handler.js"

const LISTEN_COOLDOWN_MS = 1500;
let playingSound = false;

let noteNum1 = null;
let noteNum2 = null;
let curIntervalAnsStr = null;


/* This function sets the global variables to random numbers */
async function setNewNotes() {
    /* 
    Fetch the api endpoint
    Get the json file
    Set the global answer from the json
    Set the note numbers from the json
    If there is an error of some sort then we are cooked
    */
    const GENERATE_API_URL = "/pitch-interval-generate";
    const resultJson = await fetch(GENERATE_API_URL)
        .then(result => result.json());
    
    noteNum1 = resultJson["note_num_1"];
    noteNum1 = resultJson["note_num_2"];
    curIntervalAnsStr = resultJson[resultJson.answer];
}


const button = document.getElementById("interval-button");
button.addEventListener("mouseup", event => {
    if (!playingSound) {
        playingSound = true;
        console.log(`Playing ${noteNum1} and ${noteNum2}`);
        playAudio(noteNum1);
        playAudio(noteNum2);

        // Disable debounce after waiting for 1.5 seconds
        setTimeout(() => {playingSound = false}, LISTEN_COOLDOWN_MS);
    }
});