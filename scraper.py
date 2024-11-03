import re
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from crawler_class import CrawlerClass  

crawler = CrawlerClass()

lower_bound = 700

def scraper(url, resp):
    links = extract_next_links(url, resp)
    valid_links = []
    for link in links:
        if link not in crawler.unique_urls:
            crawler.add_url(link)
            valid_links.append(link)

    return valid_links

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    links = set()

    # Check if the response is valid (e.g., status 200) and contains content
    if resp.status != 200 or not resp.raw_response:
        return []  # Return empty list if the response isn't valid
    
    content_type = resp.raw_response.headers.get('Content-Type', '')
    if 'text/html' not in content_type:
        return []

    # Parse the HTML content
    try:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
    except Exception:
        print(f"Error parsing HTML for {url}: {Exception}")
        return []

    text = soup.get_text()
    delimited_text = re.sub('\s+', ' ', text)

    if len(delimited_text) < lower_bound:
        return []

    # Find all <a> tags to get the hyperlinks
    for tag in soup.find_all("a", href=True):
        href = tag.get("href")
        
        # Resolve relative URLs
        absolute_url = urljoin(url, href)
        
        # Remove URL fragment (anything after #)
        defragmented_url = urldefrag(absolute_url).url
        
        if is_valid(defragmented_url):
            links.add(defragmented_url)
            crawler.update_words(resp.raw_response.content)

    return list(links)


def is_valid(url):
    try:
        parsed = urlparse(url)
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

        # Returns false if there is a query in the URL
        if parsed.query:
            return False

        if re.search(r"/\d{4}-\d{2}-\d{2}|/\d{4}/\d{2}/\d{2}|/\d{4}-\d{2}/|/\d{4}/\d{2}/", parsed.path):
            return False

        if parsed.query and re.search(r"(date|time|year|month|day)=\d{4}-\d{2}-\d{2}", parsed.query):
            return False
        
        if "?share=" in url or "pdf" in url or "redirect" in url or "#comment" in url or "#respond" in url or "#comments" in url:
            return False

        return True

    except Exception as e:
        print(f"Error validating URL {url}: {e}")
        return False
