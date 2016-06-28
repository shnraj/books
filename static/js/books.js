var started = false;
var timeVar;

function start() {
    if (!started) {
        var textBlock = document.getElementById('textBlock');
        textBlock.className = "";
        started = true;
        timeVar = setInterval(countTimer, 1000);
        var totalSeconds = 0;
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
}

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}
