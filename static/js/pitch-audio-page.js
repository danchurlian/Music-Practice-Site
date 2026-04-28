import {playAudio} from "./audio-handler.js";

// HTML elements 
const refButton = document.getElementById("reference-button");
const randomButton = document.getElementById("random-pitch-button");
const form = document.querySelector("form");
const answerResultDiv = document.querySelector(".answer-result");
const userInputField = document.querySelector("input");


// Mutable global state
const answers = {
    "pitch-audio-page": {
        "current-pitch-number-answer": 0,
    }
};


// Generates a new random code number
// SIDE EFFECT: Changes the global answers state
const newRandomPitchCode = () => {
    const result = Math.floor((Math.random() * 13 + 1));
    answers["pitch-audio-page"]["current-pitch-number-answer"] = result;
    return result;
}

// ------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    newRandomPitchCode();
});

refButton.addEventListener("mouseup", () => {
    playAudio(1);
});

randomButton.addEventListener("mouseup", () => {
    playAudio(answers["pitch-audio-page"]["current-pitch-number-answer"]);
});

// On user submit
form.addEventListener("submit", (event) => {
    event.preventDefault();

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

    fetch(`/notenumber?ans=${userAns}`)
        .then(result => result.text())
        .then(text => {
            // Evaluating the user input if possible
            try {
                const noteCode = parseInt(text);
                
                // Compare with the answer in the global state the compare
                const currentAnswer = answers["pitch-audio-page"]["current-pitch-number-answer"];
                
                // Compare and put the result in the answer result div
                let feedbackString = currentAnswer === noteCode ? 
                    "Correct!" : "Wrong!";
                feedbackString += " That was a [note name]."
                answerResultDiv.innerHTML = feedbackString;

            } catch {
                console.log("Failed to parse number");
            }

            // Generate a new audio
            newRandomPitchCode();

            // Clear the input of the user input
            userInputField.value = "";
        })
        .catch(err => {
            console.error("Failed to fetch /notenumber");
        });
})