import os

import json
import zipfile
import xml.etree.ElementTree as ET
from py2neo import Graph, Node, Relationship


import os
import zipfile

# Configuration from .env (make sure you have the dotenv library installed)
from dotenv import load_dotenv
load_dotenv()

# Connect to Neo4j
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

DATA_DIR = "data/raw/irc"
EXTRACT_DIR = "data/processed/irc"

def is_valid_zip(file_path):
    """
    Check if the file at file_path is a valid zip file.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            return True
    except zipfile.BadZipFile:
        return False

def extract_zip_files():
    """
    Extract all zip files from the raw data folder into the processed folder.
    """
    if not os.path.exists(EXTRACT_DIR):
        os.makedirs(EXTRACT_DIR)

    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".zip"):
            file_path = os.path.join(DATA_DIR, file_name)
            if is_valid_zip(file_path):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(EXTRACT_DIR)
                print(f"Extracted {file_name}")
            else:
                print(f"Error: {file_name} is not a valid zip file and will be skipped.")


def parse_xml_to_json(xml_file):
    """
    Parses the XML file and converts it to JSON-like structure.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    title_data = {
        "sections": []
    }

    # Example parsing logic: Adjust as needed depending on XML structure
    for section in root.findall(".//section"):
        section_data = {
            "id": section.attrib.get("id", ""),
            "heading": section.findtext("heading", ""),
            "content": section.findtext("p", "")
        }
        title_data["sections"].append(section_data)

    return title_data

def ingest_into_neo4j(json_data):
    """
    Takes JSON data and ingests it into Neo4j database.
    """
    for section in json_data['sections']:
        section_node = Node("Section", id=section['id'], heading=section['heading'], content=section['content'])
        graph.merge(section_node, "Section", "id")
        print(f"Ingested Section: {section['heading']}")

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
            ingest_into_neo4j(json_data)

if __name__ == "__main__":
    process_files()