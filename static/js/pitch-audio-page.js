import {playAudio} from "./audio-handler.js";

let refButton = document.getElementById("reference-button");
let randomButton = document.getElementById("random-pitch-button");
let form = document.querySelector("form");

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
            // Evaluating the user input if possible
            try {
                const noteCode = parseInt(text);
                
                // Compare with the answer in the global state the compare
                const currentAnswer = answers["pitch-audio-page"]["current-pitch-number-answer"];

                console.log(`Current answer: ${currentAnswer} 
                    | User answer: ${noteCode}`);

                console.log(currentAnswer === noteCode ? 
                    "That is right!" : "Wrong!");

            } catch {
                console.log("Failed to parse number");
            }

            // Generate a new audio
            newRandomPitchCode();
        })
        .catch(err => {
            console.error("Failed to fetch /notenumber");
        });
    
})