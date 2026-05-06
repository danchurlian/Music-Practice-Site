import {playAudioAsync} from "./audio-handler.js"

const button = document.getElementById("interval-button");
const form = document.querySelector("form");
const userInputField = document.querySelector("input");
const answerResultDiv = document.querySelector(".answer-result");

const LISTEN_COOLDOWN_MS = 1500;
let playingSound = false;

let noteNum1 = null;
let noteNum2 = null;
let curIntervalAnsStr = null;


/* This function sets the global variables to random numbers
and also set the answer to the name of the interval.
*/
async function setNewNotes() {
    // Fetch the api endpoint
    // Get the json file
    const GENERATE_API_URL = "/pitch-interval-generate";
    const resultJson = await fetch(GENERATE_API_URL)
        .then(result => result.json());
    

    // Set the global answer from the json
    // Set the note numbers from the json
    noteNum1 = resultJson["note_num_1"];
    noteNum2 = resultJson["note_num_2"];
    curIntervalAnsStr = resultJson["answer"];
    console.log(`Setting new notes\n${noteNum1} ${noteNum2}`);
}


// Initialize the pitches when the page loads
document.addEventListener("DOMContentLoaded", () => {
    setNewNotes();
})


form.addEventListener("submit", event => {
    event.preventDefault();
    const formData = new FormData(event.target);

    // Compare the user's data with the answers above
    // Display correct/wrong on the answer result div
    answerResultDiv.textContent = 
        ( formData.get("user-interval-answer") === curIntervalAnsStr ) ?
        "Correct! " : "Wrong!";
        
    // Display the right answer on the result div
    answerResultDiv.textContent += 
        ` The interval was \"${curIntervalAnsStr}\".`;

    // Clear the input
    userInputField.value = "";
    userInputField.focus();

    // Generate the new notes and new answer
    setNewNotes();
})


button.addEventListener("mouseup", event => {
    if (!playingSound) {
        playingSound = true;
        console.log(`Playing ${noteNum1} and ${noteNum2}`);
        playAudioAsync(noteNum1);
        playAudioAsync(noteNum2);

        // Disable debounce after waiting for 1.5 seconds
        setTimeout(() => {playingSound = false}, LISTEN_COOLDOWN_MS);
    }
});