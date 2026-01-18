import csv
import gzip
import json
from datetime import datetime, timezone

import requests

SOURCE_URL = "https://open.canada.ca/static/od-do-canada.jsonl.gz"
OUTPUT_CSV = "docs/open_data_relationships.csv"
OUTPUT_JSONL = "docs/open_data_relationships.jsonl"


def _translated_value(data, key):
    value = data.get(key) if isinstance(data, dict) else None
    if isinstance(value, dict):
        return value
    return {}


def _relationship_rows(
    source_level,
    package_id,
    package_titles,
    resource_id,
    resource_titles,
    relationship,
):
    related_urls = relationship.get("related_url") or {}
    related_url_en = related_urls.get("en", "") if isinstance(related_urls, dict) else ""
    related_url_fr = related_urls.get("fr", "") if isinstance(related_urls, dict) else ""
    return [
        source_level,
        package_id,
        package_titles.get("en", ""),
        package_titles.get("fr", ""),
        resource_id or "",
        resource_titles.get("en", ""),
        resource_titles.get("fr", ""),
        relationship.get("related_relationship", ""),
        relationship.get("resource_type", ""),
        related_url_en,
        related_url_fr,
    ]


def fetch_relationships():
    headers = [
        "source_level",
        "package_id",
        "package_title_en",
        "package_title_fr",
        "resource_id",
        "resource_title_en",
        "resource_title_fr",
        "relationship_type",
        "related_resource_type",
        "related_url_en",
        "related_url_fr",
    ]

    with (
        requests.get(SOURCE_URL, stream=True, timeout=60) as response,
        open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csv_file,
        open(OUTPUT_JSONL, "w", encoding="utf-8") as jsonl_file,
    ):
        response.raise_for_status()
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        for line in gzip.GzipFile(fileobj=response.raw):
            if not line.strip():
                continue
            package = json.loads(line)
            package_id = package.get("id") or package.get("package_id")
            package_titles = _translated_value(package, "title_translated")

            package_relationships = package.get("relationship") or []
            resources_with_relationships = []

            for relationship in package_relationships:
                writer.writerow(
                    _relationship_rows(
                        "package",
                        package_id,
                        package_titles,
                        "",
                        {},
                        relationship,
                    )
                )

            for resource in package.get("resources", []) or []:
                resource_relationships = resource.get("relationship") or []
                if not resource_relationships:
                    continue
                resource_id = resource.get("resource_id") or resource.get("id")
                resource_titles = _translated_value(resource, "name_translated")
                resources_with_relationships.append(
                    {
                        "resource_id": resource_id,
                        "name_translated": resource_titles,
                        "relationship": resource_relationships,
                    }
                )
                for relationship in resource_relationships:
                    writer.writerow(
                        _relationship_rows(
                            "resource",
                            package_id,
                            package_titles,
                            resource_id,
                            resource_titles,
                            relationship,
                        )
                    )

            if package_relationships or resources_with_relationships:
                jsonl_file.write(
                    json.dumps(
                        {
                            "package_id": package_id,
                            "title_translated": package_titles,
                            "relationship": package_relationships,
                            "resources": resources_with_relationships,
                            "source_timestamp": datetime.now(timezone.utc).isoformat(),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )


if __name__ == "__main__":
    fetch_relationships()
