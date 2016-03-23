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
    books = json.loads(content)["results"]["books"]

    book_names = {}
    for book in books:
        book_names[book["title"]] = book["amazon_product_url"]

    print "Book names:"

    for name, url in book_names.iteritems():
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "lxml")
        product = soup.find(id="productDetailsTable")
        tmp = ''
        if product:
            for line in product.get_text().split():
                if line.lower() == 'pages' and tmp.isdigit():
                    print tmp, 'pages - ', name.title()
                else:
                    tmp = line


if __name__ == "__main__":
    # execute only if run as a script
    main()
