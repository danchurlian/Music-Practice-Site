export function listenButtonPlayOn(button) {
    button.classList.remove("listen-button");
    button.classList.add("listen-button-nohover");
    button.classList.add("listen-button--playing");
}

export function listenButtonPlayOff(button) {
    button.classList.remove("listen-button--playing");
    button.classList.remove("listen-button-nohover");
    button.classList.add("listen-button");
}