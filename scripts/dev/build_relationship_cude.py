import os
import re
import json
import torch
from py2neo import Graph, Relationship
from dotenv import load_dotenv
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import logging

# Configure logging
logging.basicConfig(
    filename='build_relationships_cuda.log',
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
CUDA_PROCESSED_DIR = "data/processed/irc/cuda_processed"

# Define reference patterns
REFERENCE_PATTERNS = [
    re.compile(r'§\s*(\d+)', re.IGNORECASE),  # Matches '§ 7405'
    re.compile(r'Section\s*(\d+)', re.IGNORECASE),  # Matches 'Section 7405'
    # Add more patterns as needed
]

def find_references(content):
    """
    Finds references within the section content.
    """
    references = set()
    for pattern in REFERENCE_PATTERNS:
        matches = pattern.findall(content)
        references.update(matches)
    return list(references)

def process_section(section):
    from_id = section['id']
    content = section['content']
    references = find_references(content)
    relationships = []
    for ref in references:
        # Assuming 'ref' is a numeric identifier that maps to a section ID
        to_id = f"id{ref}"
        relationships.append((from_id, to_id))
    return relationships

def ingest_relationships(batch_relationships):
    tx = graph.begin()
    ingested = 0
    for from_id, to_id in batch_relationships:
        from_section = graph.nodes.match("Section", id=from_id).first()
        to_section = graph.nodes.match("Section", id=to_id).first()
        if from_section and to_section:
            relationship = Relationship(from_section, "REFERENCES", to_section)
            tx.merge(relationship)
            ingested += 1
        else:
            logging.warning(f"Referenced section {to_id} not found for {from_id}.")
    tx.commit()
    logging.info(f"Ingested batch of {ingested} relationships.")
    return ingested

def build_relationships_cuda():
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
    logging.info(f"Total sections to process for relationships: {total}")

    # Use GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")

    # Prepare data for GPU processing
    section_contents = [s['content'] for s in sections]
    from_ids = [s['id'] for s in sections]

    # Dummy tensor operation to simulate GPU processing (replace with actual GPU-accelerated tasks if needed)
    # For this example, we'll assume the find_references function is fast enough on CPU
    # and doesn't require GPU acceleration. If you have more complex processing, implement it here.

    # Parallel processing using multiprocessing
    def batch_process(batch):
        batch_relationships = []
        for section in batch:
            relationships = process_section(section)
            batch_relationships.extend(relationships)
        return batch_relationships

    BATCH_SIZE = 1000
    batches = [sections[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]

    with Pool(processes=cpu_count()) as pool:
        batch_relationships_list = list(tqdm(pool.imap(batch_process, batches), total=len(batches)))

    # Flatten the list
    all_relationships = [rel for batch in batch_relationships_list for rel in batch]
    logging.info(f"Total relationships found: {len(all_relationships)}")

    # Ingest relationships in batches
    ingest_batches = [all_relationships[i:i + BATCH_SIZE] for i in range(0, len(all_relationships), BATCH_SIZE)]

    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap(ingest_relationships, ingest_batches), total=len(ingest_batches))))

    total_ingested = sum(results)
    logging.info(f"Successfully ingested {total_ingested} relationships into Neo4j.")

if __name__ == "__main__":
    build_relationships_cuda()