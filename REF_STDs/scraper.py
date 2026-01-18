import json
import os
import re
from urllib.parse import urljoin, urlparse

import markdownify
import requests
from bs4 import BeautifulSoup

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(url, dest_folder):
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except requests.RequestException as exc:
        print(f"Failed to download {url}: {exc}")
        return None

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
    return ["property1", "property2"]

def _sanitize_directory_name(text):
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned.replace(" ", "_")

def _resolve_directory_name(base_dir, desired_name):
    desired_lower = desired_name.lower()
    if os.path.exists(base_dir):
        for existing in os.listdir(base_dir):
            if existing.lower() == desired_lower:
                return existing
    return desired_name

def _standard_links_from_listing(soup, base_url):
    section = soup.find("section", class_="gc-srvinfo")
    if not section:
        section = soup.find("div", class_="row wb-eqht-grd")
    links = []
    if section:
        for item in section.find_all("h3"):
            anchor = item.find("a", href=True)
            if anchor:
                links.append(urljoin(base_url, anchor["href"]))
        if links:
            return links

    content_root = soup.find("main") or soup.find(id="wb-cont") or soup.body
    if content_root:
        for anchor in content_root.find_all("a", href=True):
            href = anchor["href"]
            if "data-reference-standard" in href or "normes-referentielles" in href:
                links.append(urljoin(base_url, href))
    return list(dict.fromkeys(links))

def _download_standard_detail(detail_url, dest_folder, html_content):
    parsed = urlparse(detail_url)
    filename = os.path.basename(parsed.path) or "index.html"
    local_filename = os.path.join(dest_folder, filename)
    with open(local_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    md_content = convert_html_to_md(html_content)
    md_filename = os.path.splitext(local_filename)[0] + ".md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(md_content)

    return html_content

def scrape_table(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    detail_links = _standard_links_from_listing(soup, url)

    if not detail_links:
        print("No standard links found. Here is the HTML content:")
        print(soup.prettify())
        return

    for detail_url in detail_links:
        detail_response = requests.get(detail_url)
        detail_response.raise_for_status()
        detail_html = detail_response.text
        detail_soup = BeautifulSoup(detail_html, "html.parser")

        title = ""
        h1 = detail_soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
        if not title:
            title = detail_url.split("/")[-1]
            
        subdir_name = _sanitize_directory_name(title)
        subdir_name = _resolve_directory_name("REF_STDs", subdir_name)
        subdir_path = os.path.join("REF_STDs", subdir_name)
        create_directory(subdir_path)

        _download_standard_detail(detail_url, subdir_path, detail_html)

        content_root = detail_soup.find("main") or detail_soup.find(id="wb-cont") or detail_soup.body
        if content_root:
            for link in content_root.find_all("a", href=True):
                # Logic continues for nested file downloads if necessary
                pass
        
        generate_shacl_and_json_schema(subdir_path)
