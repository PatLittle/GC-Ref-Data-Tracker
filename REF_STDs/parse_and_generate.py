import os
import json
import markdown
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

def parse_markdown_files(subdir_path):
    data = {}
    for filename in os.listdir(subdir_path):
        if filename.endswith('.md'):
            with open(os.path.join(subdir_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                data[filename] = content
    return data

def generate_shacl(data, subdir_path):
    SH = Namespace("http://www.w3.org/ns/shacl#")
    EX = Namespace("http://example.org/")
    g = Graph()
    g.bind("sh", SH)
    g.bind("ex", EX)

    standard = URIRef(EX["Standard"])
    g.add((standard, RDF.type, SH.NodeShape))
    g.add((standard, SH.targetClass, EX.Standard))

    for filename, content in data.items():
        properties = extract_properties_from_md(content)
        for prop in properties:
            prop_uri = URIRef(EX[prop])
            g.add((prop_uri, RDF.type, SH.PropertyShape))
            g.add((prop_uri, SH.path, prop_uri))
            g.add((prop_uri, SH.datatype, XSD.string))
            g.add((standard, SH.property, prop_uri))

    shacl_file = os.path.join(subdir_path, 'standard.shacl')
    g.serialize(destination=shacl_file, format='turtle')

def generate_json_schema(data, subdir_path):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {}
    }

    for filename, content in data.items():
        properties = extract_properties_from_md(content)
        for prop in properties:
            schema["properties"][prop] = {"type": "string"}

    schema_file = os.path.join(subdir_path, 'schema.json')
    with open(schema_file, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)

def extract_properties_from_md(content):
    # Placeholder function to extract properties from markdown content
    # Actual implementation will depend on the structure of the markdown files
    return ["property1", "property2"]

def main():
    base_dir = 'REF_STDs'
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            data = parse_markdown_files(subdir_path)
            generate_shacl(data, subdir_path)
            generate_json_schema(data, subdir_path)

if __name__ == "__main__":
    main()
