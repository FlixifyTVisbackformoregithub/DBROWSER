import requests
from bs4 import BeautifulSoup
from whoosh.index import open_dir

def crawl_and_index(start_url):
    # Function to crawl a given URL and index its content
    urls_to_crawl = [start_url]
    crawled_urls = set()
    
    # Set a simple depth limit
    depth_limit = 2

    while urls_to_crawl:
        url = urls_to_crawl.pop(0)
        if url in crawled_urls:
            continue
        if len(crawled_urls) >= depth_limit:
            break
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except (requests.HTTPError, requests.RequestException) as e:
            print(f"Failed to crawl {url}: {str(e)}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.text for p in paragraphs])

        # Index the scraped data
        ix = open_dir("indexdir")
        writer = ix.writer()
        writer.add_document(title=url, content=text)
        writer.commit()

        crawled_urls.add(url)
        print(f"Crawled and indexed: {url}")

        # Logic to find new URLs
        for link in soup.find_all('a', href=True):
            full_url = link['href']
            if full_url.startswith('http') and not full_url in crawled_urls:
                urls_to_crawl.append(full_url)
