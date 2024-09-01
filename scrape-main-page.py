import requests
from bs4 import BeautifulSoup
import csv

def scrape_table(url, output_filename):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Locate the div with the class "table-responsive2 small" and then find the table within it
        table_div = soup.find('div', class_='table-responsive2 small')
        if table_div:
            table = table_div.find('table')

            if table:
                # Extract table headers
                headers = [header.text.strip() for header in table.find_all('th')]

                # Extract table rows
                rows = []
                for row in table.find('tbody').find_all('tr'):
                    cells = row.find_all('td')
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    rows.append(row_data)

                # Write data to CSV
                with open(output_filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(rows)

                print(f"Scraping and saving to {output_filename} successful!")
            else:
                print("Table not found.")
        else:
            print("Div with the specified class not found.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    # English version
    scrape_table(
        url='https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html',
        output_filename='scraped_table_en.csv'
    )
    
    # French version
    scrape_table(
        url='https://www.canada.ca/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc.html',
        output_filename='scraped_table_fr.csv'
    )
