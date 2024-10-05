import os
import xmltodict
import json
from dotenv import load_dotenv
import uuid
from tqdm import tqdm

# Load environment variables
load_dotenv()

EXTRACT_DIR = "data/processed/irc"
JSON_DIR = "data/processed/irc/json"

def parse_xml_to_json(xml_file):
    """
    Parses the XML file using xmltodict and converts it to a JSON-like structure.
    """
    try:
        with open(xml_file, 'rb') as f:
            doc = xmltodict.parse(f)
        
        # Navigate to sections - adjust based on actual XML structure
        sections = doc.get('uscDoc', {}).get('sections', {}).get('section', [])
        
        title_data = {"sections": []}
        
        for section in sections:
            section_id = section.get('@id', '')
            heading = section.get('heading', '')
            content = section.get('p', '')

            # Generate a unique ID if missing
            if not section_id:
                section_id = str(uuid.uuid4())
            
            section_data = {
                "id": section_id,
                "heading": heading,
                "content": content
            }
            title_data["sections"].append(section_data)
        
        return title_data

    except Exception as e:
        print(f"Error parsing XML file {xml_file}: {e}")
        return None

def convert_all_xml_to_json():
    """
    Converts all XML files in the extracted directory to JSON using xmltodict.
    """
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
    
    xml_files = [os.path.join(EXTRACT_DIR, f) for f in os.listdir(EXTRACT_DIR) if f.endswith(".xml")]
    total_files = len(xml_files)
    print(f"Total XML files to convert: {total_files}")

    for xml_file in tqdm(xml_files, desc="Converting XML to JSON"):
        json_data = parse_xml_to_json(xml_file)
        if json_data and json_data["sections"]:
            json_filename = os.path.splitext(os.path.basename(xml_file))[0] + ".json"
            json_file_path = os.path.join(JSON_DIR, json_filename)
            with open(json_file_path, 'w', encoding='utf-8') as jf:
                json.dump(json_data, jf, indent=4)
            # Optionally, move processed files to another directory
        else:
            print(f"No sections found in {xml_file}, skipping JSON conversion.")

if __name__ == "__main__":
    convert_all_xml_to_json()