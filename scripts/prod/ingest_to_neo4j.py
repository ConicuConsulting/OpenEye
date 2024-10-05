import os
import json
from py2neo import Graph, Node, Relationship
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Neo4j
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

JSON_DIR = "data/processed/irc/json"

def ingest_titles(json_file):
    """
    Ingests sections from a JSON file into Neo4j.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for section in data['sections']:
        section_id = section['id']
        heading = section['heading']
        content = section['content']

        # Create or merge the Section node
        section_node = Node("Section", id=section_id, heading=heading, content=content)
        graph.merge(section_node, "Section", "id")
      #  print(f"Ingested Section: {heading} (ID: {section_id})")

def ingest_all_json():
    """
    Ingests all JSON files in the JSON directory into Neo4j.
    """
    for file_name in os.listdir(JSON_DIR):
        if file_name.endswith(".json"):
            json_file = os.path.join(JSON_DIR, file_name)
            ingest_titles(json_file)

if __name__ == "__main__":
    ingest_all_json()