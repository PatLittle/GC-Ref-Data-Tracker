import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


def _find_standards_items(soup):
    section = soup.find("section", class_="gc-srvinfo")
    if not section:
        section = soup.find("div", class_="row wb-eqht-grd")
    if section:
        item_divs = section.find_all("div", class_="col-md-6")
        if item_divs:
            return item_divs
        return section.find_all("div", recursive=False)

    content_root = soup.find("main") or soup.find(id="wb-cont") or soup.body
    items = []
    if content_root:
        for h3 in content_root.find_all("h3"):
            link = h3.find("a", href=True)
            if not link:
                continue
            href = link["href"]
            if "data-reference-standard" not in href and "norme" not in href:
                continue
            container = h3.find_parent(["div", "section", "article"]) or h3
            items.append(container)
    return items


def scrape_standards_page(url, output_filename):
    """
    Scrape a GC "Reference standards" page and write a CSV with the columns:
    Title, Description, Effective date, Data reference standard stewards,
    Machine-readable formats (available on Open Government)
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to retrieve {url}, status code: {resp.status_code}")
        return

    soup = BeautifulSoup(resp.content, "html.parser")

    item_divs = _find_standards_items(soup)
    if not item_divs:
        print(f"Could not find standards section on {url}")
        return

    rows = []

    # keyword lists for label matching (English and French)
    effective_keywords = [
        "effective", "effective date", "date d’entrée", "date d’entrée en vigueur",
        "date d’entrée en vigueur :", "date d’entrée en vigueur", "date d’entrée",
        "date d'entrée", "date"
    ]
    steward_keywords = ["steward", "stewards", "responsable", "responsables"]
    machine_keywords = ["machine", "machine-readable", "machine-readable formats",
                        "format lisible", "format lisible par machine", "formats lisibles par machine",
                        "formats lisibles", "format lisible par machine"]

    def match_label(label_text):
        lab = label_text.lower()
        for k in steward_keywords:
            if k in lab:
                return "stewards"
        for k in machine_keywords:
            if k in lab:
                return "machine"
        for k in effective_keywords:
            if k in lab:
                return "effective"
        return None

    for item in item_divs:
        h3 = item.find("h3")
        title = h3.get_text(" ", strip=True) if h3 else "Unknown Title"

        description = ""
        if h3:
            desc_p = h3.find_next_sibling("p")
            if desc_p:
                description = desc_p.get_text(" ", strip=True)
        if not description:
            p_tags = item.find_all("p")
            if p_tags:
                description = p_tags[0].get_text(" ", strip=True)

        meta_p = None
        p_tags = item.find_all("p")
        for p in p_tags:
            if p.find("strong"):
                meta_p = p
                break
        
        if not meta_p and h3:
            maybe = h3.find_next_sibling("p")
            if maybe and maybe.find("strong"):
                meta_p = maybe
        
        # fallback: check other containers like lists or divs with strong tags
        if not meta_p:
            for candidate in item.find_all(["div", "ul", "ol", "dl"]):
                if candidate.find("strong"):
                    meta_p = candidate
                    break

        effective = ""
        stewards = ""
        machine = ""

        if meta_p:
            strongs = meta_p.find_all("strong")
            if strongs:
                for strong in strongs:
                    label = strong.get_text(" ", strip=True).rstrip(":").strip()
                    field = match_label(label)
                    parts = []
                    for sib in strong.next_siblings:
                        if isinstance(sib, Tag) and sib.name == "strong":
                            break
                        if isinstance(sib, NavigableString):
                            txt = str(sib).strip()
                            if txt:
                                parts.append(txt)
                        elif isinstance(sib, Tag):
                            if sib.name == "a" and sib.get("href"):
                                href = urljoin(url, sib["href"])
                                parts.append(f"{sib.get_text(strip=True)} ({href})")
                    
                    val = " ".join(parts).strip()
                    if field == "effective": effective = val
                    elif field == "stewards": stewards = val
                    elif field == "machine": machine = val

        rows.append([title, description, effective, stewards, machine])

    with open(output_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Description", "Effective date", "Stewards", "Machine-readable formats"])
        writer.writerows(rows)
