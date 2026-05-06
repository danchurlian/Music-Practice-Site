const AUDIO_BASE_URL = "/static/" // Root directory

// Play plays the appropriate note mp3 file given the noteNumber. 
async function playAudioAsync(noteNumber) {
    // Fetch for the mp3 audio file from the backend
    const fileName = `note${noteNumber}.mp3`;
    const url = AUDIO_BASE_URL + fileName;

    const blob = await fetch(url).then(result => result.blob());

    // Create an audio instance and play it
    const audioObjURL = URL.createObjectURL(blob);
    const audio = new Audio(audioObjURL);
    audio.controls = false;

    document.body.appendChild(audio);
    audio.play();

    // Destroy the audio element when it is finished playing
    audio.addEventListener("ended", event => {
        event.target.remove();
    });
};

export {playAudioAsync} 