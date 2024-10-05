import os
import re
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

REFERENCE_PATTERN = re.compile(r'id=\"([^"]+)\"')  # Example pattern to find references

def find_references(content):
    """
    Finds references within the section content.
    Adjust the regex pattern based on how references are formatted in the content.
    """
    return REFERENCE_PATTERN.findall(content)

def ingest_references():
    """
    Ingests references between sections into Neo4j.
    """
    for file_name in os.listdir(JSON_DIR):
        if file_name.endswith(".json"):
            json_file = os.path.join(JSON_DIR, file_name)
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for section in data['sections']:
                from_id = section['id']
                content = section['content']
                references = find_references(content)

                for to_id in references:
                    # Find the target section node
                    to_section = graph.nodes.match("Section", id=to_id).first()
                    if to_section:
                        from_section = graph.nodes.match("Section", id=from_id).first()
                        if from_section:
                            relationship = Relationship(from_section, "REFERENCES", to_section)
                            graph.merge(relationship)
                            print(f"Created relationship from {from_id} to {to_id}")
                    else:
                        print(f"Referenced section {to_id} not found in Neo4j.")

if __name__ == "__main__":
    ingest_references()