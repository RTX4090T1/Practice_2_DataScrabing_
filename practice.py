from requests import get
from bs4 import BeautifulSoup

FILE_NAME = "booksGenre.txt.txt"
BASE_URL = "https://books.toscrape.com"
URL = "https://books.toscrape.com"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

with open(FILE_NAME, "w", encoding="utf-8") as file:
    page = get(URL, headers=HEADERS)    
    soup = BeautifulSoup(page.content,  "html.parser")
    genres = soup.find(class_="nav nav-list")
    for li in genres.find_all("li"):
        a = li.find("a")
        print(4)
        book_genre = a.find(text=True, recursive=False)
        genre_link = BASE_URL+ a.get("href")
        file.write(f"book genre: {book_genre}")
        file.write(f"URL: {genre_link}")
        print(f"book genre: {book_genre}")
        print(f"URL: {genre_link}")
