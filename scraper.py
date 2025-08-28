import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
from urllib.parse import urljoin


def scrape_standards_page(url, output_filename):
    """
    Scrape a GC "Reference standards" page and write a CSV with the columns:
    Title, Description, Effective date, Data reference standard stewards,
    Machine-readable formats (available on Open Government)

    This function is robust to English and French label variants like:
      - "Effective date", "Date d’entrée en vigueur"
      - "Stewards", "Responsable(s)"
      - "Machine-readable formats", "Format lisible par machine"
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to retrieve {url}, status code: {resp.status_code}")
        return

    soup = BeautifulSoup(resp.content, "html.parser")

    # Find the section that contains the standards list
    section = soup.find("section", class_="gc-srvinfo")
    if not section:
        section = soup.find("div", class_="row wb-eqht-grd")
    if not section:
        print(f"Could not find standards section on {url}")
        return

    item_divs = section.find_all("div", class_="col-md-6")
    if not item_divs:
        # fallback: maybe items are direct children
        item_divs = section.find_all("div", recursive=False)

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
        """
        Return which field the label likely corresponds to: 'effective', 'stewards', 'machine', or None
        """
        lab = label_text.lower()
        # check for steward/responsable first (exact words are less ambiguous)
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
        # Title
        title = ""
        h3 = item.find("h3")
        if h3:
            # If the title contains an <a>, take the text of the link (or h3 text)
            a = h3.find("a")
            title = a.get_text(" ", strip=True) if a else h3.get_text(" ", strip=True)

        # Description: usually the first <p> after the h3 (or first p in item)
        description = ""
        if h3:
            desc_p = h3.find_next_sibling("p")
            if desc_p:
                description = desc_p.get_text(" ", strip=True)
        if not description:
            p_tags = item.find_all("p")
            if p_tags:
                description = p_tags[0].get_text(" ", strip=True)

        # Metadata paragraph (the one containing <strong> labels)
        meta_p = None
        # There are cases where the metadata is in the same p as the description (second p)
        p_tags = item.find_all("p")
        for p in p_tags:
            if p.find("strong"):
                meta_p = p
                break
        # also check the p immediately following h3 (already attempted above)
        if not meta_p and h3:
            maybe = h3.find_next_sibling("p")
            if maybe and maybe.find("strong"):
                meta_p = maybe

        effective = ""
        stewards = ""
        machine = ""

        if meta_p:
            # iterate through <strong> tags and capture the content after each strong
            strongs = meta_p.find_all("strong")
            if strongs:
                for strong in strongs:
                    label = strong.get_text(" ", strip=True).rstrip(":").strip()
                    field = match_label(label)
                    # accumulate the text / links after this strong up until the next strong
                    parts = []
                    for sib in strong.next_siblings:
                        # stop if we reach the next strong tag
                        if isinstance(sib, Tag) and sib.name == "strong":
                            break
                        if isinstance(sib, NavigableString):
                            txt = str(sib).strip()
                            if txt:
                                parts.append(txt)
                        elif isinstance(sib, Tag):
                            if sib.name == "a" and sib.get("href"):
                                href = urljoin(url, sib["href"])
                                link_text = sib.get_text(" ", strip=True)
                                parts.append(f"{link_text} ({href})")
                            else:
                                txt = sib.get_text(" ", strip=True)
                                if txt:
                                    parts.append(txt)
                    value = " ".join(parts).strip()
                    value = " ".join(value.split())

                    if field == "effective":
                        # remove leading separators
                        effective = value.strip(" :;|")
                    elif field == "stewards":
                        stewards = value.strip(" :;|")
                    elif field == "machine":
                        machine = value.strip(" :;|")

            # If no strong tags or some fields still empty, try regex-free heuristics:
            if (not machine) or (not stewards) or (not effective):
                # collect all a tags in meta_p as machine-readable links if machine empty
                if not machine:
                    links = []
                    for a in meta_p.find_all("a", href=True):
                        href = urljoin(url, a["href"])
                        text = a.get_text(" ", strip=True)
                        links.append(f"{text} ({href})")
                    machine = " | ".join(links)

                # if stewards still empty, try to extract text following known steward markers in the p
                if not stewards:
                    txt = meta_p.get_text(" ", strip=True)
                    # crude split on common labels
                    for marker in ["Stewards:", "Stewards :", "Stewards", "Steward:", "Steward :", "Stewards", "Responsable :", "Responsables :", "Responsable:", "Responsables", "Responsable"]:
                        if marker in txt:
                            parts = txt.split(marker, 1)[1].strip()
                            # if another label occurs after, trim it
                            for other in ["Effective", "Date d’entrée", "Format lisible", "Format lisible par machine", "Machine-readable", "Effective date", "Date"]:
                                if other in parts:
                                    parts = parts.split(other, 1)[0].strip(" :;|")
                            stewards = parts
                            break

                # if effective empty, try similar heuristic
                if not effective:
                    txt = meta_p.get_text(" ", strip=True)
                    for marker in ["Effective date:", "Effective date :", "Effective date", "Date d’entrée en vigueur :", "Date d’entrée en vigueur:", "Date d’entrée en vigueur", "Date d’entrée :", "Date d’entrée:", "Date d’entrée", "Date d'entrée", "Date :"]:
                        if marker in txt:
                            parts = txt.split(marker, 1)[1].strip()
                            for other in ["Stewards", "Responsable", "Format lisible", "Machine-readable", "Format lisible par machine"]:
                                if other in parts:
                                    parts = parts.split(other, 1)[0].strip(" :;|")
                            effective = parts
                            break

        # Normalize final values
        effective = effective.strip(" |;: ")
        stewards = stewards.strip(" |;: ")
        machine = machine.strip(" |;: ")

        rows.append([title, description, effective, stewards, machine])

    # Write CSV with exact header names requested
    headers = [
        "Title",
        "Description",
        "Effective date",
        "Data reference standard stewards",
        "Machine-readable formats (available on Open Government)",
    ]

    try:
        with open(output_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for r in rows:
                writer.writerow(r)
        print(f"Scraped and saved {len(rows)} items from {url} to {output_filename}")
    except Exception as e:
        print(f"Failed to write {output_filename}: {e}")


# keep compatibility with the previous function name
def scrape_table(url, output_filename):
    return scrape_standards_page(url, output_filename)


def scrape_specific_details(url, output_filename):
    """
    Preserve the previous helper to scrape specific Appendix K details if needed.
    This is left mostly unchanged but hardened against missing elements.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # safe lookup for the element
        el = soup.find(id="appK")
        if el:
            # try to find the <details> parent or write the section around the id
            parent = el.find_parent("details")
            content = parent.prettify() if parent else el.prettify()
            try:
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Scraped and saved specific content from {url} to {output_filename}")
            except Exception as e:
                print(f"Failed to write {output_filename}: {e}")
        else:
            print(f"Specific details element with id 'appK' not found at {url}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")


if __name__ == "__main__":
    # English page
    scrape_table(
        url="https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html",
        output_filename="docs/scraped_table_en.csv",
    )

    # French page
    scrape_table(
        url="https://www.canada.ca/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc.html",
        output_filename="docs/scraped_table_fr.csv",
    )

    # Appendix K scraping (kept for backward compatibility)
    scrape_specific_details(
        url="https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601#appK",
        output_filename="docs/scraped_content_eng.html",
    )
    scrape_specific_details(
        url="https://www.tbs-sct.canada.ca/pol/doc-fra.aspx?id=32601#appK",
        output_filename="docs/scraped_content_fra.html",
    )
