"""
Conciliamus AI Advisor - Streamlit Web Application
Powered by Google AI Studio (Gemini API) and Google Open Knowledge Format (OKF v0.2).
Zero-Docker, Serverless Deployment on Streamlit Community Cloud.
"""
import os
import re
import json
import yaml
import base64
from pathlib import Path
from typing import List, Dict, Any, Tuple
import time
import streamlit as st
import streamlit.components.v1 as components

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
KNOWLEDGE_DIR = ROOT_DIR / "knowledge"
GRAPH_PATH = ROOT_DIR / "graph" / "knowledge-graph.json"
MANIFEST_PATH = ROOT_DIR / "manifest" / "agent.yaml"
PECHA_HTML_PATH = ROOT_DIR / "site" / "pecha_kucha_presentation.html"
PECHA_KONZEPT_PATH = ROOT_DIR / "knowledge" / "presentation-and-ui" / "pecha_kucha_konzept.md"
TEST_RUNNER_HTML_PATH = ROOT_DIR / "site" / "test-runner.html"
ISTQB_STRATEGY_PATH = ROOT_DIR / "knowledge" / "verification" / "istqb-test-strategy.md"
TESTDATA_DIR = ROOT_DIR / "testdata"

def get_advisor_logo_base64() -> str:
    """Returns the base64-encoded IT-Advisor logo (ki_advisor_icon.png) for 100% reliable rendering."""
    for loc in [ROOT_DIR / "site" / "ki_advisor_icon.png", ROOT_DIR / "ki_advisor_icon.png"]:
        if loc.exists():
            try:
                with open(loc, "rb") as f:
                    return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return "https://lh3.googleusercontent.com/pw/AP1GczNopyl_jUGFG9Gii9MaQ1JyjPm72_iN1oLV9XlPyzkwW8HYB_Oj_hSb3D1AgGWh0bVPsTetLYwQjXvaL1I4yMyL1F06XymmtBnWpoX8SzW8eqshuNnD=s0"

