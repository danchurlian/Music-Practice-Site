console.log("Running");
const submitButton = document.getElementById("scale-submit");
const svgSection = document.getElementById("scale-svg-section");
let currentScaleName = "None";

submitButton.addEventListener('mouseup', (event) => {
    event.preventDefault();
    fetch("/scale-generate")
        .then(result => result.json())
        .then(scaleInfoJson => {
            currentScaleName = scaleInfoJson.name;
            console.log(`Answer ${currentScaleName}`)
            
            // Create a new element with the SVG inside
            const div = document.createElement("div");
            div.innerHTML = scaleInfoJson.svg;
            svgSection.replaceChildren();
            svgSection.appendChild(div);
        });
});
