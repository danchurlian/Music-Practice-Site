const svgSection = document.getElementById("keysig-svg-section");
const form = document.querySelector("form");
const majorInput = document.getElementById("major-key-input") ;
const minorInput = document.getElementById("minor-key-input") ;
const answerResultDiv = document.getElementById("keysig-answer-result");

let currentMajorAnswer = "None";
let currentMinorAnswer = "None";

const loadNewSvg = () => {
    fetch("/key-signature-generate")
        .then(response => response.json())
        .then(keysigInfo => {

            currentMajorAnswer = keysigInfo.major_name;
            currentMinorAnswer = keysigInfo.minor_name;
            
            let container = document.createElement("div");
            container.innerHTML = keysigInfo.svg;

            svgSection.replaceChildren();
            svgSection.appendChild(container);

            majorInput.value = "";
            minorInput.value = "";

            majorInput.focus();
        });
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("Loaded!");
    loadNewSvg();
})

form.addEventListener("submit", (event) => {
    event.preventDefault();

    formData = new FormData(event.target);
    console.log(formData.get("major-key-name"));
    console.log(formData.get("minor-key-name"));

    const correct = formData.get("major-key-name") == currentMajorAnswer
                    && formData.get("minor-key-name") == currentMinorAnswer;
    answerResultDiv.innerHTML = correct ? "Correct!" : "Wrong!";
    answerResultDiv.innerHTML += ` The key was ${currentMajorAnswer} and ${currentMinorAnswer}.`;

    loadNewSvg();
})