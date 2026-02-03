function vibrate(ms){
    if (navigator.vibrate) navigator.vibrate(ms);
}

function generate(){
    const text = document.getElementById("text").value.trim();
    const voice = document.getElementById("voice").value;

    if(!text){
        alert("Enter some text");
        return;
    }

    vibrate(60);

    document.getElementById("loader").style.display = "block";
    document.getElementById("result").style.display = "none";

    let progress = 0;
    const bar = document.getElementById("progress");

    const fake = setInterval(() => {
        progress += 7;
        bar.style.width = progress + "%";
        if(progress >= 90) clearInterval(fake);
    }, 100);

    fetch("/api/tts", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({text, voice})
    })
    .then(r => r.json())
    .then(d => {
        clearInterval(fake);
        bar.style.width = "100%";

        setTimeout(() => {
            document.getElementById("loader").style.display = "none";
        }, 300);

        if(d.success){
            const src = "data:audio/mpeg;base64," + d.audio;
            document.getElementById("player").src = src;
            document.getElementById("download").href = src;
            document.getElementById("result").style.display = "block";
            vibrate([40,30,40]);
        } else {
            alert("Voice generation failed");
        }
    });
}
