import requests
from bs4 import BeautifulSoup
import csv

def scrape_table(url, output_filename):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_div = soup.find('div', class_='table-responsive2')
        if table_div:
            table = table_div.find('table')
            if table:
                with open(output_filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    for row in table.find_all('tr'):
                        cells = [cell.get_text(strip=False) for cell in row.find_all(['th', 'td'])]
                        writer.writerow(cells)
                print(f"Scraped and saved table from {url} to {output_filename}")
        else:
            print(f"No table found at {url}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

def scrape_specific_details(url, output_filename):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        specific_details = soup.find('h2', id='appK').find_parent('details')
        
        if specific_details:
            with open(output_filename, 'w') as f:
                f.write(specific_details.prettify())
            print(f"Scraped and saved specific content from {url} to {output_filename}")
        else:
            print(f"Specific details element not found at {url}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

if __name__ == "__main__":
    # Scrape the tables as CSV directly to the docs folder
    scrape_table(
        url='https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html',
        output_filename='docs/scraped_table_en.csv'
    )
    scrape_table(
        url='https://www.canada.ca/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc.html',
        output_filename='docs/scraped_table_fr.csv'
    )

    # Scrape the specific details for Appendix K directly to the docs folder
    scrape_specific_details(
        url='https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601#appK',
        output_filename='docs/scraped_content_eng.html'
    )
    scrape_specific_details(
        url='https://www.tbs-sct.canada.ca/pol/doc-fra.aspx?id=32601#appK',
        output_filename='docs/scraped_content_fra.html'
    )

