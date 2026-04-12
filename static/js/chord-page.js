const form = document.querySelector("form");
const svgSection = document.getElementById("chord-svg-section");

const loadNewSvg = () => {
    fetch("/chord-generate")
        .then(response => response.json())
        .then(chordInfo => {
            const container = document.createElement("div");
            container.innerHTML = chordInfo.svg;

            svgSection.replaceChildren();
            svgSection.append(container);

        })
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    console.log("submit");

    loadNewSvg();
})