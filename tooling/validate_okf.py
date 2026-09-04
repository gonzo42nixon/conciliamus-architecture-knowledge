#!/usr/bin/env python3
"""
OKF Validator: Validiert das Google Open Knowledge Format (OKF v0.2) Bundle.
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
MARKDOWN_LINK_REGEX = re.compile(r"\[([^\]]+)\]\((/[^)]+)\)")

def validate_bundle():
    print(f"[OKF Validator] Starte Validierung in: {KNOWLEDGE_DIR}")
    errors = []
    concept_count = 0

    all_files = {}
    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = "/" + os.path.relpath(full_path, KNOWLEDGE_DIR).replace("\\", "/")
                all_files[rel_path] = full_path

    for rel_path, full_path in all_files.items():
        concept_count += 1
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read().replace("\r\n", "\n")

        match = FRONTMATTER_REGEX.match(content)
        if not match:
            errors.append(f"FEHLER: Kein gültiges YAML-Frontmatter gefunden in: {rel_path}")
            continue

        fm_text = match.group(1)
        try:
            frontmatter = yaml.safe_load(fm_text) or {}
        except Exception as e:
            errors.append(f"FEHLER: YAML-Parsing-Fehler in {rel_path}: {e}")
            continue

        # Check okf_version on root index
        if rel_path == "/index.md":
            if "okf_version" not in frontmatter:
                errors.append("FEHLER: 'okf_version' fehlt in knowledge/index.md")
            continue

        # Obligatorisches OKF-Feld: type
        if "type" not in frontmatter or not str(frontmatter.get("type", "")).strip():
            errors.append(f"FEHLER: Obligatorisches Feld 'type' fehlt oder ist leer in: {rel_path}")

        # Prüfe Relationen
        relations = frontmatter.get("relations", [])
        for rel in relations:
            target = rel.get("target")
            if target and target not in all_files:
                errors.append(f"FEHLER: Ungültiges Relations-Ziel '{target}' in {rel_path}")

        # Prüfe Markdown Links
        body = content[match.end():]
        for link_text, link_target in MARKDOWN_LINK_REGEX.findall(body):
            target_clean = link_target.split("#")[0]
            if target_clean and target_clean not in all_files:
                errors.append(f"FEHLER: Toter Markdown-Link '{link_target}' in {rel_path}")

    print(f"[OKF Validator] Geprüfte Dokumente: {concept_count}")
    if errors:
        print(f"\n[OKF Validator] [FAIL] {len(errors)} FEHLER GEFUNDEN:")
        for err in errors:
            print("  -", err)
        return False
    else:
        print("\n[OKF Validator] [PASS] Alle OKF v0.2 Dokumente sind 100% valide und konsistent!")
        return True

if __name__ == "__main__":
    success = validate_bundle()
    sys.exit(0 if success else 1)
