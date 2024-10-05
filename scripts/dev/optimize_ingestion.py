import os
import json
from py2neo import Graph, Node
from dotenv import load_dotenv
from multiprocessing import Pool, cpu_count
from functools import partial
from tqdm import tqdm
import time

# Load environment variables
load_dotenv()

# Connect to Neo4j
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

JSON_DIR = "data/processed/irc/json"
BATCH_SIZE = 500  # Adjust based on performance

def ingest_batch(batch):
    retries = 3
    for attempt in range(retries):
        try:
            tx = graph.begin()
            for section in batch:
                section_id = section['id']
                if not section_id:
                    continue  # Skip sections without ID
                heading = section['heading']
                content = section['content']
                section_node = Node("Section", id=section_id, heading=heading, content=content)
                tx.merge(section_node, "Section", "id")
            tx.commit()
            return len(batch)
        except Exception as e:
            print(f"Error: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(2 ** attempt)  # Exponential backoff
    return 0

def ingest_all_json():
    files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json')]
    all_sections = []
    for file in files:
        with open(os.path.join(JSON_DIR, file), 'r') as f:
            sections = json.load(f)
            all_sections.extend(sections)
    
    print(f"Total sections to ingest: {len(all_sections)}")
    
    batches = [all_sections[i:i + BATCH_SIZE] for i in range(0, len(all_sections), BATCH_SIZE)]
    
    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap(ingest_batch, batches), total=len(batches)))
    
    print(f"Total sections ingested: {sum(results)}")
    print("Problematic data:", section_data)

if __name__ == "__main__":
    ingest_all_json()