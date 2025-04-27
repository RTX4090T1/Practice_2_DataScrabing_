import csv
import json
from requests import get
from bs4 import BeautifulSoup
import time
import xml.etree.ElementTree as ET


class BSBS: 

    def __init__(self):
        self.baseUrl = "https://books.toscrape.com/"
        self.fileArray = ["booksData.txt", "BooksData.csv", "BooksData.json", "BooksData.xml"]
        self.userAgent = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        root = ET.Element("books")
        tree = ET.ElementTree(root)
        with open("BooksData.xml", "wb") as xml_file:
            tree.write(xml_file)

    def logDataIntoFile(self, category, url):
        data_entry = {"category": category, "url": url}

        with open("booksData.txt", "a", encoding="utf8") as txt_file:
            txt_file.write(f"{category},{url}\n")

        with open("BooksData.csv", "a", newline="", encoding="utf8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([category, url])

        try:
            with open("BooksData.json", "r", encoding="utf8") as json_file:
                json_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            json_data = []
        json_data.append(data_entry)
        with open("BooksData.json", "w", encoding="utf8") as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

        tree = ET.parse("BooksData.xml")
        root = tree.getroot()
        book_element = ET.SubElement(root, "book", category=category, url=url)
        tree.write("BooksData.xml")

    def getBooksBycategory(self, url):
        while url:
            response = get(url, headers=self.userAgent)
            objectOfSoup = BeautifulSoup(response.text, "html.parser")


            booksByCategory = objectOfSoup.select("ol.row")  
            if not booksByCategory:
                break

            itemCounterPerPage = 0
            for book in booksByCategory[0].find_all("li"):
                title = book.select_one("h3 a")["title"] 
                book_url = book.select_one("h3 a")["href"]
                self.logDataIntoFile(title, book_url)
                itemCounterPerPage += 1

            next_page = objectOfSoup.select_one("li.next a")  
            if next_page:
                next_page_url = next_page["href"]
                url = self.baseUrl + "catalogue/" + next_page_url
            else:
                break

    def getBooksCategory(self):
        tmSt = time.time()
        response = get(self.baseUrl, headers=self.userAgent)
        objectOfSoup = BeautifulSoup(response.text, "html.parser")


        bookCategories = objectOfSoup.select("ul.nav-list ul li a")
        for category in bookCategories:
            categoryUrl = self.baseUrl + category["href"]
            categoryName = category.get_text(strip=True)
            self.logDataIntoFile(categoryName, categoryUrl)
            print(categoryUrl)
            self.getBooksBycategory(categoryUrl)

        tmEnd = time.time()
        print("Time taken:", tmEnd - tmSt)


if __name__ == "__main__":
    scraper = BSBS()
    scraper.getBooksCategory()