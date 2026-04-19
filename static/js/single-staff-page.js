const mainSection = document.querySelector(".main-content");
const PAGE_ID = mainSection.id;

const answerResultDiv = document.getElementById("scale-answer-result");

// Change this later
const userInputField = document.getElementById("scale-answer");
const submitButton = document.getElementById("scale-submit");
const svgSection = document.querySelector(".music-svg-section");
const form = document.querySelector("form");

const answers = {
    "scale-page": {
        "scale-answer": "None",
    },

    "keysig-page": {
        "major-key-answer": "None",
        "minor-key-answer": "None",
    },
};

const SVG_LINKS = {
    "scale-page": "/scale-generate",
    "keysig-page": "/key-signature-generate",
};


const loadPageSvg = (aPageId, aSvgSection) => {
    // Generate a new scale.
    const fetchLink = SVG_LINKS[aPageId];
    console.assert(fetchLink, "Fetching link is not defined for this page");
    console.assert(aSvgSection !== null, "svg is not given!");
    fetch(SVG_LINKS[aPageId])
    .then(result => result.json())
    .then(infoJson => {
        /* Change the global state */
        for (key of Object.keys(answers[PAGE_ID])) {
            answers[PAGE_ID][key] = infoJson[key];
            console.log(`Set global answer ${key} to 
                ${infoJson[key]}`);
        }
        console.log(`Global answers set to 
            ${JSON.stringify(answers[PAGE_ID])}`);

        // Create a new element with the SVG inside
        const div = document.createElement("div");
        div.innerHTML = infoJson.svg;
        aSvgSection.replaceChildren();
        aSvgSection.appendChild(div);
    })
    .catch(error => {
        console.error(`Error rendering music SVG: ${error}`);
    });
}

const loadNewScaleSvg = () => {
    loadPageSvg(PAGE_ID, svgSection);
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