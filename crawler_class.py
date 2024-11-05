from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import re
from urllib.parse import urlparse

class CrawlerClass:
    def __init__(self):
        # Set to store unique URLs
        self.unique_urls = set()

        # Define file paths for storing outputs
        self.scraped_file = "scraped_urls.txt"  
        self.longest_word_count_file = "longest_word_count.txt"
        self.word_counts_file = "word_counts.txt"
        self.report_file = "report.txt"
        self.subdomain_counts_file = "subdomain_counts.txt"
        
        self.longest_word_count = 0
        self.subdomain_counts = defaultdict(int)

        # Clear scraped_file
        with open(self.scraped_file, "w") as f:
            f.write("")

        # Set counter to track frequency of word across pages
        self.word_counts = Counter()
        
        # Define common stop words to exclude from word count
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
        # Check if URL is not stored in unique_urls set
        if url not in self.unique_urls:
            # Add URL to unique_urls set
            self.unique_urls.add(url)  

            # Write new URL to scraped_file
            with open(self.scraped_file, "a") as f:
                f.write(url + "\n")

            # Extract the subdomain
            parsed_url = urlparse(url)
            # Check if URL contains hostname and hostname ends with "uci.edu"
            if parsed_url.hostname and parsed_url.hostname.endswith("uci.edu"):
                # Increment subdomain_counts
                subdomain = parsed_url.hostname
                self.subdomain_counts[subdomain] += 1
                
                # Write updated subdomain_counts to subdomain_counts_file
                with open(self.subdomain_counts_file, "w") as f:
                    for subdomain, count in sorted(self.subdomain_counts.items()):
                        f.write(f"{subdomain}, {count}\n")

    def update_words(self, html_content):
        # Parse HTML content
        soup = BeautifulSoup(html_content, "html.parser")
        # Extract text from HTML
        text = soup.get_text()
        words = text.split()

        # Update longest_word_count if current page has more words
        self.longest_word_count = max(self.longest_word_count, len(words))

        # Write current longest_word_count to longest_word_count_file
        with open(self.longest_word_count_file, "w") as f:
                f.write(str(self.longest_word_count))

        # Tokenize text
        p3_words = re.findall(r'\w+', text.lower())
        # Filter out stop words in tokenized text
        filtered_words = [word for word in p3_words if word not in self.stop_words and len(word) > 1]
        # Update word_counts with filtered_words
        self.word_counts.update(filtered_words)
        
        # Write updated word_counts to word_counts_file
        with open(self.word_counts_file, "w") as f:
            for word, count in self.word_counts.most_common():
                f.write(f"{word}: {count}\n")

    def get_most_common_words(self, n):
        # Return the n most common words in word_counts
        return self.word_counts.most_common(n)
    
    def get_subdomain_list(self):
        # Sort and format subdomains with their counts
        return sorted(
            [(subdomain, count) for subdomain, count in self.subdomain_counts.items()],
            key=lambda x: x[0]
        )
    
    def print_report(self):
        # Write report_file
        with open(self.report_file, "w") as report:
            # Question 1: Write the total unique URLs
            report.write(f"Unique Pages: {len(self.unique_urls)}\n\n")
            
            # Question 2: Write the longest page information
            report.write(f"Longest Page: {self.longest_page_url} with {self.longest_word_count} words\n\n")
            
            # Question 3: Write the 50 most common words
            report.write("50 Most Common Words:\n")
            for word, count in self.get_most_common_words(50):
                report.write(f"{word}: {count}\n")
            report.write("\n")
            
            # Question 4: Write subdomains and counts
            report.write("Subdomains and Unique Page Counts:\n")
            for subdomain, count in self.get_subdomain_list():
                report.write(f"{subdomain}, {count}\n")