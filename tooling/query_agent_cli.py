#!/usr/bin/env python3
"""
Architecture Agent CLI Prototype:
Simuliert die Abfragebeantwortung durch den API-Architektur-Agenten auf Basis des OKF-Bundles.
"""
import os
import sys
import re
import yaml

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, "knowledge")

FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def load_all_concepts():
    concepts = []
    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            if file.endswith(".md") and file != "index.md":
                full_path = os.path.join(root, file)
                rel_path = "/" + os.path.relpath(full_path, KNOWLEDGE_DIR).replace("\\", "/")
                with open(full_path, "r", encoding="utf-8") as f:
                    text = f.read().replace("\r\n", "\n")
                match = FRONTMATTER_REGEX.match(text)
                if match:
                    fm = yaml.safe_load(match.group(1)) or {}
                    body = text[match.end():]
                    concepts.append({
                        "path": rel_path,
                        "frontmatter": fm,
                        "body": body,
                        "fullText": (fm.get("title", "") + " " + fm.get("description", "") + " " + body).lower()
                    })
    return concepts

def query_agent(question):
    print(f"\n=======================================================")
    print(f"[AGENT] Conciliamus Architecture Advisor Agent (OKF v0.2)")
    print(f"[QUERY] Frage: \"{question}\"")
    print(f"=======================================================\n")

    concepts = load_all_concepts()
    keywords = [w.lower() for w in re.findall(r"\w+", question) if len(w) > 2]
    
    scored = []
    for c in concepts:
        score = 0
        for kw in keywords:
            score += c["fullText"].count(kw)
            if kw in c["frontmatter"].get("title", "").lower():
                score += 5
            if kw in [t.lower() for t in c["frontmatter"].get("tags", [])]:
                score += 3
        if score > 0:
            scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_matches = [c for _, c in scored[:3]]

    if not top_matches:
        print("Entschuldigung, zu dieser Fragestellung konnten im kuratierten OKF-Wissensbundle keine hinreichend spezifischen Fakten identifiziert werden.")
        return

    primary = top_matches[0]
    fm = primary["frontmatter"]
    print(f"[RESULT] Primäres Konzept: {fm.get('title')} ({fm.get('type')})")
    print(f"[SUMMARY] Zusammenfassung:  {fm.get('description')}\n")
    print("--- Wesentliche Architekturaussage ---")
    
    paragraphs = [p.strip() for p in primary["body"].split("\n\n") if p.strip() and not p.startswith("#")]
    for p in paragraphs[:2]:
        print(p)
        print()

    print("--- Verknüpfte Relationen & Quellen ---")
    for rel in fm.get("relations", []):
        print(f"  * [{rel.get('type')}] -> {rel.get('target')}")
    for src in fm.get("sources", []):
        print(f"  * Quelle: {src.get('title')} ({src.get('resource', 'n/a')})")
    print(f"\nVertrauensstufe: {fm.get('status', 'verified').upper()} | Generator: {fm.get('generated', {}).get('by', 'human:expert')}")

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Warum wurde ein Dual-iFlow Entwurfsmuster gewählt?"
    query_agent(q)
