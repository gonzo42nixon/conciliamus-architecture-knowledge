#!/usr/bin/env python3
"""
Conciliamus Architecture Knowledge API Server:
FastAPI-Server zur Bereitstellung der OpenAPI-Schnittstelle für API- und LLM-Agenten.
"""
import os
import sys
import re
import json
from typing import Optional, List, Dict, Any
import yaml
from fastapi import FastAPI, HTTPException, Query, Path, Request
from fastapi.responses import HTMLResponse, Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, "knowledge")
GRAPH_PATH = os.path.join(ROOT_DIR, "graph", "knowledge-graph.json")
SITE_DIR = os.path.join(ROOT_DIR, "site")
INDEX_HTML_PATH = os.path.join(SITE_DIR, "index.html")
API_DIR = os.path.join(ROOT_DIR, "api")
RUNTIME_OPENAPI_PATH = os.path.join(API_DIR, "conciliamus-runtime-iflows.openapi.yaml")
KNOWLEDGE_OPENAPI_PATH = os.path.join(API_DIR, "conciliamus-architecture.openapi.yaml")

FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

app = FastAPI(
    title="Conciliamus Architecture Knowledge API",
    version="1.0.0",
    description="API-Schnittstelle zur Abfrage von Architekturkonzepten, iFlow-Spezifikationen, ADRs und Testnachweisen im Google Open Knowledge Format (OKF v0.2).",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ConceptSummary(BaseModel):
    id: str
    title: str
    type: str
    path: str
    description: Optional[str] = ""
    tags: List[str] = []

class ConceptDetail(BaseModel):
    id: str
    frontmatter: Dict[str, Any]
    content: str

class VerifyRuleRequest(BaseModel):
    proposedDesign: str
    context: str

class VerifyRuleResponse(BaseModel):
    compliant: bool
    ruleViolations: List[str] = []
    applicableDecisions: List[str] = []
    recommendation: str

class ChatQueryRequest(BaseModel):
    question: str

class ChatQueryResponse(BaseModel):
    question: str
    primaryConcept: Optional[ConceptSummary] = None
    answer: str
    relations: List[Dict[str, Any]] = []
    sources: List[Dict[str, Any]] = []
    trustTier: str = "VERIFIED"

# Helper to load concepts
def load_all_concepts_data():
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
                    body = text[match.end():].strip()
                    cid = fm.get("id") or rel_path.lstrip("/").replace(".md", "")
                    concepts.append({
                        "id": cid,
                        "path": rel_path,
                        "frontmatter": fm,
                        "content": body,
                        "fullText": (fm.get("title", "") + " " + fm.get("description", "") + " " + body).lower()
                    })
    return concepts

@app.get("/", tags=["Info"])
def root_info():
    return {
        "title": "Conciliamus Architecture Knowledge API",
        "standard": "Google Open Knowledge Format (OKF v0.2)",
        "graphViewerUrl": "/graph",
        "obsidianViewerUrl": "/obsidian",
        "obsidianVaultPath": ROOT_DIR,
        "docsUrl": "/docs",
        "redocUrl": "/redoc",
        "status": "ready"
    }

@app.get("/concepts", response_model=List[ConceptSummary], tags=["Concepts"])
def search_concepts(
    q: Optional[str] = Query(None, description="Suchbegriff oder semantische Frage"),
    type: Optional[str] = Query(None, description="Filter nach OKF-Typ"),
    tag: Optional[str] = Query(None, description="Filter nach Schlagwort")
):
    concepts = load_all_concepts_data()
    results = []

    keywords = [w.lower() for w in re.findall(r"\w+", q)] if q else []

    for c in concepts:
        fm = c["frontmatter"]
        
        # Type filter
        if type and fm.get("type", "").lower() != type.lower():
            continue
            
        # Tag filter
        if tag and tag.lower() not in [t.lower() for t in fm.get("tags", [])]:
            continue

        # Text search
        if keywords:
            matches = any(kw in c["fullText"] for kw in keywords)
            if not matches:
                continue

        results.append(ConceptSummary(
            id=c["id"],
            title=fm.get("title", c["id"]),
            type=fm.get("type", "Concept"),
            path=c["path"],
            description=fm.get("description", ""),
            tags=fm.get("tags", [])
        ))

    return results

@app.get("/concepts/{concept_id:path}", response_model=ConceptDetail, tags=["Concepts"])
def get_concept(concept_id: str = Path(..., description="ID oder Pfad des Konzepts")):
    clean_id = concept_id.lstrip("/").replace(".md", "")
    concepts = load_all_concepts_data()
    for c in concepts:
        if c["id"] == clean_id or c["path"].lstrip("/").replace(".md", "") == clean_id:
            return ConceptDetail(
                id=c["id"],
                frontmatter=c["frontmatter"],
                content=c["content"]
            )
    raise HTTPException(status_code=404, detail=f"Konzept '{concept_id}' nicht im OKF-Bundle gefunden.")

@app.get("/decisions/{adr_number}", tags=["Decisions"])
def get_decision_record(adr_number: str):
    norm_number = adr_number.lower().replace("_", "-")
    concepts = load_all_concepts_data()
    for c in concepts:
        if norm_number in c["id"].lower() and c["frontmatter"].get("type") == "Decision Record":
            return {
                "adrId": c["frontmatter"].get("id"),
                "title": c["frontmatter"].get("title"),
                "status": c["frontmatter"].get("status"),
                "frontmatter": c["frontmatter"],
                "content": c["content"]
            }
    raise HTTPException(status_code=404, detail=f"Architecture Decision Record '{adr_number}' nicht gefunden.")

@app.get("/graph", tags=["Knowledge Graph"])
def get_knowledge_graph(
    request: Request,
    focusNode: Optional[str] = Query(None, description="Ausgangsknoten"),
    depth: int = Query(2, ge=1, le=5),
    format: Optional[str] = Query(None, description="Format ('html' oder 'json')")
):
    accept = request.headers.get("accept", "")
    is_browser = "text/html" in accept and "application/json" not in accept
    if format == "html" or (is_browser and format != "json"):
        if os.path.exists(INDEX_HTML_PATH):
            with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())

    if not os.path.exists(GRAPH_PATH):
        raise HTTPException(status_code=500, detail="knowledge-graph.json nicht generiert. Bitte tooling/build_graph.py ausführen.")
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)

    if not focusNode:
        return graph

    # Filter subgraph around focusNode
    visited_nodes = {focusNode}
    current_frontier = {focusNode}
    collected_edges = []

    for _ in range(depth):
        next_frontier = set()
        for edge in graph.get("edges", []):
            if edge["source"] in current_frontier or edge["target"] in current_frontier:
                collected_edges.append(edge)
                visited_nodes.add(edge["source"])
                visited_nodes.add(edge["target"])
                next_frontier.add(edge["source"])
                next_frontier.add(edge["target"])
        current_frontier = next_frontier

    filtered_nodes = [n for n in graph.get("nodes", []) if n["id"] in visited_nodes]
    return {
        "okfVersion": "0.2",
        "focusNode": focusNode,
        "nodesCount": len(filtered_nodes),
        "edgesCount": len(collected_edges),
        "nodes": filtered_nodes,
        "edges": collected_edges
    }

