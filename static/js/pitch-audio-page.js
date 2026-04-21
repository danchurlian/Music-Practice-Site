import {playAudio} from "./audio-handler.js";

let randomPitchCode = null;

let refButton = document.getElementById("reference-button");
let randomButton = document.getElementById("random-pitch-button");
let form = document.querySelector("form");

const newRandomPitchCode = () => {
    return Math.floor((Math.random() * 13 + 1));
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
    console.log(formData.get("user-answer"));

    // Generate a new audio
    randomPitchCode = newRandomPitchCode();
})