from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import re
from urllib.parse import urlparse

class CrawlerClass:
    def __init__(self):
        self.unique_urls = set()  # Set to store unique URLs
        self.scraped_file = "scraped_urls.txt"  # File to store scraped URLs
        self.longest_word_count = 0
        self.subdomain_counts = defaultdict(int)

        with open(self.scraped_file, "w") as f:
            f.write("")

        self.word_counts = Counter()
        self.stop_words = {
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
            "you", "your", "yours", "yourself", "yourselves", "he", "him",
            "his", "himself", "she", "her", "hers", "herself", "it", "its",
            "itself", "they", "them", "their", "theirs", "themselves", 
            "what", "which", "who", "whom", "this", "that", "these", "those", 
            "am", "is", "are", "was", "were", "be", "been", "being", "have", 
            "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
            "the", "and", "but", "if", "or", "because", "as", "until", 
            "while", "of", "at", "by", "for", "with", "about", "against", 
            "between", "into", "through", "during", "before", "after", 
            "above", "below", "to", "from", "up", "down", "in", "out", 
            "on", "off", "over", "under", "again", "further", "then", 
            "once", "here", "there", "when", "where", "why", "how", 
            "all", "any", "both", "each", "few", "more", "most", "other", 
            "some", "such", "no", "nor", "not", "only", "own", "same", 
            "so", "than", "too", "very", "s", "t", "can", "will", "just", 
            "don", "should", "now"
        }


    def add_url(self, url):
        # Add it to set
        if url not in self.unique_urls:
            self.unique_urls.add(url)  

            # Add it to file
            with open(self.scraped_file, "a") as f:
                f.write(url + "\n")

            # Extract the subdomain and update its count
            parsed_url = urlparse(url)
            if parsed_url.hostname and parsed_url.hostname.endswith("uci.edu"):
                subdomain = parsed_url.hostname
                self.subdomain_counts[subdomain] += 1

    def update_words(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()  
        words = text.split()
        self.longest_word_count = max(self.longest_word_count, len(words))

        p3_words = re.findall(r'\w+', text.lower())
        filtered_words = [word for word in p3_words if word not in self.stop_words] 
        self.word_counts.update(filtered_words)

    def get_most_common_words(self, n):
        return self.word_counts.most_common(n)
    
    def get_subdomain_list(self):
        # Sort and format subdomains with their counts
        return sorted(
            [(subdomain, count) for subdomain, count in self.subdomain_counts.items()],
            key=lambda x: x[0]
        )
    
    def print_report(self):
        with open(self.report_file, "w") as report:
            # Write the total unique URLs
            report.write(f"Unique Pages: {len(self.unique_urls)}\n\n")
            
            # Write the longest page information
            report.write(f"Longest Page: {self.longest_page_url} with {self.longest_word_count} words\n\n")
            
            # Write the 50 most common words
            report.write("50 Most Common Words:\n")
            for word, count in self.get_most_common_words(50):
                report.write(f"{word}: {count}\n")
            report.write("\n")
            
            # Write subdomains and counts
            report.write("Subdomains and Unique Page Counts:\n")
            for subdomain, count in self.get_subdomain_list():
                report.write(f"{subdomain}, {count}\n")