from bs4 import BeautifulSoup
from collections import Counter
import re

class CrawlerClass:
    def __init__(self):
        self.unique_urls = set()  # Set to store unique URLs
        self.scraped_file = "scraped_urls.txt"  # File to store scraped URLs
        self.longest_word_count = 0

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

    def update_words(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()  
        words = text.split()
        self.longest_word_count = max(self.longest_word_count, len(words))

        p3_words = re.findall(r'\w+', text.lower())
        filtered_words = [word for word in p3_words if word not in self.stop_words] 
        self.word_counts.update(filtered_words)

    def get_most_common_words(self, n=50):
        return self.word_counts.most_common(n)