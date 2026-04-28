import {playAudio} from "./audio-handler.js";

let randomPitchCode = null;

let refButton = document.getElementById("reference-button");
let randomButton = document.getElementById("random-pitch-button");
let form = document.querySelector("form");

const answers = {
    "pitch-audio-page": {
        "current-pitch-number-answer": 0,
    }
};

// TOOD: Add setting the answer in this method
const newRandomPitchCode = () => {
    const result = Math.floor((Math.random() * 13 + 1));
    answers["pitch-audio-page"]["current-pitch-number-answer"] = result;
    return result;
}

document.addEventListener("DOMContentLoaded", () => {
    randomPitchCode = newRandomPitchCode();
});
refButton.addEventListener("mouseup", () => {
    playAudio(1);
});
randomButton.addEventListener("mouseup", () => {
    playAudio(randomPitchCode);
});

// On user submit
form.addEventListener("submit", (event) => {
    event.preventDefault();

    console.log("Submitted");
    const formData = new FormData(event.target);

    // Get the user input
    // turn to lowercase
    // replace hashtags with s
    const userAns = formData.get("random-pitch-answer")
                            .toLowerCase()
                            .replace("#", "s");

    // TODO: Call the backend with (user input, current answer), 
    // backend converts user input which is a note name
    // into a number and see if it matches the answer
    console.log(userAns);

    fetch(`/notenumber?ans=${userAns}`)
        .then(result => result.text())
        .then(text => {
            try {
                const noteCode = parseInt(text);
                console.log(`Backend notecode result: ${noteCode}`)
            } catch {
                console.log("Failed to parse number");
            }
        })
    

    // Generate a new audio
    randomPitchCode = newRandomPitchCode();
})