import config  # file that contains my API tokens
import json
import re
import requests
import shelve  # simple persistent storage option

from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def main():
    books = get_books()
    # list_name = 'hardcover-fiction'
    # books = [book.__dict__ for book in get_all_books_from_shelve(list_name)]
    return render_template('books.html', books=books)
    # return get_list_names()


def get_list_names():
    request_url = "http://api.nytimes.com/svc/books/v3/lists/names.json?api-key=" + config.NYT_KEY

    content = requests.get(request_url)._content
    results = json.loads(content)["results"]

    list_names = {}
    for result in results:
        list_names[result["display_name"]] = result["list_name_encoded"]

    return list_names


# get new york times bestseller list of books
def get_books():
    list_name = 'hardcover-fiction'
    request_url = "http://api.nytimes.com/svc/books/v3/lists/" + list_name + ".json?api-key=" + config.NYT_KEY

    content = requests.get(request_url)._content
    books_results = json.loads(content)["results"]["books"]

    books = [Book(
             book["title"],
             book["author"],
             book["primary_isbn13"],
             book["amazon_product_url"],
             book["book_image"],
             book["description"])
             for book in books_results
             if not book_in_shelve(book["primary_isbn13"], list_name)]

    for book in books:
        book.pages = get_page_count(book)
        if book.pages:
            add_book_to_shelve(book, list_name)

    return [book.__dict__ for book in get_all_books_from_shelve(list_name)]


# get book page number from isbndb
def get_page_count(book):
    page_count = get_ibdndb_pages(book)
    if not page_count:
        page_count = get_amazon_pages(book)
    return page_count


# get page number from isbndb
def get_ibdndb_pages(book):
    request_url = "http://isbndb.com/api/v2/json/" + config.ISBNDB_KEY + "/book/" + book.isbn

    content = json.loads(requests.get(request_url)._content)
    if "data" in content:
        pages_result = content["data"][0]["physical_description_text"]
        wordList = re.sub('[^\w]', ' ',  pages_result).split()
        tmp = ''
        for word in wordList:
            if word == "pages" or word == "p" and tmp.isdigit():
                return int(tmp)
            tmp = word


# scrape amazon to get book page number
def get_amazon_pages(book):
    r = requests.get(book.amazon_url)

    soup = BeautifulSoup(r.text, "lxml")
    product = soup.find(id="productDetailsTable")
    tmp = ''
    if product:
        for line in product.get_text().split():
            if line.lower() == 'pages' and tmp.isdigit():
                book.pages = int(tmp)
                return int(tmp)
            else:
                tmp = line


class Book():

    def __init__(self, name, author, isbn, amazon_url, image, summary=None, pages=0):
        self.name = name
        self.author = author
        self.isbn = isbn
        self.amazon_url = amazon_url
        self.pages = pages
        self.image = image
        self.summary = summary

    def __lt__(self, other):
        return self.pages < other.pages


# if book does not exist in shelve and has a page number, add to shelve
def add_book_to_shelve(book, db_name):
    s = shelve.open(db_name)
    try:
        if book.pages and book.isbn not in s:
            s[book.isbn] = book
    finally:
        s.close()


# get book from shelve given isbn number
def get_book_from_shelve(isbn, db_name):
    s = shelve.open(db_name)
    try:
        if isbn in s:
            book = s[isbn]
    finally:
        s.close()
    return book


# get all books from shelve - returns book objects
def get_all_books_from_shelve(db_name):
    s = shelve.open(db_name)
    try:
        books = s.values()
        books.sort()
    finally:
        s.close()
    return books


# return string form of all books in shelve
def all_books_str(db_name):
    books_in_shelve = get_all_books_from_shelve(db_name)
    books_string = ''
    for book in books_in_shelve:
        if book.pages:
            books_string += '<img src="' + book.image +'" width="170"/>' + '  ' + str(book.pages) + ' - ' + book.name + ' - ' + book.author + ' - ' + book.summary + '<br/>'
    return books_string


# return if book exists in shelve given isbn number
def book_in_shelve(isbn, db_name):
    s = shelve.open(db_name)
    try:
        book_in_shelve = isbn in s
    finally:
        s.close()
    return book_in_shelve


if __name__ == "__main__":
    app.run()
