import re
import requests
import json

from bs4 import BeautifulSoup


GOODREADS_KEY = "a2812dc7a11a8746e78e803c2baccb46:5:74720908"
ISBNDB_KEY = "VMBECAZ6"


def main():
    # print "List names:"
    # print '\n'.join(get_list_names())
    get_books()


def get_list_names():
    request_url = "http://api.nytimes.com/svc/books/v3/lists/names.json?api-key=" + GOODREADS_KEY

    content = requests.get(request_url)._content
    results = json.loads(content)["results"]

    list_names = {}
    for result in results:
        list_names[result["display_name"]] = result["list_name_encoded"]

    return list_names


def get_books():
    request_url = "http://api.nytimes.com/svc/books/v3/lists/combined-print-fiction.json?api-key=" + GOODREADS_KEY

    content = requests.get(request_url)._content
    books_results = json.loads(content)["results"]["books"]

    books = [Book(
             book["title"],
             book["author"],
             book["primary_isbn13"],
             book["amazon_product_url"])
             for book in books_results]

    for book in books:
        get_pages(book)

    print "Books:"
    for book in books:
        if book.pages:
            print book.pages, ' - ', book.name, book.author


def get_pages(book):
    request_url = "http://isbndb.com/api/v2/json/" + ISBNDB_KEY + "/book/" + book.isbn

    content = json.loads(requests.get(request_url)._content)
    if "data" in content:
        pages_result = content["data"][0]["physical_description_text"]
        wordList = re.sub('[^\w]', ' ',  pages_result).split()
        tmp = ''
        for word in wordList:
            if word == "pages" or word == "p.":
                book.pages = int(tmp)
            tmp = word


def get_amazon_pages(books):
    for book in books:
        r = requests.get(book.amazon_url)

        soup = BeautifulSoup(r.text, "lxml")
        product = soup.find(id="productDetailsTable")
        tmp = ''
        if product:
            for line in product.get_text().split():
                if line.lower() == 'pages' and tmp.isdigit():
                    book.pages = tmp
                else:
                    tmp = line


class Book():

    def __init__(self, name, author, isbn, amazon_url, pages=None, summary=None):
        self.name = name
        self.author = author
        self.isbn = isbn
        self.amazon_url = amazon_url
        self.pages = pages
        self.summary = summary


if __name__ == "__main__":
    # execute only if run as a script
    main()
