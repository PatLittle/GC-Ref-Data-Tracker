import os
import requests
from bs4 import BeautifulSoup
import markdownify
import json

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(url, dest_folder):
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def convert_html_to_md(html_content):
    return markdownify.markdownify(html_content, heading_style="ATX")

def generate_shacl_and_json_schema(subdir_path):
    shacl_data = {
        "@context": "http://www.w3.org/ns/shacl#",
        "@type": "NodeShape",
        "targetClass": "http://example.org/Standard",
        "property": []
    }
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {}
    }

    for filename in os.listdir(subdir_path):
        if filename.endswith('.md'):
            with open(os.path.join(subdir_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract properties from markdown content
                # This is a placeholder, actual extraction logic will depend on the content structure
                properties = extract_properties_from_md(content)
                for prop in properties:
                    shacl_data["property"].append({
                        "path": f"http://example.org/{prop}",
                        "datatype": "http://www.w3.org/2001/XMLSchema#string"
                    })
                    json_schema["properties"][prop] = {"type": "string"}

    with open(os.path.join(subdir_path, 'standard.shacl'), 'w', encoding='utf-8') as f:
        json.dump(shacl_data, f, indent=2)

    with open(os.path.join(subdir_path, 'schema.json'), 'w', encoding='utf-8') as f:
        json.dump(json_schema, f, indent=2)

def extract_properties_from_md(content):
    # Placeholder function to extract properties from markdown content
    # Actual implementation will depend on the structure of the markdown files
    return ["property1", "property2"]

def scrape_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table_div = soup.find('div', id='wb-auto-4_info')
    if table_div:
        table = table_div.find('table')
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')
                subdir_name = cells[0].get_text(strip=True).replace(' ', '_')
                subdir_path = os.path.join('REF_STDs', subdir_name)
                create_directory(subdir_path)

                for link in row.find_all('a', href=True):
                    file_url = link['href']
                    downloaded_file = download_file(file_url, subdir_path)

                    if downloaded_file.endswith('.html'):
                        with open(downloaded_file, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        md_content = convert_html_to_md(html_content)
                        md_filename = os.path.splitext(downloaded_file)[0] + '.md'
                        with open(md_filename, 'w', encoding='utf-8') as f:
                            f.write(md_content)

                        if 'lang-toggle' in html_content:
                            fr_url = file_url.replace('/en/', '/fr/')
                            fr_downloaded_file = download_file(fr_url, subdir_path)
                            with open(fr_downloaded_file, 'r', encoding='utf-8') as f:
                                fr_html_content = f.read()
                            fr_md_content = convert_html_to_md(fr_html_content)
                            fr_md_filename = os.path.splitext(fr_downloaded_file)[0] + '.md'
                            with open(fr_md_filename, 'w', encoding='utf-8') as f:
                                f.write(fr_md_content)

                generate_shacl_and_json_schema(subdir_path)
        else:
            print(f"No table found at {url}")
    else:
        print(f"No table div found at {url}")


if __name__ == "__main__":
    create_directory('REF_STDs')
    scrape_table('https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html')
