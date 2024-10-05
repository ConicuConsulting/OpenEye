import os
import json
from py2neo import Graph, Node
from dotenv import load_dotenv
import logging
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename='ingest_into_neo4j.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load environment variables
load_dotenv()

# Connect to Neo4j
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

JSON_DIR = "data/processed/irc/json"
BATCH_SIZE = 1000  # Adjust based on performance

def ingest_batch(batch):
    tx = graph.begin()
    ingested = 0
    for section in batch:
        section_id = section.get('id', '')
        if not section_id:
            logging.warning(f"Skipping section with missing ID: {section.get('heading', 'No Heading')}")
            continue  # Skip sections without ID
        heading = section.get('heading', '')
        content = section.get('content', '')
        section_node = Node("Section", id=section_id, heading=heading, content=content)
        tx.merge(section_node, "Section", "id")
        ingested += 1
    tx.commit()
    logging.info(f"Ingested batch of {ingested} sections.")
    return ingested

def ingest_all_json():
    sections = []
    json_files = [os.path.join(JSON_DIR, f) for f in os.listdir(JSON_DIR) if f.endswith(".json")]

    # Gather all sections
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                sections.extend(data.get('sections', []))
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON file {json_file}: {e}")

    # Remove sections without ID
    sections = [s for s in sections if s.get('id')]

    total = len(sections)
    logging.info(f"Total sections to ingest: {total}")

    # Split into batches
    batches = [sections[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]

    # Use multiprocessing Pool
    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap(ingest_batch, batches), total=len(batches)))

    total_ingested = sum(results)
    logging.info(f"Successfully ingested {total_ingested} sections into Neo4j.")

if __name__ == "__main__":
    ingest_all_json()