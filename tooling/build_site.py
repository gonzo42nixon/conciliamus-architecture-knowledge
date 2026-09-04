import os, json, re, yaml

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, "knowledge")
GRAPH_PATH = os.path.join(ROOT_DIR, "graph", "knowledge-graph.json")
SITE_PATH = os.path.join(ROOT_DIR, "site", "index.html")

print("Generator script template ready")
