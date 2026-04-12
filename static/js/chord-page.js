const form = document.querySelector("form");
const svgSection = document.getElementById("chord-svg-section");
const chordInputField = document.getElementById("chord-input");

const loadNewSvg = () => {
    fetch("/chord-generate")
        .then(response => response.json())
        .then(chordInfo => {
            const container = document.createElement("div");
            container.innerHTML = chordInfo.svg;

            svgSection.replaceChildren();
            svgSection.append(container);
            
            chordInputField.value = "";
            chordInputField.focus();
        })
}

form.addEventListener("submit", (event) => {
    event.preventDefault();

    loadNewSvg();
})