from requests import get
from bs4 import BeautifulSoup
import time

class BSBS:  # Beautiful Soup Book Scraper
    
    def __init__(self):
        self.baseUrl = "https://books.toscrape.com/"
        self.datafile = "booksData.txt"
        self.userAgent = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
         
    def logDataIntoFile(self, category, url):
        with open(self.datafile, "a", encoding="utf8") as writeData:
            writeData.write(f"{category},{url}\n")     

    def getBooksBycategory(self, url):
        while url:
            response = get(url, headers=self.userAgent)
            objectOfSoup = BeautifulSoup(response.text, "html.parser")
            booksByCategory = objectOfSoup.find("ol", class_="row")
            if not booksByCategory:
                break
            itemCounterPerPage = 0
            for book in booksByCategory.find_all("li"):
                self.logDataIntoFile(book.find("h3").find("a").find(text=True, recursive=False), book.find("a").get("href"))
                itemCounterPerPage += 1

            next_page = objectOfSoup.find("li", class_="next")
            if next_page:
                next_page_url = next_page.find("a").get("href")
                url = self.baseUrl + "catalogue/" + next_page_url
            else:
                break

    def getBooksCategory(self):
        tmSt = time.time()
        response = get(self.baseUrl, headers=self.userAgent)
        objectOfSoup = BeautifulSoup(response.text, "html.parser")
        bookCategories = objectOfSoup.find("ul", class_="nav nav-list").find("ul")
        for category in bookCategories.find_all("li"):
            categoryUrl = self.baseUrl + category.find("a").get("href")
            self.logDataIntoFile(category.find("a").find(text=True, recursive=False), categoryUrl)
            print(categoryUrl)
            self.getBooksBycategory(categoryUrl)

        tmEnd = time.time()
        print(tmEnd - tmSt)
