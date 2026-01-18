import requests
from bs4 import BeautifulSoup
import re
import html2text

def count_links_in_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        links = re.findall(r'\[.*?\]\(.*?\)', content)
        return len(links)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return 0

def count_entries_on_page(url):
    """
    Counts the number of entries in the list or grid on the specified URL.

    Parameters:
        url (str): The URL of the page to scrape.

    Returns:
        int: The number of standard entries found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for grid-based service info sections
        section = soup.find('section', class_='gc-srvinfo')
        if not section:
            section = soup.find('div', class_='row wb-eqht-grd')
        
        if section:
            items = section.find_all('div', class_='col-md-6')
            if items:
                return len(items)

        # Fallback to searching for specific H3 anchors in the main content area
        content_root = soup.find('main') or soup.find(id='wb-cont') or soup.body
        if content_root:
            headers = []
            for h3 in content_root.find_all('h3'):
                anchor = h3.find('a', href=True)
                if not anchor:
                    continue
                href = anchor['href']
                # Check for standard naming patterns in URLs
                if 'data-reference-standard' in href or 'normes-referentielles' in href:
                    headers.append(h3)
            if headers:
                return len(headers)

        print(f"No standards list found on page: {url}")
        return 0
    except Exception as e:
        print(f"Error fetching entries from {url}: {e}")
        return 0

def generate_markdown_files():
    """
    Generates Markdown files by scraping content from the specified URLs.
    """
    urls = [
        ('https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601#appK', 'docs/directive_appendix_k_eng.md'),
        ('https://www.tbs-sct.canada.ca/pol/doc-fra.aspx?id=32601#appK', 'docs/directive_appendix_k_fra.md')
    ]
    for url, output_file in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            directive_content = soup.find('h2', id='appK').find_parent('details')
            if directive_content:
                markdown_converter = html2text.HTML2Text()
                markdown_converter.ignore_links = False
                markdown_converter.body_width = 0
                markdown_content = markdown_converter.handle(directive_content.prettify())
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
        except Exception as e:
            print(f"Error generating markdown for {url}: {e}")
