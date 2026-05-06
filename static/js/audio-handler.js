const AUDIO_BASE_URL = "./" // Root directory
// Play plays the appropriate note mp3 file given the noteNumber. 
const playAudio = (noteNumber) => {
    // Fetch for the mp3 audio file from the backend
    const fileName = `note${noteNumber}.mp3`;
    const url = AUDIO_BASE_URL + fileName;
    console.log(url);
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            // Create an audio instance and play it
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.controls = false;
            document.body.appendChild(audio);
            audio.play();

            // Destroy the audio element when it is finished playing
            audio.addEventListener("ended", event => {
                event.target.remove();
            });
        })
        .catch(() => { console.log("Something happened."); });
};

export {playAudio} 