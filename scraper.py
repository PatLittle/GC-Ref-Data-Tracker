import requests
from bs4 import BeautifulSoup
import csv

def scrape_table(url, output_filename):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_div = soup.find('div', class_='table-responsive2 small')
        if table_div:
            table = table_div.find('table')
            if table:
                with open(output_filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    for row in table.find_all('tr'):
                        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                        writer.writerow(cells)
                print(f"Scraped and saved table from {url} to {output_filename}")
        else:
            print(f"No table found at {url}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

def scrape_html_content(url, output_filename):
    response = requests.get(url)
    if response.status_code == 200):
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.prettify()
        with open(output_filename, 'w') as f:
            f.write(content)
        print(f"Scraped and saved HTML content from {url} to {output_filename}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

if __name__ == "__main__":
    # Scrape the tables as CSV (created in current directory)
    scrape_table(
        url='https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html',
        output_filename='scraped_table_en.csv'
    )
    scrape_table(
        url='https://www.canada.ca/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc.html',
        output_filename='scraped_table_fr.csv'
    )

    # Scrape the HTML content (created in current directory)
    scrape_html_content(
        url='https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601#appK',
        output_filename='scraped_content_eng.html'
    )
    scrape_html_content(
        url='https://www.tbs-sct.canada.ca/pol/doc-fra.aspx?id=32601#appK',
        output_filename='scraped_content_fra.html'
    )
