var books;

function setup() {
    var cookie_str = document.cookie;
    var wpm = cookie_str.substring(cookie_str.indexOf('=') + 1);
    update_book_times(wpm);
}

function update_book_times(personal_wpm) {
    for (var i=0; i < books.length; i++) {
        className = "timeToRead" + books[i].isbn;
        var total_min = books[i].pages * 225 / personal_wpm;
        var hours = Math.floor((total_min)/60);
        var min =  Math.floor(total_min - (hours * 60));
        document.getElementById(className).innerHTML = hours + ' hr ' + min + ' min';
    }
}

function show_detailed_view(book_isbn) {
    var isbn_to_book_mapping = {}
    for (var i=0; i < books.length; i++) {
        isbn_to_book_mapping[books[i].isbn] = books[i]
    }
    document.getElementById('detailed_image').src = isbn_to_book_mapping[book_isbn].image;
    document.getElementById('detailed_name').innerHTML = isbn_to_book_mapping[book_isbn].name;
    document.getElementById('detailed_name').href = isbn_to_book_mapping[book_isbn].amazon_url;
    document.getElementById('detailed_pages').innerHTML = isbn_to_book_mapping[book_isbn].pages + " pages";
    document.getElementById('detailed_author').innerHTML = "By " + isbn_to_book_mapping[book_isbn].author;
    document.getElementById('detailed_summary').innerHTML = isbn_to_book_mapping[book_isbn].summary;
}

