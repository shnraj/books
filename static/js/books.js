var started = false;
var timeVar;
var totalSeconds = 0;
var fiction_books;
var nonfiction_books;

function setup() {
    var cookie_str = document.cookie;
    var wpm = cookie_str.substring(cookie_str.indexOf('=') + 1);
    update_book_times(wpm);
}

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
    var personal_wpm = wpm(343, totalSeconds)
    document.getElementById("wpm").innerHTML = 'Words per minute: ' + personal_wpm;
    document.cookie = "wpm=" + personal_wpm.toString();
    update_book_times(personal_wpm)
    totalSeconds = 0;
}

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

function wpm(words, time_in_sec) {
    var min = time_in_sec/60;
    var wpm = words/min;
    return Math.round(wpm * 100) / 100
}

function update_book_times(personal_wpm) {
    var lists = [fiction_books, nonfiction_books];
    for (var j=0; j < lists.length; j++) {
        for (var i=0; i < lists[j].length; i++) {
            className = "timeToRead" + lists[j][i].isbn;
            var total_min = lists[j][i].pages * 225 / personal_wpm;
            var hours = Math.floor((total_min)/60);
            var min =  Math.floor(total_min - (hours * 60));
            document.getElementById(className).innerHTML = hours + ' hr ' + min + ' min';
        }
    }
}