@app.get("/obsidian", response_class=HTMLResponse, tags=["Obsidian Graph"])
@app.get("/view", response_class=HTMLResponse, tags=["Obsidian Graph"])
def view_obsidian_workspace():
    if not os.path.exists(INDEX_HTML_PATH):
        raise HTTPException(status_code=404, detail="site/index.html nicht gefunden.")
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
    svg_icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">💎</text></svg>'
    return Response(content=svg_icon, media_type="image/svg+xml")

@app.get("/app.js", include_in_schema=False)
@app.get("/site/app.js", include_in_schema=False)
def serve_app_js():
    js_path = os.path.join(SITE_DIR, "app.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="app.js nicht gefunden.")

@app.get("/specs/runtime-iflows.yaml", tags=["Specifications"])
def get_runtime_iflows_spec():
    if os.path.exists(RUNTIME_OPENAPI_PATH):
        return FileResponse(RUNTIME_OPENAPI_PATH, media_type="application/yaml", filename="conciliamus-runtime-iflows.openapi.yaml")
    raise HTTPException(status_code=404, detail="conciliamus-runtime-iflows.openapi.yaml nicht gefunden.")

@app.get("/specs/knowledge-api.yaml", tags=["Specifications"])
def get_knowledge_api_spec():
    if os.path.exists(KNOWLEDGE_OPENAPI_PATH):
        return FileResponse(KNOWLEDGE_OPENAPI_PATH, media_type="application/yaml", filename="conciliamus-architecture.openapi.yaml")
    raise HTTPException(status_code=404, detail="conciliamus-architecture.openapi.yaml nicht gefunden.")

@app.get("/docs/iflows", response_class=HTMLResponse, tags=["Specifications"])
def view_iflows_swagger():
    return HTMLResponse(content="""<!DOCTYPE html>
<html>
<head>
  <title>Conciliamus iFlow Runtime API - Swagger UI</title>
  <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.ico">
</head>
<body style="margin:0; background:#fafafa;">
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: '/specs/runtime-iflows.yaml',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ]
      });
    };
  </script>
</body>
</html>""")

@app.post("/rules/verify", response_model=VerifyRuleResponse, tags=["Architecture Rules"])
def verify_architecture_rule(req: VerifyRuleRequest):
    p_lower = req.proposedDesign.lower()
    violations = []
    adrs = []

    if "monolith" in p_lower or ("ein" in p_lower and "iflow" in p_lower and "beide" in p_lower):
        violations.append("Verstoß gegen Dual-iFlow Entkopplungsmuster: Transport und fachliche Verarbeitung müssen getrennt sein.")
        adrs.append("ADR-001: Dual-iFlow Entkopplungsmuster")

    if "jms" in p_lower or "queue" in p_lower:
        violations.append("Hinweis: Nach ADR-002 ist für tenant-interne Kopplung ProcessDirect zu bevorzugen, um Latenz und Kosten zu minimieren.")
        adrs.append("ADR-002: ProcessDirect statt Message Queues")

    if "statisch" in p_lower and "id" in p_lower:
        violations.append("Verstoß gegen dynamische OData-Adressierung: BusinessPartner-ID muss dynamisch aus dem OData GET ermittelt werden.")

    compliant = len(violations) == 0
    rec = "Entwurf entspricht den Architekturrichtlinien." if compliant else "Bitte passen Sie den Entwurf gemäß den genannten ADRs an."

    return VerifyRuleResponse(
        compliant=compliant,
        ruleViolations=violations,
        applicableDecisions=adrs,
        recommendation=rec
    )

@app.post("/chat", response_model=ChatQueryResponse, tags=["Agent Chat"])
def agent_chat_query(req: ChatQueryRequest):
    concepts = load_all_concepts_data()
    keywords = [w.lower() for w in re.findall(r"\w+", req.question) if len(w) > 2]

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
    if not scored:
        return ChatQueryResponse(
            question=req.question,
            answer="Zu dieser Frage liegen im kuratierten OKF-Wissensbundle keine hinreichend spezifischen Fakten vor.",
            trustTier="UNKNOWN"
        )

    best = scored[0][1]
    fm = best["frontmatter"]
    summary = ConceptSummary(
        id=best["id"],
        title=fm.get("title", best["id"]),
        type=fm.get("type", "Concept"),
        path=best["path"],
        description=fm.get("description", ""),
        tags=fm.get("tags", [])
    )

    paragraphs = [p.strip() for p in best["content"].split("\n\n") if p.strip() and not p.startswith("#")]
    extracted_answer = "\n\n".join(paragraphs[:2]) if paragraphs else fm.get("description", "")

    return ChatQueryResponse(
        question=req.question,
        primaryConcept=summary,
        answer=extracted_answer,
        relations=fm.get("relations", []),
        sources=fm.get("sources", []),
        trustTier=fm.get("status", "VERIFIED").upper()
    )

if __name__ == "__main__":
    import uvicorn
    print("[API Server] Starte Conciliamus Architecture Knowledge API auf http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
