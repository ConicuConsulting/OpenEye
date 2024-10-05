import os
import xml.etree.ElementTree as ET
import json

EXTRACT_DIR = "data/processed/irc"
JSON_DIR = "data/processed/irc/json"

def parse_xml_to_json(xml_file):
    """
    Parses the XML file and converts it to a JSON-like structure.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Extract namespace
        namespace = {'ns': root.tag.split('}')[0].strip('{')}

        title_data = {
            "sections": []
        }

        # Adjust the XPath based on the actual XML structure
        for section in root.findall(".//ns:section", namespace):
            section_id = section.attrib.get("id", "")
            heading = section.findtext("ns:heading", default="", namespaces=namespace)
            content = section.findtext("ns:p", default="", namespaces=namespace)

            section_data = {
                "id": section_id,
                "heading": heading,
                "content": content
            }
            title_data["sections"].append(section_data)

        return title_data

    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_file}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error parsing XML file {xml_file}: {e}")
        return None

def convert_all_xml_to_json():
    """
    Converts all XML files in the extracted directory to JSON.
    """
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

    for file_name in os.listdir(EXTRACT_DIR):
        if file_name.endswith(".xml"):
            xml_file = os.path.join(EXTRACT_DIR, file_name)
            json_data = parse_xml_to_json(xml_file)

            if json_data:
                json_filename = os.path.splitext(file_name)[0] + ".json"
                json_file_path = os.path.join(JSON_DIR, json_filename)
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, indent=4)
                print(f"Converted {file_name} to {json_filename}")
            else:
                print(f"Failed to convert {file_name}")

if __name__ == "__main__":
    convert_all_xml_to_json()