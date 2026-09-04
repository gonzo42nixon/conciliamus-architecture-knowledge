#!/usr/bin/env python3
"""
Graph Builder: Generiert maschinenlesbare Knowledge Graph Artefakte
(knowledge-graph.json und architecture-graph.mmd) aus den OKF-Markdown-Konzepten.
"""
import os
import sys
import json
import re
import yaml

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, "knowledge")
GRAPH_DIR = os.path.join(ROOT_DIR, "graph")

FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def build():
    nodes = []
    edges = []
    node_map = {}

    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            if file.endswith(".md") and file != "index.md":
                full_path = os.path.join(root, file)
                rel_path = "/" + os.path.relpath(full_path, KNOWLEDGE_DIR).replace("\\", "/")
                
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read().replace("\r\n", "\n")

                match = FRONTMATTER_REGEX.match(content)
                if not match:
                    continue

                fm = yaml.safe_load(match.group(1)) or {}
                node_id = fm.get("id") or rel_path.lstrip("/").replace(".md", "")
                title = fm.get("title", file)
                node_type = fm.get("type", "Concept")
                tags = fm.get("tags", [])

                node = {
                    "id": node_id,
                    "label": title,
                    "type": node_type,
                    "path": rel_path,
                    "tags": tags
                }
                nodes.append(node)
                node_map[rel_path] = node_id

    # Kanten sammeln
    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            if file.endswith(".md") and file != "index.md":
                full_path = os.path.join(root, file)
                rel_path = "/" + os.path.relpath(full_path, KNOWLEDGE_DIR).replace("\\", "/")
                source_id = node_map.get(rel_path)

                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read().replace("\r\n", "\n")

                match = FRONTMATTER_REGEX.match(content)
                if not match:
                    continue

                fm = yaml.safe_load(match.group(1)) or {}
                relations = fm.get("relations", [])
                for rel in relations:
                    target_path = rel.get("target")
                    target_id = node_map.get(target_path)
                    if target_id and source_id:
                        edges.append({
                            "source": source_id,
                            "target": target_id,
                            "relation": rel.get("type", "references")
                        })

    # JSON export
    graph_data = {
        "okfVersion": "0.2",
        "nodesCount": len(nodes),
        "edgesCount": len(edges),
        "nodes": nodes,
        "edges": edges
    }

    json_path = os.path.join(GRAPH_DIR, "knowledge-graph.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    print(f"[Graph Builder] {len(nodes)} Knoten und {len(edges)} Kanten exportiert nach: {json_path}")

    # Mermaid export
    mmd_lines = ["graph TD", "  %% Conciliamus OKF Architecture Knowledge Graph"]
    def clean_id(raw):
        return raw.replace("/", "_").replace("-", "_")

    for node in nodes:
        cid = clean_id(node["id"])
        escaped_label = node["label"].replace('"', "'")
        mmd_lines.append(f'  {cid}["{escaped_label}<br/><i>{node["type"]}</i>"]')

    for edge in edges:
        s = clean_id(edge["source"])
        t = clean_id(edge["target"])
        rel = edge["relation"]
        mmd_lines.append(f"  {s} -->|{rel}| {t}")

    mmd_path = os.path.join(GRAPH_DIR, "architecture-graph.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write("\n".join(mmd_lines) + "\n")
    print(f"[Graph Builder] Mermaid-Diagramm exportiert nach: {mmd_path}")

if __name__ == "__main__":
    build()
