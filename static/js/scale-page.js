const answerResultDiv = document.getElementById("scale-answer-result");
const userInputField = document.getElementById("user-input");
const submitButton = document.getElementById("scale-submit");
const svgSection = document.getElementById("scale-svg-section");
const form = document.querySelector("form");
let currentScaleName = "None";

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

    // Generate a new scale.
    fetch("/scale-generate")
        .then(result => result.json())
        .then(scaleInfoJson => {
            currentScaleName = scaleInfoJson.name;
            console.log(`Answer ${currentScaleName}`)

            answerResultDiv.innerHTML
            
            // Create a new element with the SVG inside
            const div = document.createElement("div");
            div.innerHTML = scaleInfoJson.svg;
            svgSection.replaceChildren();
            svgSection.appendChild(div);
        });
});
