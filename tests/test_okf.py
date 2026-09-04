import os
import re
import json
import yaml
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, "knowledge")
GRAPH_PATH = os.path.join(ROOT_DIR, "graph", "knowledge-graph.json")
MANIFEST_PATH = os.path.join(ROOT_DIR, "manifest", "agent.yaml")

FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
MARKDOWN_LINK_REGEX = re.compile(r"\[([^\]]+)\]\((/[^)]+)\)")

def get_all_markdown_files():
    files_map = {}
    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = "/" + os.path.relpath(full_path, KNOWLEDGE_DIR).replace("\\", "/")
                files_map[rel_path] = full_path
    return files_map

def test_all_documents_have_valid_frontmatter():
    files_map = get_all_markdown_files()
    assert len(files_map) >= 25, f"Erwartet mindestens 25 OKF-Dokumente, gefunden: {len(files_map)}"

    for rel_path, full_path in files_map.items():
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read().replace("\r\n", "\n")

        match = FRONTMATTER_REGEX.match(content)
        assert match is not None, f"Kein gültiges Frontmatter in {rel_path}"

        fm = yaml.safe_load(match.group(1))
        assert isinstance(fm, dict), f"Frontmatter ist kein Mapping in {rel_path}"

        if rel_path == "/index.md":
            assert fm.get("okf_version") == "0.2", f"okf_version fehlt in index.md"
        else:
            concept_type = fm.get("type")
            assert concept_type is not None and str(concept_type).strip() != "", f"Obligatorisches OKF-Feld 'type' fehlt in {rel_path}"
            assert "title" in fm and str(fm["title"]).strip() != "", f"Titel fehlt in {rel_path}"

def test_all_markdown_links_resolve():
    files_map = get_all_markdown_files()

    for rel_path, full_path in files_map.items():
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read().replace("\r\n", "\n")

        match = FRONTMATTER_REGEX.match(content)
        body = content[match.end():] if match else content

        for text, link in MARKDOWN_LINK_REGEX.findall(body):
            clean_link = link.split("#")[0]
            assert clean_link in files_map, f"Toter Link '{link}' in {rel_path}"

def test_knowledge_graph_structure():
    assert os.path.exists(GRAPH_PATH), "knowledge-graph.json existiert nicht"
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)

    assert graph.get("okfVersion") == "0.2"
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    assert len(nodes) >= 20, f"Zu wenige Knoten: {len(nodes)}"
    assert len(edges) >= 40, f"Zu wenige Kanten: {len(edges)}"

    node_ids = {n["id"] for n in nodes}
    for edge in edges:
        assert edge["source"] in node_ids, f"Kante hat unbekannte Source: {edge['source']}"
        assert edge["target"] in node_ids, f"Kante hat unbekanntes Target: {edge['target']}"
        assert "relation" in edge and edge["relation"], f"Kante fehlt Relationstyp"

def test_agent_manifest_validity():
    assert os.path.exists(MANIFEST_PATH), "manifest/agent.yaml fehlt"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    assert manifest.get("kind") == "KnowledgeAgent"
    assert "spec" in manifest
    assert manifest["spec"]["knowledge"]["okfVersion"] == "0.2"
    assert manifest["spec"]["retrieval"]["startAt"] == "index.md"
