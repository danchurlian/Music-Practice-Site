console.log("Running");
const submitButton = document.getElementById("scale-submit");
const svgSection = document.getElementById("scale-svg-section");
submitButton.addEventListener('mouseup', (event) => {
    event.preventDefault();
    fetch("/scale-generate")
        .then(result => result.text())
        .then(htmlString => {
            // Create a new element with the SVG inside
            const div = document.createElement("div");
            div.innerHTML = htmlString;
            svgSection.replaceChildren();
            svgSection.appendChild(div);
        });
});