def execute_cpi_live_test(payload_str: str, creds: Dict[str, str]) -> Dict[str, Any]:
    """Executes a real live batch test against SAP Cloud Integration tenant."""
    import urllib.request
    import urllib.parse
    import urllib.error
    import http.cookiejar
    import base64
    import time

    start_time = time.time()
    audit_log = []

    token_url = creds.get("token_url", "").strip()
    runtime_url = creds.get("runtime_url", "").strip()
    client_id = creds.get("client_id", "").strip()
    client_secret = creds.get("client_secret", "").strip()

    if not client_id or not client_secret or not token_url or not runtime_url:
        return {
            "success": False,
            "status": 0,
            "error": "BTP Anmeldedaten unvollständig. Bitte Client-ID, Secret, Token-URL und Runtime-URL prüfen.",
            "duration": 0,
            "audit_log": ["[-] Fehler: Unvollständige BTP Anmeldedaten."]
        }

    # Step 1: OAuth2 Token
    audit_log.append(f"[*] Anforderung OAuth2-Token von: {token_url}")
    token_start = time.time()
    try:
        data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
        auth_bytes = f"{client_id}:{client_secret}".encode("utf-8")
        auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

        req = urllib.request.Request(token_url, data=data, method="POST")
        req.add_header("Authorization", f"Basic {auth_b64}")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        with urllib.request.urlopen(req, timeout=15) as resp:
            token_res = json.loads(resp.read().decode("utf-8"))
            token = token_res.get("access_token")
            expires_in = token_res.get("expires_in")
            audit_log.append(f"[+] Token erhalten ({time.time() - token_start:.2f}s): Type={token_res.get('token_type')}, Scope=ESBMessaging.send, ExpiresIn={expires_in}s")
    except Exception as e:
        audit_log.append(f"[-] Token-Fehler: {str(e)}")
        return {
            "success": False,
            "status": 401,
            "error": f"OAuth2 Token-Anforderung fehlgeschlagen: {str(e)}",
            "duration": round(time.time() - start_time, 2),
            "audit_log": audit_log
        }

    # Step 2: CSRF Handshake
    endpoint = f"{runtime_url.rstrip('/')}/http/conciliamus/v1/businesspartners/batch"
    audit_log.append(f"[*] Führe CSRF-Handshake durch an: {endpoint}")
    csrf_start = time.time()

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    req1 = urllib.request.Request(endpoint, method="GET")
    req1.add_header("Authorization", f"Bearer {token}")
    req1.add_header("X-CSRF-Token", "Fetch")

    csrf_token = None
    try:
        resp1 = opener.open(req1, timeout=15)
        csrf_token = resp1.headers.get("X-CSRF-Token")
        audit_log.append(f"[+] CSRF-Token erhalten ({time.time() - csrf_start:.2f}s): {csrf_token}")
    except urllib.error.HTTPError as e:
        csrf_token = e.headers.get("X-CSRF-Token")
        if csrf_token:
            audit_log.append(f"[+] CSRF-Token aus Fehler-Header extrahiert ({time.time() - csrf_start:.2f}s): {csrf_token}")
        else:
            audit_log.append(f"[-] CSRF-Fehler (HTTP {e.code}): {str(e)}")
            return {
                "success": False,
                "status": e.code,
                "error": f"CSRF-Handshake fehlgeschlagen: {str(e)}",
                "duration": round(time.time() - start_time, 2),
                "audit_log": audit_log
            }
    except Exception as e:
        audit_log.append(f"[-] CSRF-Verbindungsfehler: {str(e)}")
        return {
            "success": False,
            "status": 500,
            "error": f"CSRF-Verbindung fehlgeschlagen: {str(e)}",
            "duration": round(time.time() - start_time, 2),
            "audit_log": audit_log
        }

    # Step 3: Send Batch POST
    audit_log.append(f"[*] Sende Batch-Payload an: {endpoint}")
    post_start = time.time()
    try:
        post_data = payload_str.encode("utf-8")
        req2 = urllib.request.Request(endpoint, data=post_data, method="POST")
        req2.add_header("Authorization", f"Bearer {token}")
        req2.add_header("Content-Type", "application/json")
        req2.add_header("Accept", "application/json")
        if csrf_token:
            req2.add_header("X-CSRF-Token", csrf_token)

        resp2 = opener.open(req2, timeout=30)
        resp_body = resp2.read().decode("utf-8")
        duration = round(time.time() - start_time, 2)
        sap_msg_id = resp2.headers.get("SAP_MessageProcessingLogID", "N/A")

        audit_log.append(f"[+] Batch erfolgreich verarbeitet ({time.time() - post_start:.2f}s)! HTTP Status: {resp2.status}")
        if sap_msg_id != "N/A":
            audit_log.append(f"[+] SAP Message Processing Log ID: {sap_msg_id}")

        return {
            "success": True,
            "status": resp2.status,
            "duration": duration,
            "body": resp_body,
            "sap_message_id": sap_msg_id,
            "audit_log": audit_log
        }
    except urllib.error.HTTPError as e:
        duration = round(time.time() - start_time, 2)
        err_body = e.read().decode("utf-8", errors="replace")
        audit_log.append(f"[-] Übertragungsfehler (HTTP {e.code}): {e.reason}")
        return {
            "success": False,
            "status": e.code,
            "duration": duration,
            "body": err_body,
            "error": f"HTTP {e.code} {e.reason}",
            "headers": dict(e.headers),
            "audit_log": audit_log
        }
    except Exception as e:
        duration = round(time.time() - start_time, 2)
        audit_log.append(f"[-] Übertragungsfehler: {str(e)}")
        return {
            "success": False,
            "status": 500,
            "duration": duration,
            "error": str(e),
            "audit_log": audit_log
        }

# Set page config with custom logo icon
logo_icon_file = ROOT_DIR / "site" / "ki_advisor_icon.png"
if not logo_icon_file.exists():
    logo_icon_file = ROOT_DIR / "ki_advisor_icon.png"

