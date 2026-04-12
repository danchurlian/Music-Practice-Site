const svgSection = document.getElementById("keysig-svg-section");
const form = document.querySelector("form");
console.log(form);

form.addEventListener("submit", (event) => {
    event.preventDefault();

    formData = new FormData(event.target)
    console.log(formData.get("major-key-name"));
    console.log(formData.get("minor-key-name"));
})