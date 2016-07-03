var started = false;
var timeVar;
var totalSeconds = 0;
var fiction_books;
var nonfiction_books;

function setup(fiction_books, nonfiction_books) {
    fiction_books = fiction_books;
    nonfiction_books = nonfiction_books;
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
    fiction_books = [{'isbn': '9780804141260', 'name': 'VINEGAR GIRL', 'author': 'Anne Tyler', 'image': 'https://s1.nyt.com/du/books/images/9780804141260.jpg', 'amazon_url': 'http://www.amazon.com/Vinegar-Girl-Novel-Hogarth-Shakespeare/dp/0804141266?tag=thenewyorktim-20', 'pages': 240}, {'isbn': '9780812996494', 'name': 'A HERO OF FRANCE', 'author': 'Alan Furst', 'image': 'https://s1.nyt.com/du/books/images/9780812996500.jpg', 'amazon_url': 'http://www.amazon.com/Hero-France-Novel-Alan-Furst-ebook/dp/B018CHH2A8?tag=thenewyorktim-20', 'pages': 256}]
    started = false;
    clearInterval(timeVar);
    document.getElementById("wpm").innerHTML = 'Words per minute: ' + wpm(343, totalSeconds);
    for (var i=0; i < fiction_books.length; i++) {
        className = "timeToRead" + fiction_books[i].isbn
        document.getElementById(className).innerHTML = fiction_books[i].pages * 225 * wpm(343, totalSeconds);
    }
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
