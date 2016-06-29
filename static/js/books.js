var started = false;
var timeVar;
var totalSeconds = 0;

function start() {
    if (!started) {
        var textBlock = document.getElementById('textBlock');
        textBlock.className = "";
        started = true;
        timeVar = setInterval(countTimer, 1000);
        function countTimer() {
            ++totalSeconds;
            var hour = Math.floor(totalSeconds /3600);
            var minute = Math.floor((totalSeconds - hour*3600)/60);
            var seconds = totalSeconds - (hour*3600 + minute*60);

            document.getElementById("timer").innerHTML = pad(minute) + ":" + pad(seconds);
        };
    }
}

function stop() {
    started = false;
    clearInterval(timeVar);
    document.getElementById("wpm").innerHTML = 'Words per minute: ' + wpm(343, totalSeconds);
    totalSeconds = 0;
}

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

function wpm(words, time_in_sec) {
    var wps = words/time_in_sec;
    var wpm = wps/60
    return Math.round(wpm * 100) / 100
}
