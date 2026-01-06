from dataclasses import dataclass
from typing import List, Iterator, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"

@dataclass
class Book:
    title: str
    price: float
    availability: str
    rating: int
    url: str

def _parse_rating(element) -> int:
    """
    p.star-rating contains classes like ['star-rating', 'Three]
    This function maps the words to numbers
    """
    classes = element.get("class", [])
    word_to_num = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for c in classes:
        if c in word_to_num:
            return word_to_num[c]
    return 0


def scrape_page(url: str) -> List[Book]:
    """
    Put all articles into a list, iterates over it and scrap informations for every book.
    """
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    books: List[Book] = []

    for article in soup.select("article.product_pod"):
        a_tag = article.select_one("h3 a")
        title = a_tag["title"]
        rel_url = a_tag["href"]
        book_url = urljoin(url, rel_url)

        price_text = article.select_one(".price_color").get_text(strip=True)
        price_str = price_text.lstrip("Â£")
        price = float(price_str)

        availability = article.select_one(".availability").get_text(strip=True)

        rating_el = article.select_one("p.star-rating")
        rating = _parse_rating(rating_el) if rating_el else 0

        books.append(
            Book(
                title=title,
                price=price,
                availability=availability,
                rating=rating,
                url=book_url
            )
        )
    
    return books


def get_next_page_url(current_url: str, soup: BeautifulSoup) -> Optional[str]:
    """
    Returns the url for the next page.
    """
    next_link = soup.select_one("li.next a")
    if not next_link:
        return None
    rel_href = next_link.get("href")
    return urljoin(current_url, rel_href)

def crawl_all_pages(start_url: str = BASE_URL) -> Iterator[Book]:
    """
    Get all books from one page and yield every book.
    After all books got yielded start with next page.
    """
    current_url = start_url
    pages_crawled = 0

    while current_url:
        resp = requests.get(current_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for book in scrape_page(current_url):
            yield book
        
        pages_crawled += 1
        current_url = get_next_page_url(current_url, soup)
