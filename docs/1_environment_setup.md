Here’s a Python script that will set up the project structure, create the necessary directories and files, and include starter content for your scripts and configurations based on what we discussed.

Save this script as `setup_project.py` and run it to set up the **OpenEye** project structure:

```python
import os

# Define the project structure
project_structure = {
    "data": {
        "raw": {
            "irc": {}
        },
        "processed": {
            "irc": {}
        },
        "references": {
            "federal": {},
            "state": {}
        }
    },
    "scripts": {
        "parse_xml.py": """import os
import json
from bs4 import BeautifulSoup

# Define your parsing logic here
# Example parse logic
def parse_title_xml(title_number):
    pass
""",
        "extract_references.py": """import os
import re

# Define your reference extraction logic here
def extract_references(title_number):
    pass
""",
        "ingest_to_neo4j.py": """from py2neo import Graph, Node, Relationship

# Neo4j ingestion script
def ingest_titles(graph):
    pass

def ingest_references(graph):
    pass
""",
        "visualize_graph.py": """import networkx as nx
import matplotlib.pyplot as plt

# Define your visualization logic here
def visualize(G):
    pass
"""
    },
    "src": {
        "database": {
            "setup_neo4j.sh": """#!/bin/bash
# Script to set up Neo4j using Docker
docker run \\
    --name openeye-neo4j \\
    -p7474:7474 -p7687:7687 \\
    -d \\
    -e NEO4J_AUTH=neo4j/your_password \\
    neo4j:latest
""",
            "schema.cypher": """CREATE CONSTRAINT ON (t:Title) ASSERT t.title_number IS UNIQUE;
CREATE CONSTRAINT ON (s:Section) ASSERT s.id IS UNIQUE;

// Example node creation
CREATE (t1:Title {title_number: 1, name: "GENERAL PROVISIONS"});
"""
        },
        "utils": {
            "config.py": """import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
"""
        }
    },
    "tests": {
        "test_parse_xml.py": "# Test parse_xml.py",
        "test_extract_references.py": "# Test extract_references.py",
        "test_ingest_to_neo4j.py": "# Test ingest_to_neo4j.py"
    },
    ".env.example": """# Example .env file
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
""",
    "requirements.txt": """beautifulsoup4
lxml
spaCy
networkx
py2neo
matplotlib
dotenv
"""
}

# Function to create directories and files
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)  # Recurse into subdirectory
        else:
            # Create file and write content
            with open(path, 'w') as file:
                file.write(content)

# Set base directory as the current project directory
base_dir = os.getcwd()

# Create the project structure
create_structure(base_dir, project_structure)

print("Project structure created successfully!")
```

### Steps to Run:
1. **Save the script** as `setup_project.py` in your project directory.
   
   For example, if your project directory is:
   ```bash
   ~/projects/OpenEye
   ```
   save it as:
   ```bash
   ~/projects/OpenEye/setup_project.py
   ```

2. **Run the script** to create the entire project structure:

   In your terminal, navigate to the **OpenEye** directory and run:
   ```bash
   python setup_project.py
   ```

### Resulting Project Structure:
After running the script, your project directory should now look like this:

```bash
.
├── LICENSE
├── README.md
├── requirements.txt
├── data
│   ├── processed
│   │   └── irc
│   └── raw
│       └── irc
├── scripts
│   ├── extract_references.py
│   ├── ingest_to_neo4j.py
│   ├── parse_xml.py
│   └── visualize_graph.py
├── src
│   ├── database
│   │   ├── schema.cypher
│   │   └── setup_neo4j.sh
│   └── utils
│       └── config.py
├── tests
│   ├── test_extract_references.py
│   ├── test_ingest_to_neo4j.py
│   └── test_parse_xml.py
└── .env.example
```

### What's Included:
- **Data Directory**: For storing raw and processed IRC documents.
- **Scripts**:
  - `parse_xml.py`: For parsing XML documents.
  - `extract_references.py`: For extracting references between sections.
  - `ingest_to_neo4j.py`: For loading data into Neo4j.
  - `visualize_graph.py`: For visualizing the relationships.
- **src Directory**: For configuration and utility scripts, and the database schema and setup scripts.
- **Tests Directory**: Placeholder unit test files.
- **`.env.example`**: Example file to manage environment variables.
- **`requirements.txt`**: Lists the necessary Python packages.

### Next Steps:
1. **Install the dependencies** by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Neo4j**:
   - Use the `setup_neo4j.sh` script in `src/database/` to launch a Neo4j container or set up Neo4j Desktop.

3. **Edit the scripts** (e.g., `parse_xml.py`, `ingest_to_neo4j.py`, etc.) to implement your logic.

4. **Run the scripts** and test the functionality.

---

This script should help you hit the ground running with your **OpenEye** project by setting up everything you need in one go. Let me know if you need any further adjustments!
