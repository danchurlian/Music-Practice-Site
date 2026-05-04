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

    try {
        const formData = new FormData(event.target);

        // Get the user input
        // turn to lowercase
        // replace hashtags with s
        const userAns = formData.get("random-pitch-answer")
                                .toLowerCase()
                                .replace("#", "s");

        // The pitch number of the random note
        const currentAnswer = answers["pitch-audio-page"]["current-pitch-number-answer"];

        // Call the backend with (user input, current answer), 
        // backend converts user input which is a note name
        // into a number and see if it matches the answer
        const [userNoteNumberString, actualNoteName] = await Promise.all([

            // Call the backend to get the note number that the user added.
            fetch(`/notenumber?ans=${userAns}`)
                .then(result => result.text()),

            // Get the actual note name answer, which will be stored
            // in the answer result div
            fetch(`/notenumber-to-name?${currentAnswer}`)
                .then(result => result.text()),

        ]); // Error handling is handled by the surrounding catch block

        let feedbackString = "Wrong!";

        // Evaluating the user input if possible
        try {
            const noteCode = parseInt(userNoteNumberString);
            
            // Compare and put the result in the answer result div
            if (currentAnswer === noteCode)
                feedbackString = "Correct!";

        } catch (err) {
            console.log(`Failed to parse number. Error: ${err}`);

        } finally {
            feedbackString += ` That was a ${actualNoteName}.`;
            answerResultDiv.textContent = feedbackString;
        }

    } catch (err) {
        answerResultDiv.textContent = `Error processing user input. 
        Generating new random note...`;
        console.error(`Error submitting data ${err}`)
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