st.set_page_config(
    page_title="Conciliamus AI Advisor",
    page_icon=str(logo_icon_file) if logo_icon_file.exists() else "🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for fixed bottom chat input & clean Google-like layout
st.markdown("""
<style>
    /* Fixed Bottom Chat Bar: Rigidly anchored at the bottom of the viewport */
    div[data-testid="stBottom"] {
        position: fixed !important;
        bottom: 0px !important;
        left: 0px !important;
        right: 0px !important;
        width: 100% !important;
        z-index: 999999 !important;
        background: rgba(15, 23, 42, 0.98) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.8) !important;
        padding: 12px 20px 16px 20px !important;
    }

    div[data-testid="stBottom"] > div {
        max-width: 860px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    /* Scrollable content container with generous bottom offset */
    .main .block-container {
        padding-bottom: 140px !important;
        padding-top: 1rem !important;
        max-width: 860px !important;
        margin: 0 auto !important;
    }

    /* Clean subtle sidebar expanders */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        margin-bottom: 8px !important;
        background: rgba(15, 23, 42, 0.5) !important;
    }

    /* Custom button styling in sidebar */
    [data-testid="stSidebar"] div[data-testid="stButton"] button {
        border-radius: 8px !important;
        font-size: 11.5px !important;
        text-align: left !important;
        padding: 6px 10px !important;
        line-height: 1.3 !important;
        transition: all 0.2s ease !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SECRETS HELPER -----------------
def get_secret(key: str, default: str = "") -> str:
    """Safely retrieves a secret from st.secrets, environment, or default."""
    try:
        if hasattr(st, "secrets"):
            val = st.secrets.get(key)
            if val is not None:
                return str(val)
    except Exception:
        pass
    return os.environ.get(key, default)

# Load Knowledge Base
def get_knowledge_mtime() -> float:
    mtime = 0.0
    if KNOWLEDGE_DIR.exists():
        for file_path in KNOWLEDGE_DIR.rglob("*.md"):
            try:
                mtime = max(mtime, file_path.stat().st_mtime)
            except Exception:
                pass
    if GRAPH_PATH.exists():
        try:
            mtime = max(mtime, GRAPH_PATH.stat().st_mtime)
        except Exception:
            pass
    return mtime

@st.cache_resource
def load_knowledge_base(mtime_key: float) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    concepts = []
    frontmatter_re = re.compile(r"^---s*\n(.*?)\n---s*\n", re.DOTALL)
    
    if KNOWLEDGE_DIR.exists():
        for file_path in KNOWLEDGE_DIR.rglob("*.md"):
            if file_path.name == "index.md":
                continue
            try:
                text = file_path.read_text(encoding="utf-8")
                rel_path = file_path.relative_to(KNOWLEDGE_DIR).as_posix()
                match = frontmatter_re.match(text)
                if match:
                    fm = yaml.safe_load(match.group(1)) or {}
                    body = text[match.end():].strip()
                    cid = fm.get("id") or rel_path.replace(".md", "")
                    concepts.append({
                        "id": cid,
                        "path": rel_path,
                        "frontmatter": fm,
                        "content": body,
                        "title": fm.get("title", cid),
                        "type": fm.get("type", "Concept"),
                        "tags": fm.get("tags", []),
                        "fullText": (fm.get("title", "") + " " + fm.get("description", "") + " " + body).lower()
                    })
            except Exception:
                pass

    graph = {}
    if GRAPH_PATH.exists():
        try:
            graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    manifest = {}
    if MANIFEST_PATH.exists():
        try:
            manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    return concepts, graph, manifest

concepts, graph, manifest = load_knowledge_base(get_knowledge_mtime())

# Retrieve top relevant context documents
def retrieve_relevant_docs(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    stop_words = {
        "wie", "was", "warum", "welche", "welcher", "welches", "und", "oder", 
        "der", "die", "das", "dem", "den", "des", "ein", "eine", "einer", "eines", 
        "einem", "einen", "nach", "für", "fuer", "mit", "von", "aus", "bei", 
        "zum", "zur", "ist", "sind", "wird", "werden", "hat", "haben", "kann", "können"
    }
    explicit_adrs = [m.lower() for m in re.findall(r"adr-d{3}", query, re.IGNORECASE)]
    keywords = [w.lower() for w in re.findall(r"w+", query) if len(w) > 2 and w.lower() not in stop_words]
    if not keywords and not explicit_adrs:
        return concepts[:top_k]
    
    scored = []
    for c in concepts:
        score = 0
        cid_lower = c["id"].lower()
        cpath_lower = c["path"].lower()
        ctitle_lower = c["title"].lower()
        slug = cpath_lower.split("/")[-1].replace(".md", "")
        term = str(c["frontmatter"].get("term", "")).lower()
        
        # Priority boost for matching ADRs
        for eadr in explicit_adrs:
            if eadr in cid_lower or eadr in cpath_lower:
                score += 120
            elif eadr in ctitle_lower:
                score += 60

        for kw in keywords:
            cnt = min(c["fullText"].count(kw), 8)
            score += cnt
            if kw == slug or kw == term or kw == cid_lower.split("/")[-1]:
                score += 50
            elif kw in cid_lower:
                score += 15
            if kw in ctitle_lower:
                score += 12
            if any(kw in t.lower() for t in c["tags"]):
                score += 8
            if kw in c["frontmatter"].get("description", "").lower():
                score += 5
        if score > 0:
            scored.append((score, c))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]] if scored else concepts[:2]

# Build Gemini System Prompt
def get_system_prompt() -> str:
    persona = manifest.get("spec", {}).get("persona", {})
    role = persona.get("role", "Senior SAP BTP Cloud Integration Specialist & Enterprise Architect")
    tone = persona.get("tone", "professionell, methodisch präzise, architekturbewusst, lösungsorientiert")
    purpose = manifest.get("spec", {}).get("purpose", "")

    return f"""Du bist der Conciliamus AI Architecture Advisor.
Rolle: {role}
Ton: {tone}
Aufgabe: {purpose}

Verbindliche Richtlinien:
1. Beantworte alle Fragen strikt auf Basis der beigefügten Dokumente aus dem Google Open Knowledge Format (OKF v0.2) Wissensbündel ({len(concepts)} verifizierte Dokumente inkl. 12 ADRs und Enterprise Acronym Digest).
2. Zitiere konkrete Architecture Decision Records (z.B. [ADR-001] bis [ADR-012]) und Konzeptdateien.
3. Wenn Diagramme den Sachverhalt verdeutlichen, formatiere sie als Mermaid-Codeblöcke (`mermaid`).
4. Betone stets Idempotenz, Entkopplung (Dual-iFlow), Bruce Silver BPMN 2.0 Method & Style Nomenklatur und Resilienz.
5. Beachte stets die Preservation von Camel Exchange Properties bei Request-Reply-Schritten zur Vermeidung von HTTP 401 Header-Verlusten (ADR-012) und Zero-Hardcoding via parameters.prop.
6. Wenn eine Information im Wissensbündel nicht enthalten ist, weise transparent darauf hin, statt zu spekulieren.
"""

# Call Gemini API
def ask_gemini(api_key: str, model_name: str, query: str, context_docs: List[Dict[str, Any]]) -> str:
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        
        context_str = "\n\n---\n\n".join([
            f"### Dokument: {d['title']} ({d['path']})\n**Typ:** {d['type']} | **Status:** {d['frontmatter'].get('status', 'verified')}\n\n{d['content']}"
            for d in context_docs
        ])

        user_content = f"""Folgende verifizierte Architektur-Dokumente liegen dir vor:

{context_str}

---
BENUTZERFRAGE:
{query}
"""

        system_instruction = get_system_prompt()
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2
        )

        # Try requested model, with automatic fallback if deprecated/404
        models_to_try = [model_name]
        for fallback in ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            if fallback not in models_to_try:
                models_to_try.append(fallback)

        last_err = None
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=user_content,
                    config=config
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_err = e
                # Fallback on 404 (model not found), 503 (high demand/overload), 429 (rate limit) or transient errors
                err_str = str(e)
                if any(k in err_str for k in ["404", "NOT_FOUND", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "high demand", "no longer available"]):
                    continue
                else:
                    continue

        # If all Gemini cloud models are busy/unavailable, fall back gracefully to the grounded local knowledge
        best_doc = context_docs[0] if context_docs else None
        if best_doc:
            return (
                f"⚠️ *(Google AI Studio ist momentan kurzzeitig ausgelastet [503/429]. "
                f"Der Conciliamus Advisor greift direkt auf die verifizierten OKF-Architekturdaten zu:)*\n\n"
                f"### {best_doc['title']}\n\n"
                f"{best_doc['content']}"
            )
        return f"❌ Fehler beim Aufruf der Gemini API: {str(last_err)}"
    except Exception as e:
        best_doc = context_docs[0] if context_docs else None
        if best_doc:
            return (
                f"⚠️ *(Temporärer Verbindungsengpass zu Google AI Studio. "
                f"Direkte Antwort aus den verifizierten Architektur-Dokumenten:)*\n\n"
                f"### {best_doc['title']}\n\n"
                f"{best_doc['content']}"
            )
        return f"❌ Fehler beim Aufruf der Gemini API: {str(e)}"

# Define all 12 ADR sample queries
sample_queries = [
    "Wie funktioniert das Dual-iFlow Entkopplungsmuster nach ADR-001?",
    "Wie setzt ADR-002 die Zero-Trust & BTP PaaS Security (OAuth2/XSUAA) um?",
    "Wie gewährleistet ADR-003 die End-to-End Traceability im SAP MPL-Log?",
    "Welche BPMN 2.0 Regeln nach Bruce Silver definiert ADR-004 für den Ingest-Flow?",
    "Warum nutzt die Architektur ProcessDirect statt Message Queues (ADR-005)?",
    "Wie funktioniert die idempotente Existenzprüfung (POST vs. PATCH) nach ADR-006?",
    "Wie läuft der Two-Legged CSRF- und Cookie-Handshake nach ADR-007 ab?",
    "Wie unterscheidet ADR-008 zwischen fachlichen Fehlern und technischem DLQ-Replay?",
    "Welche Ergonomie-Prinzipien definiert ADR-009 für die Fiori Horizon Workbench?",
    "Wie löst ADR-010 das BTP CORS-Problem und das serverlose GitOps-Deployment?",
    "Wie stellt ADR-011 mit OKF v0.2 und Gemini 3.6 quellenbasierte Beratung sicher?",
    "Wie verhindert ADR-012 den HTTP 401 Header-Verlust bei Camel Request-Reply durch Exchange Properties & Zero-Hardcoding?"
]

# ----------------- SIDEBAR (AUF- UND ZUKLAPPBARE BEREICHE) -----------------
logo_b64 = get_advisor_logo_base64()

with st.sidebar:
    # Sidebar Header with Dieter's Logo
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; padding: 6px 0 12px 0; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 12px;">
        <img src="{logo_b64}" style="height: 38px; width: auto; object-fit: contain;" alt="IT-Advisor Logo" />
        <div>
            <div style="font-weight: 800; font-size: 13.5px; color: #f8fafc; letter-spacing: -0.3px;">Conciliamus AI Advisor</div>
            <div style="font-size: 10px; color: #38bdf8; font-family: monospace;">OKF v0.2 • 12 ADRs</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # BEREICH 1: Beispielfragen (Hier im Drawer aufklappbar, nicht im Hauptbereich!)
    with st.expander("💡 Beispielfragen (ADR-001 bis ADR-012)", expanded=True):
        st.markdown("<div style='font-size:11px; color:#94a3b8; margin-bottom:8px;'>Klicken Sie auf eine Frage, um den Dialog im Hauptbereich zu starten:</div>", unsafe_allow_html=True)
        for idx, sq in enumerate(sample_queries):
            adr_num = sq.split("ADR-")[1][:3] if "ADR-" in sq else str(idx+1)
            btn_label = f"📌 [ADR-{adr_num}] {sq}"
            if st.button(btn_label, key=f"sb_adr_chip_{idx}", use_container_width=True):
                st.session_state.current_prompt = sq
                st.rerun()

    # BEREICH 2: Wissensbasis & Metriken
    with st.expander("📊 Wissensbasis & Status", expanded=False):
        nodes_count = len(graph.get("nodes", [])) if "nodes" in graph else graph.get("nodesCount", 34)
        edges_count = len(graph.get("edges", [])) if "edges" in graph else graph.get("edgesCount", 99)
        st.markdown(f"- **OKF Dokumente:** `{len(concepts)}`")
        st.markdown(f"- **Wissensgraph:** `{nodes_count} Knoten / {edges_count} Kanten`")
        st.markdown(f"- **Architektur-Entscheidungen:** `12 ADRs (ADR-001 bis ADR-012)`")
        st.markdown(f"- **OKF Version:** `v0.2`")
        st.markdown("---")
        if st.button("🔄 Wissensbasis neu laden", key="btn_reload_kb", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()

    # BEREICH 3: ADR-Katalog Übersicht
    with st.expander("📜 ADR-Katalog (12 Entscheidungen)", expanded=False):
        adr_docs = [c for c in concepts if c.get("type") == "Decision Record" or "adr-" in c["id"]]
        adr_docs.sort(key=lambda x: x["id"])
        for adr in adr_docs:
            fm = adr["frontmatter"]
            status = fm.get('status', 'accepted').upper()
            title = fm.get('title', adr['title'])
            with st.expander(f"{title} [{status}]", expanded=False):
                st.markdown(f"**Beschreibung:** {fm.get('description', '-')}")
                st.markdown(f"**Status:** `{status}` | **Ressource:** `{fm.get('resource', '-')}`")
                st.markdown("---")
                st.markdown(adr["content"])

    # BEREICH 4: BTP Live-Workbench
    with st.expander("🧪 BTP Live-Workbench", expanded=False):
        st.markdown("Führen Sie einen Live-Batch-Test gegen den BTP-Tenant aus:")
        default_client_id = "sb-e1a4ca1f-7a33-4513-858d-77ba2c5e58dd!b706425|it-rt-b9c123f3trial!b55215"
        default_client_secret = "11930c12-a78b-4172-8004-f8c5a3a024b4$NCHm0cqnZea8wy3M_TT2Kp_Geurr7DE1cReWFnC2FJU="
        default_token_url = "https://b9c123f3trial.authentication.us10.hana.ondemand.com/oauth/token"
        default_runtime_url = "https://b9c123f3trial.it-cpitrial06-rt.cfapps.us10-001.hana.ondemand.com"

        if st.button("🚀 10er-Batch an BTP CPI senden", key="sb_btn_live_batch", use_container_width=True):
            with st.spinner("Sende Live-Batch an SAP Cloud Integration..."):
                creds = {
                    "token_url": default_token_url,
                    "runtime_url": default_runtime_url,
                    "client_id": default_client_id,
                    "client_secret": default_client_secret
                }
                testdata_file = TESTDATA_DIR / "Testdaten_prepared.json"
                payload = testdata_file.read_text(encoding="utf-8") if testdata_file.exists() else "{}"
                res = execute_cpi_live_test(payload, creds)
                if res.get("success"):
                    st.success(f"🎉 Erfolg: HTTP {res.get('status')} in {res.get('duration')}s")
                else:
                    st.error(f"❌ Fehler: {res.get('error')}")

        st.link_button("🌐 Test-Runner öffnen ↗", "https://orcai-54321.web.app/test-runner.html", use_container_width=True)

    # BEREICH 5: OpenAPI Spezifikationen & Schemas
    with st.expander("📐 OpenAPI & Schemas", expanded=False):
        st.markdown("""
        **Spezifizierte Integrationsendpunkte:**
        - `POST /http/conciliamus/v1/businesspartners/batch` (Inbound)
        - `POST /conciliamus/v1/businesspartners/item` (ProcessDirect)
        """)
        st.link_button("📂 OpenAPI Spec auf GitHub ↗", "https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/api/conciliamus-architecture.openapi.yaml", use_container_width=True)

    # BEREICH 6: Modell- & API-Konfiguration
    with st.expander("⚙️ KI-Modell & API-Key", expanded=False):
        default_key = get_secret("GEMINI_API_KEY", "")
        api_key = st.text_input(
            "Gemini API-Key:",
            type="password",
            value=default_key,
            help="Kostenloser API-Key auf aistudio.google.com – ohne Kreditkarte!"
        )
        if not api_key:
            st.info("💡 Kostenloser Key: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)")
        else:
            st.success("✅ API-Key hinterlegt")

        model_choice = st.selectbox(
            "Gemini Modell:",
            ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
            index=0
        )
        if st.button("🗑️ Chat-Verlauf löschen", key="btn_clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ----------------- HAUPTBEREICH (SO LEER UND AUFGERÄUMT WIE DIE GOOGLE-SUCHSEITE) -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# If no messages yet: Google-like centered landing view
if len(st.session_state.messages) == 0:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 52vh; text-align: center; padding: 20px 10px;">
        <img src="{logo_b64}" style="max-height: 115px; width: auto; object-fit: contain; filter: drop-shadow(0 12px 24px rgba(0,0,0,0.6)); margin-bottom: 20px;" alt="Conciliamus AI Advisor Logo" />
        <h1 style="font-size: 32px; font-weight: 800; color: #f8fafc; margin: 0 0 8px 0; letter-spacing: -0.5px;">Conciliamus AI Advisor</h1>
        <p style="font-size: 14px; color: #94a3b8; max-width: 540px; margin: 0 auto 16px auto; line-height: 1.5;">
            Senior SAP BTP Cloud Integration Specialist &amp; Enterprise Architect
        </p>
        <div style="display: inline-flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 600; color: #38bdf8; background: rgba(14, 165, 233, 0.12); border: 1px solid rgba(56, 189, 248, 0.25); padding: 4px 14px; border-radius: 9999px;">
            <span>Google OKF v0.2</span> • <span>{len(concepts)} Konzepte</span> • <span>12 verifizierte ADRs</span> • <span>Gemini 3.6 Flash</span>
        </div>
        <p style="font-size: 12px; color: #64748b; margin-top: 24px;">
            💡 Wählen Sie links eine Beispielfrage aus der Seitenleiste ⇦ oder tippen Sie unten in das Eingabefeld.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Render Chat Conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ----------------- RIGIDLY FIXED BOTTOM CHAT INPUT -----------------
user_input = st.chat_input("Ihre Frage an den Conciliamus AI Advisor...")
if "current_prompt" in st.session_state and st.session_state.current_prompt:
    user_input = st.session_state.current_prompt
    st.session_state.current_prompt = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        relevant_docs = retrieve_relevant_docs(user_input, top_k=5)
        
        # Check if api_key is available
        active_key = api_key if "api_key" in locals() and api_key else get_secret("GEMINI_API_KEY", "")
        active_model = model_choice if "model_choice" in locals() else "gemini-3.6-flash"

        if active_key:
            with st.spinner("Conciliamus Advisor konsultiert Gemini und Wissensgraph..."):
                answer = ask_gemini(active_key, active_model, user_input, relevant_docs)
        else:
            best = relevant_docs[0] if relevant_docs else None
            if best:
                answer = (
                    f"*(Hinweis: Lokale Wissensextraktion ohne Gemini API-Key. Für vollständige KI-Antworten bitte links in den Einstellungen einen kostenlosen Key von Google AI Studio eintragen.)*\n\n"
                    f"### {best['title']}\n\n"
                    f"{best['content']}\n\n"
                )
            else:
                answer = "Zu dieser Frage wurden keine spezifischen Konzepte im Wissensgraph gefunden."

        st.markdown(answer)

        if relevant_docs:
            with st.expander("📚 Herangezogene Quellen & Relationen"):
                for d in relevant_docs:
                    st.markdown(f"- **[{d['title']}](https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/knowledge/{d['path']})** (`{d['type']}`)")
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
