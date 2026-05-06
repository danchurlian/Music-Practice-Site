import {playAudio} from "./audio-handler.js"

const LISTEN_COOLDOWN_MS = 1500;
let playingSound = false;
const noteNum1 = Number("{{ note_1 }}");
const noteNum2 = Number("{{ note_2 }}");

const button = document.getElementById("interval-button");
button.addEventListener("mouseup", event => {
    if (!playingSound) {
        playingSound = true;
        console.log(`Playing ${noteNum1} and ${noteNum2}`);
        playAudio(noteNum1);
        playAudio(noteNum2);

        // Disable debounce after waiting for 1.5 seconds
        setTimeout(() => {playingSound = false}, LISTEN_COOLDOWN_MS);
    }
});