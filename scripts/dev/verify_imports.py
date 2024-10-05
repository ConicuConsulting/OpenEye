from py2neo import Graph
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to Neo4j
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def verify_counts():
    query = "MATCH (s:Section) RETURN COUNT(s) AS total_sections"
    result = graph.run(query).data()
    total_sections = result[0]['total_sections'] if result else 0
    print(f"Total Sections in Neo4j: {total_sections}")

def verify_sample_sections():
    query = """
    MATCH (s:Section)
    RETURN s.id, s.heading, s.content
    LIMIT 10
    """
    results = graph.run(query).data()
    print("Sample Sections:")
    for record in results:
        print(record)

def verify_relationships():
    query = "MATCH (s1:Section)-[r:REFERENCES]->(s2:Section) RETURN COUNT(r) AS total_relationships"
    result = graph.run(query).data()
    total_relationships = result[0]['total_relationships'] if result else 0
    print(f"Total Relationships in Neo4j: {total_relationships}")

def verify_sample_relationships():
    query = """
    MATCH (s1:Section)-[r:REFERENCES]->(s2:Section)
    RETURN s1.id AS from_id, s1.heading AS from_heading, s2.id AS to_id, s2.heading AS to_heading
    LIMIT 10
    """
    results = graph.run(query).data()
    print("Sample Relationships:")
    for record in results:
        print(record)

if __name__ == "__main__":
    verify_counts()
    verify_sample_sections()
    verify_relationships()
    verify_sample_relationships()