import os
import zipfile
import xml.etree.ElementTree as ET
import json
from py2neo import Graph, Node
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Neo4j
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

DATA_DIR = "data/raw/irc"
EXTRACT_DIR = "data/processed/irc"

def extract_zip_files():
    """
    Extract all zip files from the raw data folder into the processed folder.
    """
    if not os.path.exists(EXTRACT_DIR):
        os.makedirs(EXTRACT_DIR)

    for file_name in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file_name)
        if file_name.endswith(".zip"):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(EXTRACT_DIR)
                print(f"Extracted {file_name}")
            except zipfile.BadZipFile:
                print(f"Error: {file_name} is not a valid zip file and will be skipped.")
        else:
            print(f"{file_name} is not a zip file and will be skipped.")

def parse_xml_to_json(xml_file):
    """
    Parses the XML file and converts it to a JSON-like structure.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        title_data = {
            "sections": []
        }

        # Debug: Print the root tag to check if XML is loaded correctly
        print(f"Parsing {xml_file}, root tag: {root.tag}")

        # Check the structure of the XML
        for section in root.findall(".//section"):
            section_id = section.attrib.get("id", "")
            heading = section.findtext("heading", "")
            content = section.findtext("p", "")
            
            # Debug: Print found sections
            print(f"Found Section ID: {section_id}, Heading: {heading}")

            section_data = {
                "id": section_id,
                "heading": heading,
                "content": content
            }
            title_data["sections"].append(section_data)

        return title_data

    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
        return None

def ingest_titles(graph, json_data):
    """
    Ingest the titles and sections into the Neo4j graph.
    """
    for section in json_data['sections']:
        section_node = Node("Section", id=section['id'], heading=section['heading'], content=section['content'])
        graph.merge(section_node, "Section", "id")
        print(f"Ingested Section: {section['heading']}")

def ingest_references(graph, json_data):
    """
    Ingest the references between sections in the Neo4j graph.
    This would depend on identifying references in the text (e.g., cross-references between sections).
    """
    # For now, this is a placeholder for linking references
    pass

def process_files():
    """
    Main function to process all XML files, convert to JSON, and load into Neo4j.
    """
    # Extract zip files
    extract_zip_files()

    # Loop through extracted XML files
    for file_name in os.listdir(EXTRACT_DIR):
        if file_name.endswith(".xml"):
            xml_file = os.path.join(EXTRACT_DIR, file_name)
            json_data = parse_xml_to_json(xml_file)
            
            # Ingest the parsed JSON data into Neo4j
            ingest_titles(graph, json_data)
            # Optional: Ingest references between sections
            ingest_references(graph, json_data)
            


if __name__ == "__main__":
    process_files()