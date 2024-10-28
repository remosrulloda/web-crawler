import re
from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup

from crawler_class import CrawlerClass
from utils.response import Response


crawler = CrawlerClass()


def scraper(url: str, resp: Response) -> list[str]:
    # Return a list of valid hyperlinks (as strings) scrapped from resp.raw_response.content
    # Add all links to crawler.unique_urls

    links = extract_next_links(url, resp)
    unique_links = []
    
    for link in links:
        if link not in crawler.unique_urls:
            crawler.add_url(link)
            unique_links.append(link)

    return unique_links


def extract_next_links(url: str, resp: Response) -> list[str]:
    # Return a list of valid hyperlinks (as strings) scrapped from resp.raw_response.content
    # Updates crawler.word_counts and crawler.longest_word_count with respective data from page
    # 
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #     resp.raw_response.url: the url, again
    #     resp.raw_response.content: the content of the page!

    links = set()

    # Check if the response is valid (e.g., status 200) and contains content
    if resp.status != 200 or not resp.raw_response:
        return []  # Return empty list if the response isn't valid

    # Parse the HTML content
    soup = BeautifulSoup(resp.raw_response.content, "html.parser")

    # Find all <a> tags to get the hyperlinks
    for tag in soup.find_all("a", href = True):
        href = tag.get("href")

        # Resolve relative URLs
        absolute_url = urljoin(url, href)

        # Remove URL fragment (anything after #)
        defragmented_url = urldefrag(absolute_url).url

        # Add valid links to set and update word counts
        if is_valid(defragmented_url):
            links.add(defragmented_url)
            crawler.update_words(resp.raw_response.content)

    return list[links]


def is_valid(url: str) -> bool:
    # Return whether URL is valid based on protocol, format, and domain

    try:
        parsed = urlparse(url)
        
        # Include only URLs using HTTP(S) protocol
        if parsed.scheme not in {"http", "https"}:
            return False

        # Exclude certain file types based on extension
        if re.search(
            r"\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
            r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1"
            r"|thmx|mso|arff|rtf|jar|csv|rm|smil|wmv|swf|wma|zip|rar|gz)$", 
            parsed.path.lower()
        ):
            return False

        valid_domains = [
            'ics.uci.edu',
            'cs.uci.edu',
            'informatics.uci.edu',
            'stat.uci.edu',
            'today.uci.edu'
        ]

        # Check if netloc ends with any of the valid domains
        if not any(parsed.netloc.endswith(domain) for domain in valid_domains):
            return False

        # Special path restriction for today.uci.edu
        if "today.uci.edu" in parsed.netloc and not parsed.path.startswith("/department/information_computer_sciences"):
            return False

        return True

    except TypeError:
        print("TypeError for", url)
        raise
