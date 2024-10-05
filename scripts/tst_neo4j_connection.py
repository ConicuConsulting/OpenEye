from py2neo import Graph
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

try:
    graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    print("Connection to Neo4j established successfully.")
except Exception as e:
    print(f"Failed to connect to Neo4j: {e}")