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


async function onSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    // Get the user input
    // turn to lowercase
    // replace hashtags with s
    const userAns = formData.get("random-pitch-answer")
                            .toLowerCase()
                            .replace("#", "s");


    // Compare with the answer in the global state the compare
    // The current answer is the pitch number of the random note
    const currentAnswer = answers["pitch-audio-page"]["current-pitch-number-answer"];

    // TODO: Call the backend with (user input, current answer), 
    // backend converts user input which is a note name
    // into a number and see if it matches the answer

    // Call the backend to get the note number that the user added.
    const noteNumberApiResult = await fetch(`/notenumber?ans=${userAns}`);
    const noteNumberApiResultText = await noteNumberApiResult.text();


    // Get the actual note name answer, which will be stored
    // in the answer result div
    const actualAnswerResult = await fetch(
        `/notenumber-to-name?${currentAnswer}`
    );
    const actualNoteAnswer = await(actualAnswerResult.text());
    let feedbackString = "Wrong!";

    // Evaluating the user input if possible
    try {
        const noteCode = parseInt(noteNumberApiResultText);
        
        // Compare and put the result in the answer result div
        if (currentAnswer === noteCode)
            feedbackString = "Correct!";
    } catch (err) {
        console.log(`Failed to parse number. Error: ${err}`);
    } finally {
        feedbackString += ` That was a ${actualNoteAnswer}.`;
        answerResultDiv.textContent = feedbackString;
    }

    // Clear the input of the user input
    userInputField.value = "";
    // Generate a new audio
    newRandomPitchCode();
}


// On user submit
form.addEventListener("submit", (event) => {
    onSubmit(event);
})