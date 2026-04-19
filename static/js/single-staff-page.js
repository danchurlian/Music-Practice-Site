const mainSection = document.querySelector(".main-content");
const PAGE_ID = mainSection.id;

const answerResultDiv = document.getElementById("scale-answer-result");

// Change this later
const userInputField = document.getElementById("scale-user-answer");
const submitButton = document.getElementById("scale-submit");
const svgSection = document.getElementById("scale-svg-section");
const form = document.querySelector("form");

const answers = {
    "scale-page": {
        "scale-user-answer": "None",
    }
};

const SVG_LINKS = {
    "scale-page": "/scale-generate",
};

const loadNewScaleSvg = () => {
    // Generate a new scale.
    fetch(SVG_LINKS["scale-page"])
        .then(result => result.json())
        .then(scaleInfoJson => {
            answers[PAGE_ID]["scale-user-answer"] = scaleInfoJson.scale_name;
            console.log(`Answer ${answers[PAGE_ID]}`);

            // Create a new element with the SVG inside
            const div = document.createElement("div");
            div.innerHTML = scaleInfoJson.svg;
            svgSection.replaceChildren();
            svgSection.appendChild(div);
        });
}

const loadPageSvg = (aPageId, aSvgSection) => {
    // Generate a new scale.
    fetch(SVG_LINKS[aPageId])
        .then(result => result.json())
        .then(infoJson => {
            // Change this later
            answers[aPageId]["scale-user-answer"] = infoJson.scale_name;
            console.log(`Answer object ${answers[aPageId]}`);

            // Create a new element with the SVG inside
            const div = document.createElement("div");
            div.innerHTML = infoJson.svg;
            aSvgSection.replaceChildren();
            aSvgSection.appendChild(div);
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
    const currentAnswers = answers[PAGE_ID]; 
    console.log(PAGE_ID + " " +currentAnswers);

    // Get the list of key-value pairs of the user's inputs
    // Compare them one by one to the current state of the web page
    let correct = true;

    for (const key of formData.keys()) {
        console.log(`Entry ${key} ${formData.get(key)} ${currentAnswers[key]}`);
        if (formData.get(key) != currentAnswers[key]) {
            console.log("Mismatch!");
            correct = false;
        }
    }

    answerResultDiv.innerHTML = correct ? "Correct!" : "Wrong!";
    answerResultDiv.innerHTML += ` that was a following...`;

    userInputField.value = "";

    loadNewScaleSvg();
})