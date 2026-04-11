const answerResultDiv = document.getElementById("scale-answer-result");
const userInputField = document.getElementById("user-input");
const submitButton = document.getElementById("scale-submit");
const svgSection = document.getElementById("scale-svg-section");
const form = document.querySelector("form");

let currentScaleName = "None";

/* This function calls the backend to get a new scale
which is a JSON response that has a name and an svg element
as a string.

The function has 2 side effects:
1. currentScaleName is changed.
2. The svg is rendered on the page.
WITH the side effect of loading the svg onto the webpage.

*/
const loadNewScaleSvg = () => {
    // Generate a new scale.
    fetch("/scale-generate")
        .then(result => result.json())
        .then(scaleInfoJson => {
            currentScaleName = scaleInfoJson.name;
            console.log(`Answer ${currentScaleName}`);

            // Create a new element with the SVG inside
            const div = document.createElement("div");
            div.innerHTML = scaleInfoJson.svg;
            svgSection.replaceChildren();
            svgSection.appendChild(div);
        });
}

/* When the webpage is loaded, this function calls the
load scale svg method.
*/
document.addEventListener("DOMContentLoaded", () => {
    loadNewScaleSvg();
})


/* When the user submits the form, this function handles
the submission with two steps.
1. checks user evaluation.
2. calls the load new svg function 
*/
form.addEventListener("submit", (event) => {
    event.preventDefault();

    // Retrieve the scale name guess and evaluate it
    const formData = new FormData(event.target);
    const scaleNameGuess = formData.get("user-input");

    // Generate a new thing.
    if (currentScaleName != "None") {
        console.log(`input field: ${scaleNameGuess}`);
        const correct = scaleNameGuess == currentScaleName;
        console.log(`${scaleNameGuess} ${currentScaleName} ${correct}`),

        answerResultDiv.innerHTML = correct ? "Correct!" : "Wrong!";
        answerResultDiv.innerHTML += ` that was a ${currentScaleName}.`;
    }

    userInputField.value = "";
    loadNewScaleSvg();
});
