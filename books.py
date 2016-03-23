import requests
import json

from bs4 import BeautifulSoup


KEY = "a2812dc7a11a8746e78e803c2baccb46:5:74720908"


def main():
    # print "List names:"
    # print '\n'.join(get_list_names())
    get_books()


def get_list_names():
    request_url = "http://api.nytimes.com/svc/books/v3/lists/names.json?api-key=" + KEY

    content = requests.get(request_url)._content
    results = json.loads(content)["results"]

    list_names = {}
    for result in results:
        list_names[result["display_name"]] = result["list_name_encoded"]

    return list_names


def get_books():
    request_url = "http://api.nytimes.com/svc/books/v3/lists/combined-print-fiction.json?api-key=" + KEY

    content = requests.get(request_url)._content
    books_results = json.loads(content)["results"]["books"]

    books = [Book(book["title"], book["author"], book["amazon_product_url"])
             for book in books_results]

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

    print "Books:"
    for book in books:
        if book.pages:
            print book.pages, ' - ', book.name, book.author


class Book():

    def __init__(self, name, author, amazon_url, pages=None):
        self.name = name
        self.author = author
        self.amazon_url = amazon_url
        self.pages = pages


if __name__ == "__main__":
    # execute only if run as a script
    main()
