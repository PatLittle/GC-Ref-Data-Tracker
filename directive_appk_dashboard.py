import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


import re

def count_links_in_markdown(file_path):
    """
    Counts the number of links in a Markdown file.

    Parameters:
        file_path (str): The path to the Markdown file.

    Returns:
        int: The number of links in the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Match Markdown-style links: [text](url)
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
    Counts the number of entries in the table on the specified URL.

    Parameters:
        url (str): The URL of the page to scrape.

    Returns:
        int: The number of table rows (excluding the header).
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('div', class_='table-responsive2').find('table')
        if table:
            rows = table.find_all('tr')
            return len(rows) - 1  # Exclude header row
        else:
            print(f"No table found on page: {url}")
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
                print(f"Saved {output_file}")
            else:
                print(f"Directive content not found at {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")



def append_to_csv(date, status, en_appk, en_canadaca, fr_appk, fr_canadaca):
    """
    Appends a row of data to the CSV file.
    """
    csv_file = 'docs/chart_data.csv'
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if f.tell() == 0:  # Write headers if file is empty
                writer.writerow(['date', 'status', 'EN_AppK', 'EN_Canadaca', 'FR_AppK', 'FR_Canadaca'])
            writer.writerow([date, status, en_appk, en_canadaca, fr_appk, fr_canadaca])
        print(f"Appended data to {csv_file}")
    except Exception as e:
        print(f"Error appending to CSV: {e}")


def generate_bar_chart_widget(markdown_files, reference_pages):
    """
    Generates the Chart.js widget and updates the CSV file.
    """
    data = []
    labels = ['ENGLISH', 'FRENCH']
    markdown_links = []
    page_entries = []
    all_equal = True

    for file, page in zip(markdown_files, reference_pages):
        md_links = count_links_in_markdown(file)
        entries = count_entries_on_page(page)
        markdown_links.append(md_links)
        page_entries.append(entries)
        if md_links != entries:
            all_equal = False

    chart_title = "✅Directive on Service and Digital: Appendix K updated 🆗" if all_equal else "🚩Directive on Service and Digital: Appendix K not updated 🆖"

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_to_csv(now, chart_title, markdown_links[0], page_entries[0], markdown_links[1], page_entries[1])

    print("Bar chart and CSV update completed.")


if __name__ == "__main__":
    generate_markdown_files()
    markdown_files = [
        'docs/directive_appendix_k_eng.md',
        'docs/directive_appendix_k_fra.md'
    ]
    reference_pages = [
        'https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html',
        'https://www.canada.ca/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc.html'
    ]
    generate_bar_chart_widget(markdown_files, reference_pages)
