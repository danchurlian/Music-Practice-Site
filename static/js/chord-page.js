const form = document.querySelector("form");
const svgSection = document.getElementById("chord-svg-section");
const chordInputField = document.getElementById("chord-input");
const answerResultDiv = document.getElementById("chord-answer-result");

let currentChordName = "None";

const loadNewSvg = () => {
    fetch("/chord-generate")
        .then(response => response.json())
        .then(chordInfo => {
            const container = document.createElement("div");
            container.innerHTML = chordInfo.svg;
            currentChordName = chordInfo.chord_name;

            svgSection.replaceChildren();
            svgSection.append(container);
            
            chordInputField.value = "";
            chordInputField.focus();
        });
};

document.addEventListener("DOMContentLoaded", () => {
    loadNewSvg();
})

form.addEventListener("submit", (event) => {
    event.preventDefault();
    formData = new FormData(event.target);

    answerResultDiv.innerHTML = (formData.get("chord-answer") == currentChordName) ? "Correct!" : "Wrong!";
    answerResultDiv.innerHTML += ` That was a ${currentChordName} chord.`;

    loadNewSvg();
});