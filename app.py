from __future__ import annotations
"""
Conciliamus AI Advisor - Streamlit Web Application
Powered by Google AI Studio (Gemini API), DeepSeek / OpenRouter Multi-LLM,
and Google Open Knowledge Format (OKF v0.2).
Zero-Docker, Serverless Deployment on Streamlit Community Cloud.
"""
import os
import re
import json
import yaml
import base64
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Iterator
import time
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import streamlit as st
import streamlit.components.v1 as components

from glossary_advisor import (
    build_glossary_analysis_prompt,
    build_glossary_visible_question,
    parse_glossary_query,
    polish_glossary_answer,
    should_dispatch_pending_glossary,
)
from chat_history import active_chat, bind_session, delete_chat, select_chat, serialize_store, start_new_chat, touch_active_chat
from streaming_utils import iter_openai_sse_lines, iter_text_chunks, smooth_stream

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
USER_AVATAR_URL = "https://firebasestorage.googleapis.com/v0/b/orcai-54321.firebasestorage.app/o/clients%2FACME%2Frecords%2FORCAI-260908-09H03-IMAGE-4PN9F%2Fpreview.png?alt=media&token=3246238a-cad5-4cdd-a9bf-ce4e8044ff72"
ASSISTANT_AVATAR_URL = "https://firebasestorage.googleapis.com/v0/b/orcai-54321.firebasestorage.app/o/clients%2FACME%2Frecords%2FORCAI-260908-09H03-IMAGE-NF52H%2Fpreview.png?alt=media&token=47c7f6b6-2801-4b7a-bac0-5f9ebe67bf8b"

@st.cache_data(show_spinner=False)
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
    initial_sidebar_state="collapsed"
)

# Custom CSS for high contrast typography, fixed bottom input & Google-like layout
st.markdown("""
<style>
    /* Global Base & Typography - Rich Dark, High Contrast, Readable Size */
    html, body, [class*="css"], .stApp {
        font-size: 15.5px !important;
        color: #f8fafc !important;
        background-color: #0b0f19 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Modern Chat Input: Rigidly fixed at the bottom of the viewport */
    div[data-testid="stCustomComponentV1"]:has(iframe[title*="modern_chat_input"]),
    div[data-testid="stElementContainer"]:has(iframe[title*="modern_chat_input"]) {
        position: fixed !important;
        bottom: 18px !important;
        left: 21rem !important;
        right: 0px !important;
        width: auto !important;
        z-index: 999999 !important;
        background: transparent !important;
        padding: 0 16px !important;
        box-sizing: border-box !important;
        pointer-events: none !important;
    }

    div[data-testid="stCustomComponentV1"]:has(iframe[title*="modern_chat_input"]) iframe[title*="modern_chat_input"],
    div[data-testid="stElementContainer"]:has(iframe[title*="modern_chat_input"]) iframe[title*="modern_chat_input"] {
        max-width: 860px !important;
        margin: 0 auto !important;
        display: block !important;
        pointer-events: auto !important;
        border: none !important;
        background: transparent !important;
        overflow: visible !important;
    }

    @media (max-width: 760px) {
        div[data-testid="stCustomComponentV1"]:has(iframe[title*="modern_chat_input"]),
        div[data-testid="stElementContainer"]:has(iframe[title*="modern_chat_input"]) {
            left: 0 !important;
            padding-inline: 10px !important;
        }
    }

    /* Fixed Bottom Chat Bar (Fallback stChatInput) */
    div[data-testid="stBottom"] {
        position: fixed !important;
        bottom: 0px !important;
        left: 0px !important;
        right: 0px !important;
        width: 100% !important;
        z-index: 999998 !important;
        background: rgba(11, 15, 25, 0.98) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.9) !important;
        padding: 10px 20px 14px 20px !important;
    }

    div[data-testid="stBottom"] > div {
        max-width: 860px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    div[data-testid="stChatInput"] textarea {
        font-size: 15px !important;
        color: #ffffff !important;
        background: #1e293b !important;
        border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 20px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        font-size: 14.5px !important;
    }

    /* Scrollable content container with generous bottom offset */
    .main .block-container {
        padding-bottom: 24px !important;
        padding-top: 1.2rem !important;
        max-width: 860px !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 860px !important;
        width: 100% !important;
        margin-inline: auto !important;
        padding-bottom: 24px !important;
    }
    .conversation-safe-space, #advisor-scroll-anchor {
        height: 150px !important;
        min-height: 150px !important;
        pointer-events: none !important;
    }

    /* Headings - Bold, high-contrast pure white and bright sky blue */
    h1 {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.4px !important;
        line-height: 1.3 !important;
    }
    h2 {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.2px !important;
        margin-top: 1rem !important;
    }
    h3 {
        font-size: 17.5px !important;
        font-weight: 700 !important;
        color: #38bdf8 !important;
    }
    h4, h5, h6 {
        font-size: 15.5px !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }

    /* Standard Text & Paragraphs */
    p, span, label {
        font-size: 15px !important;
        color: #f1f5f9 !important;
        line-height: 1.6 !important;
    }

    /* CHAT MESSAGES - Distinct, large, readable */
    [data-testid="stChatMessage"] {
        background-color: #131b2e !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
        font-size: 15.5px !important;
        line-height: 1.65 !important;
        color: #f8fafc !important;
    }
    [data-testid="stChatMessage"] strong, [data-testid="stChatMessage"] b {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    [data-testid="stChatMessage"] code {
        font-size: 14px !important;
        background: #1e293b !important;
        color: #38bdf8 !important;
        padding: 3px 7px !important;
        border-radius: 5px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
    }
    [data-testid="stChatMessage"] pre {
        background: #020617 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
    }

    /* SIDEBAR - compact, theme-independent light surface with dark text */
    [data-testid="stSidebar"] {
        background-color: #f3f6fa !important;
        border-right: 1px solid #cbd5e1 !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div:not([data-baseweb="select"]) {
        color: #172033 !important;
    }
    [data-testid="stSidebarContent"] {
        padding-top: 0.45rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }

    /* SIDEBAR EXPANDERS */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        margin-bottom: 4px !important;
        background: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        padding: 6px 10px !important;
        min-height: 34px !important;
        background: #ffffff !important;
        color: #172033 !important;
        border-radius: 7px !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        background: #e8f1fb !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary svg {
        fill: #334155 !important;
        color: #334155 !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
        padding: 2px 8px 7px !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary p,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary span {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #172033 !important;
    }

    /* SIDEBAR BUTTONS - Highly readable, bold, clear border & hover state */
    [data-testid="stSidebar"] div[data-testid="stButton"] button {
        border-radius: 7px !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        text-align: left !important;
        padding: 6px 9px !important;
        min-height: 34px !important;
        line-height: 1.25 !important;
        background: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        color: #172033 !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
        background: #0284c7 !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        transform: translateX(2px) !important;
    }
    [data-testid="stSidebar"] div[data-testid="stButton"] button:hover p,
    [data-testid="stSidebar"] div[data-testid="stButton"] button:hover span {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stLinkButton"] a {
        min-height: 34px !important;
        padding: 6px 9px !important;
        border-radius: 7px !important;
        border-color: #94a3b8 !important;
        color: #172033 !important;
        background: #ffffff !important;
        font-size: 12.5px !important;
    }

    /* DAY MODE: keep the complete embedded drawer legible on light desktops. */
    @media (prefers-color-scheme: light) {
        html, body, [class*="css"], .stApp {
            color: #172033 !important;
            background-color: #f7f9fc !important;
        }
        div[data-testid="stCustomComponentV1"]:has(iframe[title*="modern_chat_input"]),
        div[data-testid="stElementContainer"]:has(iframe[title*="modern_chat_input"]) {
            background: transparent !important;
        }
        [data-testid="stChatMessage"] {
            background: #ffffff !important;
            border-color: #cbd5e1 !important;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.10) !important;
        }
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li,
        p, span, label { color: #172033 !important; }
        [data-testid="stChatMessage"] code {
            background: #e6edf5 !important;
            color: #0369a1 !important;
            border-color: #b7c7d9 !important;
        }
        [data-testid="stChatMessage"] pre {
            background: #f1f5f9 !important;
            border-color: #cbd5e1 !important;
        }
        h1, h2 { color: #0f172a !important; }
        h4, h5, h6 { color: #334155 !important; }
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

# Load the immutable deployment bundle once per Streamlit worker. The explicit
# sidebar reload action remains available when a manual refresh is required.
@st.cache_resource(show_spinner=False)
def load_knowledge_base() -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    concepts = []
    frontmatter_re = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
    
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
                    full_text = (fm.get("title", "") + " " + fm.get("description", "") + " " + body).lower()
                    tokens = set(re.findall(r"\b[a-z0-9_äöüß]{2,}\b", full_text.replace("-", " ")))
                    concepts.append({
                        "id": cid,
                        "path": rel_path,
                        "frontmatter": fm,
                        "content": body,
                        "title": fm.get("title", cid),
                        "type": fm.get("type", "Concept"),
                        "tags": fm.get("tags", []),
                        "fullText": full_text,
                        "tokens": tokens
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

concepts, graph, manifest = load_knowledge_base()

# ----------------- HIGH-PRECISION RETRIEVAL WITH CONFIDENCE SCORING -----------------
@st.cache_data(show_spinner=False, max_entries=512)
def retrieve_relevant_docs(query: str, top_k: int = 5) -> Tuple[List[Dict[str, Any]], int, Dict[str, Any]]:
    """
    Retrieves the most relevant OKF architecture documents and computes a calibrated confidence score (0-99%).
    STRICT SAFETY RULE: Never returns irrelevant fallback documents if confidence is low.
    """
    stop_words = {
        "wie", "was", "warum", "welche", "welcher", "welches", "und", "oder", 
        "der", "die", "das", "dem", "den", "des", "ein", "eine", "einer", "eines", 
        "einem", "einen", "nach", "für", "fuer", "mit", "von", "aus", "bei", 
        "zum", "zur", "ist", "sind", "wird", "werden", "hat", "haben", "kann", "können", 
        "ab", "an", "auf", "in", "im", "ins", "über", "ueber", "unter", "vor", "hinter", 
        "neben", "zwischen", "durch", "ohne", "gegen", "um", "bis", "seit", "beim", "am", "vom",
        "ich", "mich", "mir", "du", "dir", "dich", "er", "sie", "es", "wir", "uns", "ihr", "euch", "ihnen",
        "mein", "meine", "meiner", "meines", "dein", "sein", "unser", "euer"
    }

    # Extract explicit ADR tokens (e.g. adr-001 ... adr-012)
    explicit_adrs = [m.lower() for m in re.findall(r"adr-\d{3}", query, re.IGNORECASE)]

    # Extract alphanumeric and hyphenated keywords (min length 3, excluding stop words)
    raw_words = re.findall(r"\b[a-zA-Z0-9_äöüÄÖÜß]{3,}\b", query.replace("-", " "))
    keywords = [w.lower() for w in raw_words if w.lower() not in stop_words]

    if not keywords and not explicit_adrs:
        return [], 0, {"match_type": "empty_query"}

    scored = []
    for c in concepts:
        score = 0
        cid_lower = c["id"].lower()
        cpath_lower = c["path"].lower()
        ctitle_lower = c["title"].lower()
        slug = cpath_lower.split("/")[-1].replace(".md", "")
        term = str(c["frontmatter"].get("term", "")).lower()

        # 1. Major boost for explicit ADR matches
        for eadr in explicit_adrs:
            if eadr in cid_lower or eadr in cpath_lower:
                score += 200
            elif eadr in ctitle_lower:
                score += 100

        # 2. Targeted whole-word keyword & acronym scoring
        doc_tokens = c.get("tokens") or set()
        for kw in keywords:
            # Exact acronym or slug match (e.g. btp, csrf, iflow, processdirect, camel)
            if kw == slug or kw == term or kw == cid_lower.split("/")[-1]:
                score += 60
            elif kw in cid_lower.split("/")[-1].split("-"):
                score += 30
            elif kw in re.findall(r"\b[a-z0-9_äöüß]{2,}\b", ctitle_lower.replace("-", " ")):
                score += 25
            elif any(kw == t.lower() for t in c["tags"]):
                score += 20
            elif kw in doc_tokens:
                cnt = min(len(re.findall(r"\b" + re.escape(kw) + r"\b", c["fullText"])), 8)
                score += cnt * 2

        if score > 0:
            scored.append((score, c))

    if not scored:
        return [], 0, {"match_type": "no_match"}

    scored.sort(key=lambda x: x[0], reverse=True)
    top_score = scored[0][0]

    # Calculate calibrated confidence percentage (0 to 99%)
    if explicit_adrs:
        confidence = min(99, 88 + min(11, top_score // 30))
    elif top_score >= 60:
        confidence = min(95, int(top_score * 1.1))
    elif top_score >= 25:
        confidence = min(75, int(top_score * 1.5))
    else:
        confidence = max(10, int(top_score * 1.8))

    # Strict Confidence Gate: Never return random concepts if query doesn't match!
    if confidence < 25 and not explicit_adrs:
        return [], confidence, {"match_type": "low_confidence", "top_score": top_score}

    selected = [item[1] for item in scored[:top_k]]
    return selected, confidence, {
        "match_type": "adr" if explicit_adrs else "concept",
        "top_score": top_score,
        "explicit_adrs": explicit_adrs
    }

# Build System Prompt
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
7. Beginne unmittelbar mit der inhaltlichen Antwort. Verwende keine Anrede, keine Selbstvorstellung und keinen Meta-Vorspann zur Rolle oder zum OKF-Wissensbündel.
8. Verwende als Schlussüberschrift ausschließlich „Zusammenfassung“, niemals „Zusammenfassung für das Team“.
"""

# ----------------- LLM PROVIDERS: GEMINI & DEEPSEEK / OPENROUTER -----------------

def normalize_gemini_model(model_name: str) -> str:
    """Normalizes any UI string or mockup version to a valid Google AI Studio model identifier."""
    lower = (model_name or "").lower()
    if "3.8" in lower:
        return "gemini-3.8-flash"
    if "3.7" in lower:
        return "gemini-3.7-flash"
    if "3.6" in lower:
        return "gemini-3.6-flash"
    if "3.5" in lower:
        return "gemini-3.5-flash"
    if "3.1" in lower and "pro" in lower:
        return "gemini-3.1-pro-preview"
    if "pro" in lower:
        return "gemini-3.1-pro-preview"
    if "2.0" in lower:
        return "gemini-2.0-flash"
    if "1.5" in lower:
        return "gemini-1.5-flash"
    return "gemini-3.6-flash"


@st.cache_resource(show_spinner=False, max_entries=4)
def get_gemini_client(api_key: str):
    """Reuse the SDK client and its HTTP connection pool across Streamlit reruns."""
    from google import genai
    from google.genai import types

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(api_version="v1beta", timeout=20000),
    )

def call_gemini(api_key: str, model_name: str, query: str, context_docs: List[Dict[str, Any]]) -> Optional[str]:
    """Calls Google Gemini with dynamic model discovery, multi-version fallback (v1/v1beta), and automatic resilience."""
    try:
        from google import genai
        from google.genai import types

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

        norm_model = normalize_gemini_model(model_name)

        # Try endpoints: stable v1 first, then v1beta
        for api_ver in ["v1", "v1beta"]:
            try:
                client = genai.Client(api_key=api_key, http_options={"api_version": api_ver})

                # Try dynamic model discovery to find what this specific key supports
                models_to_try = [norm_model]
                try:
                    for m in client.models.list():
                        name = (m.name or "").replace("models/", "")
                        acts = getattr(m, "supported_actions", None) or getattr(m, "supported_generation_methods", None) or []
                        if (not acts or "generateContent" in acts) and name and name not in models_to_try:
                            if "flash" in name or "pro" in name:
                                models_to_try.append(name)
                except Exception:
                    pass

                # Production models recognized by Google AI Studio
                for fallback in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro", "gemini-2.0-flash-lite"]:
                    if fallback not in models_to_try:
                        models_to_try.append(fallback)

                for m in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=user_content,
                            config=config
                        )
                        if response and response.text:
                            return response.text
                    except Exception as gen_err:
                        err_str = str(gen_err)
                        if "API_KEY_INVALID" in err_str or "401" in err_str:
                            return f"❌ **Gemini API-Fehler:** Der API-Schlüssel ist ungültig. Bitte prüfen Sie den Key in der Seitenleiste."
                        continue
            except Exception:
                continue

        # If all Gemini models returned errors (e.g. 404, quota): return None to trigger automatic local grounded fallback
        return None
    except Exception as e:
        return None


def stream_gemini(api_key: str, model_name: str, query: str, context_docs: List[Dict[str, Any]]) -> Iterator[str]:
    """Stream Gemini tokens with the current Google GenAI SDK."""
    from google.genai import types

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
    models_to_try = [
        normalize_gemini_model(model_name),
        "gemini-3.6-flash",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
    ]
    last_error: Exception | None = None
    client = get_gemini_client(api_key)
    config = types.GenerateContentConfig(system_instruction=get_system_prompt(), temperature=0.2)
    for active_model in dict.fromkeys(models_to_try[:2]):
        emitted = False
        try:
            for chunk in client.models.generate_content_stream(
                model=active_model,
                contents=user_content,
                config=config,
            ):
                if chunk.text:
                    emitted = True
                    yield chunk.text
            if emitted:
                return
        except Exception as error:
            last_error = error
            if emitted:
                return
    if last_error:
        raise last_error


def stream_deepseek_or_openrouter(
    api_key: str,
    provider: str,
    model_name: str,
    query: str,
    context_docs: List[Dict[str, Any]],
) -> Iterator[str]:
    """Stream DeepSeek/OpenRouter tokens from their compatible SSE API."""
    context_str = "\n\n---\n\n".join([
        f"### Dokument: {d['title']} ({d['path']})\n**Typ:** {d['type']} | **Status:** {d['frontmatter'].get('status', 'verified')}\n\n{d['content']}"
        for d in context_docs
    ])
    user_content = f"Folgende verifizierte Architektur-Dokumente liegen dir vor:\n\n{context_str}\n\n---\nBENUTZERFRAGE:\n{query}\n"
    if "deepseek" in provider.lower() and "openrouter" not in provider.lower():
        url = "https://api.deepseek.com/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        active_model = model_name if model_name in {"deepseek-chat", "deepseek-reasoner"} else "deepseek-chat"
    else:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://orcai-54321.web.app",
            "X-Title": "Conciliamus AI Advisor",
        }
        active_model = model_name if "/" in model_name else "deepseek/deepseek-chat"
    payload = {
        "model": active_model,
        "messages": [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.2,
        "stream": True,
    }
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    emitted = False
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            for token in iter_openai_sse_lines(response):
                emitted = True
                yield token
    except Exception:
        if not emitted:
            raise

def call_deepseek_or_openrouter(api_key: str, provider: str, model_name: str, query: str, context_docs: List[Dict[str, Any]]) -> str:
    """Calls DeepSeek or OpenRouter API (OpenAI-compatible)."""
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
    system_prompt = get_system_prompt()

    if "deepseek" in provider.lower() and "openrouter" not in provider.lower():
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        active_model = model_name if model_name in ["deepseek-chat", "deepseek-reasoner"] else "deepseek-chat"
    else:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://orcai-54321.web.app",
            "X-Title": "Conciliamus AI Advisor"
        }
        active_model = model_name if "/" in model_name else "deepseek/deepseek-chat"

    payload = {
        "model": active_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.2
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        return f"❌ **{provider} HTTP {e.code} Fehler:** {e.reason} ({err_body})"
    except Exception as e:
        return f"❌ **{provider} Verbindungsfehler:** {str(e)}"

def run_critic_audit(critic_key: str, query: str, draft_answer: str, context_docs: List[Dict[str, Any]]) -> str:
    """DeepSeek acts as the architectural critic and judge, refining and validating the draft."""
    url = "https://openrouter.ai/api/v1/chat/completions" if len(critic_key) > 40 and "sk-or" in critic_key else "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {critic_key}",
        "Content-Type": "application/json"
    }
    model = "deepseek/deepseek-chat" if "openrouter" in url else "deepseek-chat"

    sources_summary = ", ".join([d["title"] for d in context_docs[:3]])
    audit_prompt = f"""Du bist der unabhängige Architecture Reviewer & Auditor (DeepSeek Quality Gate).
Benutzerfrage: "{query}"
Quellen: {sources_summary}

Antwortentwurf:
{draft_answer}

AUFGABE:
1. Prüfe, ob die Antwort die Benutzerfrage präzise und vollständig beantwortet.
2. Prüfe, ob alle Zitate (z.B. ADRs) exakt den Tatsachen entsprechen und keine Halluzinationen vorliegen.
3. Wenn nötig, verbessere ungenaue Passagen direkt und erhalte das professionelle Markdown-Format.
Gib die geprüfte, optimierte Antwort aus."""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Du bist ein strenger Senior Enterprise Integration Auditor. Korrigiere Halluzinationen und unpassende Antworten."},
            {"role": "user", "content": audit_prompt}
        ],
        "temperature": 0.1
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            audited = data["choices"][0]["message"]["content"]
            return audited + "\n\n---\n🛡️ *Qualitäts-Audit: Durch DeepSeek-V3 erfolgreich verifiziert und freigegeben.*"
    except Exception:
        return draft_answer

# Curated, OKF-grounded starter questions grouped by user intent.
question_groups = [
    {
        "id": "adr",
        "title": "🏛️ ADR – Architecture Decision Records (12)",
        "expanded": False,
        "questions": [
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
            "Wie stellt ADR-011 mit OKF v0.2 und Gemini quellenbasierte Beratung sicher?",
            "Wie verhindert ADR-012 den HTTP 401 Header-Verlust bei Camel Request-Reply durch Exchange Properties & Zero-Hardcoding?",
        ],
    },
    {
        "id": "flows",
        "title": "🔄 Integration Flows & Data Flow",
        "expanded": False,
        "questions": [
            "Zeige den vollständigen Weg eines Business Partners vom MDM bis SAP S/4HANA.",
            "Welche Aufgaben übernimmt der IFL_MDM_BP_Batch_Receiver?",
            "Welche Aufgaben übernimmt der IFL_MDM_BP_Item_Processor?",
            "Warum werden Batch- und Einzelverarbeitung getrennt?",
            "Wie werden zehn Partner voneinander isoliert verarbeitet?",
            "Erzeuge ein Mermaid-Sequenzdiagramm des End-to-End-Ablaufs.",
            "Welche Daten und Metadaten werden über ProcessDirect weitergegeben?",
            "An welchen Stellen verändert sich das Nachrichtenformat?",
        ],
    },
    {
        "id": "development",
        "title": "💻 Development",
        "expanded": False,
        "questions": [
            "Wie verarbeitet der Batch Receiver einen eingehenden JSON-Batch?",
            "Wie arbeitet der Streaming Iterating Splitter?",
            "Welche Validierungen führt ValidateBusinessPartnerItem.groovy aus?",
            "Wie wird das Ergebnis der OData-Existenzprüfung ausgewertet?",
            "Wie werden POST- und PATCH-Payloads aufgebaut?",
            "Welche Exchange Properties und HTTP-Header werden verwendet?",
            "Wie wird die SAP-Business-Partner-Nummer dynamisch ermittelt?",
            "Wo befindet sich testdatenspezifische oder hart codierte Logik?",
            "Wie müsste der CSRF-Handshake im iFlow ergänzt werden?",
            "Wie müsste der Data-Store-Write für die DLQ implementiert werden?",
        ],
    },
    {
        "id": "contracts",
        "title": "🗂️ Data Contracts & Mapping",
        "expanded": False,
        "questions": [
            "Wie sieht der MDM-Inbound-Datenvertrag aus?",
            "Welche Felder sind Pflichtfelder?",
            "Wie wird externalId auf SAP S/4HANA abgebildet?",
            "Wie werden Firma, Adresse, E-Mail und Telefon gemappt?",
            "Wie sieht der POST-Deep-Insert-Payload aus?",
            "Welche Felder enthält der PATCH-Payload?",
            "Warum wird vatId aktuell nicht übertragen?",
            "Welche SAP-Feldlängen müssen berücksichtigt werden?",
            "Wie werden ungültige Länder- und E-Mail-Werte behandelt?",
        ],
    },
    {
        "id": "security",
        "title": "🛡️ Security & Compliance",
        "expanded": False,
        "questions": [
            "Wie ist der öffentliche HTTPS-Endpunkt abgesichert?",
            "Welche Rolle besitzt ESBMessaging.send?",
            "Wie funktioniert OAuth2 Client Credentials mit XSUAA?",
            "Wozu dient der SAP-Sandbox-API-Key?",
            "Welche Secrets und Endpunkte sind externalisiert?",
            "Wie funktioniert der Two-Legged-CSRF-Handshake?",
            "Warum müssen CSRF-Token und Session-Cookie gemeinsam übertragen werden?",
            "Welche Security-Unterschiede bestehen zwischen Sandbox und Produktion?",
            "Welche Zero-Trust-Anforderungen sind umgesetzt und welche fehlen?",
        ],
    },
    {
        "id": "testing",
        "title": "🧪 Testing & Quality Assurance",
        "expanded": False,
        "questions": [
            "Welche Testfälle decken POST, PATCH und Duplikate ab?",
            "Warum enthält der Referenzbatch drei Updates und sieben Neuanlagen?",
            "Wie teste ich einen ungültigen Einzeldatensatz?",
            "Wie teste ich die Fehlerisolation innerhalb eines Batches?",
            "Wie simuliere ich einen technischen Zielsystemausfall?",
            "Wie prüfe ich die Idempotenz?",
            "Wie teste ich einen Mehrfachtreffer bei der Existenzprüfung?",
            "Welche Aussagen sind durch einen Live-Lauf belegt?",
            "Welche Aussagen sind nur durch Design-Time-Artefakte belegt?",
        ],
    },
    {
        "id": "operations",
        "title": "📈 Operations",
        "expanded": False,
        "questions": [
            "Wie finde ich einen Batch anhand seiner BatchId im MPL?",
            "Wie finde ich alle Nachrichten zu einer ExternalId?",
            "Welche Custom Status Values verwendet die Lösung?",
            "Wie unterscheide ich fachliche und technische Fehler?",
            "Welche Informationen enthalten die MPL-Attachments?",
            "Was bedeuten FAILED_BUSINESS und FAILED_TECHNICAL?",
            "Welche Timeouts und Retry-Einstellungen sind konfiguriert?",
            "Wie funktioniert der selektive Wiederanlauf?",
            "Welche Betriebsinformationen fehlen für Production Readiness?",
        ],
    },
    {
        "id": "troubleshooting",
        "title": "🚨 Troubleshooting & Resilience",
        "expanded": False,
        "questions": [
            "Warum erhält ein POST- oder PATCH-Aufruf HTTP 401?",
            "Warum antwortet SAP mit HTTP 403?",
            "Was bedeutet HTTP 405 in der SAP-Sandbox?",
            "Warum wurde ein Business Partner mehrfach gefunden?",
            "Warum wurde ein Batch nicht vollständig verarbeitet?",
            "Warum kann der APIKey nach einem Request-Reply fehlen?",
            "Warum wird eine Nachricht nicht in der DLQ gespeichert?",
            "Warum wurde ein Partner als POST statt PATCH behandelt?",
            "Warum wurden Adressdaten bei PATCH nicht geändert?",
            "Wie kann eine einzelne Nachricht sicher erneut verarbeitet werden?",
        ],
    },
    {
        "id": "conformance",
        "title": "🧭 Implementation Conformance & Gaps",
        "expanded": False,
        "questions": [
            "Welche ADRs sind im aktuellen Export vollständig umgesetzt?",
            "Wo weicht der Item Processor von ADR-007 ab?",
            "Ist die DLQ aus ADR-008 tatsächlich implementiert?",
            "Ist die Header-Preservation aus ADR-012 vollständig umgesetzt?",
            "Welche Unterschiede bestehen zwischen dokumentierter und beobachteter Implementierung?",
            "Welche Lücken verhindern derzeit Production Readiness?",
            "Welche Änderungen haben die höchste Priorität?",
            "Welche Aussage stammt aus einem ADR und welche direkt aus dem ZIP-Export?",
            "Erstelle eine Conformance-Matrix aller ADRs.",
        ],
    },
    {
        "id": "digest",
        "title": "📚 Enterprise Acronym Digest",
        "expanded": False,
        "questions": [
            "Was bedeuten BTP, CPI und SAP Integration Suite?",
            "Was sind MPL und Custom Header Properties?",
            "Was ist ein iFlow?",
            "Was ist ProcessDirect?",
            "Was bedeuten BP, CVI und API_BUSINESS_PARTNER?",
            "Was sind OData V2, REST und HTTP?",
            "Was bedeuten POST, PATCH, GET und DELETE?",
            "Was sind CSRF, OAuth2, XSUAA und JWT?",
            "Was bedeuten DLQ, Retry und Replay?",
            "Was sind BPMN, EIP und ADR?",
            "Was bedeuten API, OpenAPI und JSON Schema?",
            "Erkläre alle Akronyme der aktuellen Antwort.",
        ],
    },
]

QA_SECTION_LABELS = {
    "adr": "ADR",
    "flows": "Iflows",
    "development": "Dev",
    "contracts": "Data",
    "security": "Security",
    "testing": "Tests",
    "operations": "Ops",
    "troubleshooting": "Troubleshooting",
    "conformance": "Conformance",
    "digest": "Glossar",
}

# Only offer starter questions that pass the same grounding gate as free-text input.
# This prevents a manually curated question from promising an answer the current OKF
# pool cannot support yet.
question_audit = [
    (group["id"], question, retrieve_relevant_docs(question, top_k=1)[1])
    for group in question_groups
    for question in group["questions"]
]
question_groups = [
    {
        **group,
        "questions": [
            question
            for question in group["questions"]
            if retrieve_relevant_docs(question, top_k=1)[1] >= 25
        ],
    }
    for group in question_groups
]

# ----------------- SIDEBAR (AUF- UND ZUKLAPPBARE BEREICHE) -----------------
logo_b64 = get_advisor_logo_base64()
if "chat_store" not in st.session_state:
    bind_session(st.session_state)

with st.sidebar:
    # Sidebar Header with Dieter's Logo
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:9px;padding:3px 0 7px;border-bottom:1px solid #cbd5e1;margin-bottom:5px;">
        <img src="{logo_b64}" style="height:32px;width:auto;object-fit:contain;" alt="IT-Advisor Logo" />
        <div>
            <div style="font-weight:800;font-size:14px;color:#0f172a;letter-spacing:-0.2px;">Conciliamus AI Advisor</div>
            <div style="font-size:11px;color:#0369a1;font-family:monospace;font-weight:700;">OKF v0.2 • 12 ADRs</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Persisted chat timeline. The browser-storage bridge lives in modern_chat_input.
    with st.expander("💬 Chats", expanded=True):
        if st.button("＋ Neuer Chat", key="btn_new_chat", use_container_width=True, type="primary"):
            start_new_chat(st.session_state.chat_store)
            bind_session(st.session_state)
            st.session_state.pop("chat_delete_candidate", None)
            st.rerun()
        for chat in sorted(st.session_state.chat_store["chats"], key=lambda item: item["updated_at"], reverse=True):
            prefix = "● " if chat["id"] == st.session_state.chat_store["active_id"] else ""
            chat_col, delete_col = st.columns([0.82, 0.18], gap="small")
            with chat_col:
                if st.button(prefix + chat["label"], key=f"chat_timeline_{chat['id']}", use_container_width=True):
                    if select_chat(st.session_state.chat_store, chat["id"]):
                        bind_session(st.session_state)
                        st.session_state.pop("chat_delete_candidate", None)
                        st.rerun()
            with delete_col:
                if st.button("🗑️", key=f"chat_delete_{chat['id']}", help=f"„{chat['label']}“ löschen"):
                    st.session_state["chat_delete_candidate"] = chat["id"]
                    st.rerun()

            if st.session_state.get("chat_delete_candidate") == chat["id"]:
                st.warning(f"Chat „{chat['label']}“ wirklich löschen?")
                confirm_col, cancel_col = st.columns(2)
                with confirm_col:
                    if st.button("Löschen", key=f"chat_delete_confirm_{chat['id']}", type="primary", use_container_width=True):
                        if delete_chat(st.session_state.chat_store, chat["id"]):
                            bind_session(st.session_state)
                        st.session_state.pop("chat_delete_candidate", None)
                        st.rerun()
                with cancel_col:
                    if st.button("Abbrechen", key=f"chat_delete_cancel_{chat['id']}", use_container_width=True):
                        st.session_state.pop("chat_delete_candidate", None)
                        st.rerun()

    # BEREICH 1: Kompakte, standardmäßig geschlossene Q&A-Starter
    with st.expander("Q&A", expanded=False):
        for group in question_groups:
            state_key = f"qa_section_open_{group['id']}"
            is_open = bool(st.session_state.get(state_key, False))
            chevron = "⌄" if is_open else "›"
            section_label = QA_SECTION_LABELS.get(group["id"], group["title"])
            if st.button(
                f"{chevron} {section_label}",
                key=f"qa_section_toggle_{group['id']}",
                use_container_width=True,
            ):
                st.session_state[state_key] = not is_open
                st.rerun()
            if is_open:
                for idx, question in enumerate(group["questions"]):
                    if st.button(f"📌 {question}", key=f"sb_question_{group['id']}_{idx}", use_container_width=True):
                        st.session_state.current_prompt = question
                        st.rerun()

    with st.expander("Links", expanded=False):
        st.link_button(
            "BTP ↗",
            "https://account.hanatrial.ondemand.com/trial/#/globalaccount/34eec884-0c14-4a9d-a509-55a912f83aee/accountModel&//?section=SubaccountsSection&view=TilesView",
            use_container_width=True,
        )
        st.link_button(
            "OpenAPI ↗",
            "https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/api/conciliamus-architecture.openapi.yaml",
            use_container_width=True,
        )

    # BEREICH 2: Wissensbasis & Metriken
    with st.expander("📊 Wissensbasis & Status", expanded=False):
        nodes_count = len(graph.get("nodes", [])) if "nodes" in graph else graph.get("nodesCount", 308)
        edges_count = len(graph.get("edges", [])) if "edges" in graph else graph.get("edgesCount", 99)
        st.markdown(f"- **OKF Dokumente:** `{len(concepts)}`")
        st.markdown(f"- **Geprüfte Starterfragen:** `{sum(len(group['questions']) for group in question_groups)} / {len(question_audit)}`")
        st.markdown(f"- **Wissensgraph:** `{nodes_count} Knoten / {edges_count} Kanten`")
        st.markdown(f"- **Architektur-Entscheidungen:** `12 ADRs (ADR-001 bis ADR-012)`")
        st.markdown(f"- **OKF Version:** `v0.2`")
        st.markdown("---")
        if st.button("🔄 Wissensbasis neu laden", key="btn_reload_kb", use_container_width=True):
            st.cache_resource.clear()
            st.cache_data.clear()
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
        st.markdown("Führen Sie einen Live-Batch-Test gegen den SAP BTP CPI Tenant aus:")
        
        # Sicher aus Secrets / Umgebungsvariablen laden (niemals hardcoded im Quellcode!)
        btp_client_id = get_secret("BTP_CLIENT_ID", "")
        btp_client_secret = get_secret("BTP_CLIENT_SECRET", "")
        btp_token_url = get_secret("BTP_TOKEN_URL", "")
        btp_runtime_url = get_secret("BTP_RUNTIME_URL", "")

        # Konfigurationsfelder für BTP Service-Key Credentials (anonymisiert / passwort-geschützt)
        with st.expander("🔑 BTP Service-Key Credentials konfigurieren", expanded=not bool(btp_client_secret)):
            c_id = st.text_input(
                "BTP Client-ID:",
                value=btp_client_id,
                placeholder="sb-xxxxxx!b000000|it-rt-trial!b00000",
                type="password" if btp_client_id else "default",
                help="Client-ID aus dem SAP BTP Service Key (oder in secrets.toml als BTP_CLIENT_ID hinterlegen)"
            )
            c_sec = st.text_input(
                "BTP Client-Secret:",
                value=btp_client_secret,
                placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx$...",
                type="password",
                help="Client-Secret aus dem SAP BTP Service Key (oder in secrets.toml als BTP_CLIENT_SECRET hinterlegen)"
            )
            t_url = st.text_input(
                "BTP Token-URL:",
                value=btp_token_url or "https://<subaccount>.authentication.us10.hana.ondemand.com/oauth/token",
                placeholder="https://<subaccount>.authentication.<region>.hana.ondemand.com/oauth/token"
            )
            r_url = st.text_input(
                "BTP Runtime-URL:",
                value=btp_runtime_url or "https://<subaccount>.it-cpitrial06-rt.cfapps.us10-001.hana.ondemand.com",
                placeholder="https://<subaccount>.it-cpitrial06-rt.cfapps.<region>.hana.ondemand.com"
            )

        if st.button("🚀 10er-Batch an BTP CPI senden", key="sb_btn_live_batch", use_container_width=True):
            active_cid = c_id or btp_client_id
            active_csec = c_sec or btp_client_secret
            active_turl = t_url or btp_token_url
            active_rurl = r_url or btp_runtime_url

            if not active_csec or not active_cid or "xxxx" in active_csec:
                st.warning("⚠️ Bitte tragen Sie gültige BTP Service-Key Credentials ein (oder hinterlegen Sie diese sicher in secrets.toml).")
            else:
                with st.spinner("Sende Live-Batch an SAP Cloud Integration..."):
                    creds = {
                        "token_url": active_turl,
                        "runtime_url": active_rurl,
                        "client_id": active_cid,
                        "client_secret": active_csec
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
        **ORCAI**

        Spezifizierte Integrationsendpunkte:
        - `POST /http/conciliamus/v1/businesspartners/batch` (Inbound)
        - `POST /conciliamus/v1/businesspartners/item` (ProcessDirect)
        """)
        st.link_button("ORCAI OpenAPI ↗", "https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/api/conciliamus-architecture.openapi.yaml", use_container_width=True)

        st.markdown("""
        **SAP – API_BUSINESS_PARTNER**

        Basis-URL:
        `https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER`

        - `GET /A_BusinessPartner`
        - `POST /A_BusinessPartner`
        - `PATCH /A_BusinessPartner('{BusinessPartner}')`

        HTTP-Header:

        - `Accept: application/json`
        - `Content-Type: application/json`
        - `APIKey: separat bereitgestellt`

        Der API-Key darf weder im Integration Flow noch im Groovy-Code fest hinterlegt werden.
        """)
        st.link_button("SAP API-Dokumentation ↗", "https://api.sap.com/api/API_BUSINESS_PARTNER/tryout", use_container_width=True)
        st.link_button(
            "Quelle: Praxisaufgabe (PDF) ↗",
            "https://firebasestorage.googleapis.com/v0/b/orcai-54321.firebasestorage.app/o/clients%2FACME%2Frecords%2FORCAI-260905-17H10-FILE-HSWWD%2FPraxisaufgabe%20%E2%80%93%20SAP%20Cloud%20Integration%20(SAP%20Integration%20Suite.pdf?alt=media&token=afecb33d-7bb0-4045-8bbe-579581fb67be",
            use_container_width=True,
        )

    # BEREICH 6: Multi-LLM Provider & Qualitäts-Audit Konfiguration
    with st.expander("⚙️ KI-Provider, DeepSeek & Audit", expanded=False):
        provider_options = [
            "Google Gemini (Schnell & Quellentreu)",
            "DeepSeek (Direkt via DeepSeek API)",
            "OpenRouter (DeepSeek V3 / R1 / Claude)",
            "Dual-Inspector: Gemini + DeepSeek Verifier (Höchste Qualität)"
        ]
        default_p_idx = 0
        if "active_provider" in st.session_state and st.session_state.active_provider in provider_options:
            default_p_idx = provider_options.index(st.session_state.active_provider)

        provider_choice = st.selectbox(
            "KI-Architektur & Provider:",
            provider_options,
            index=default_p_idx
        )

        # Gemini Key
        gemini_secret = get_secret("GEMINI_API_KEY", "")
        api_key = st.text_input(
            "Gemini API-Key:",
            type="password",
            value=gemini_secret,
            help="Kostenloser Key von aistudio.google.com"
        )

        # DeepSeek / OpenRouter Key
        deepseek_secret = get_secret("DEEPSEEK_API_KEY", "") or get_secret("OPENROUTER_API_KEY", "")
        deepseek_key = st.text_input(
            "DeepSeek / OpenRouter Key:",
            type="password",
            value=deepseek_secret,
            help="Key für DeepSeek API oder OpenRouter (für Dual-Inspection & Audit)"
        )

        # Model selection
        if "DeepSeek" in provider_choice and "Dual" not in provider_choice:
            ds_models = ["deepseek-chat", "deepseek-reasoner"]
            ds_idx = 0
            if st.session_state.get("active_model") in ds_models:
                ds_idx = ds_models.index(st.session_state["active_model"])
            model_choice = st.selectbox("DeepSeek Modell:", ds_models, index=ds_idx)
        elif "OpenRouter" in provider_choice:
            model_choice = st.selectbox("OpenRouter Modell:", ["deepseek/deepseek-chat", "deepseek/deepseek-r1", "google/gemini-2.5-flash", "anthropic/claude-3.5-sonnet"], index=0)
        else:
            gem_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
            gem_idx = 0
            if st.session_state.get("active_model") in gem_models:
                gem_idx = gem_models.index(st.session_state["active_model"])
            model_choice = st.selectbox("Gemini Modell:", gem_models, index=gem_idx)

        enable_audit = st.checkbox("🛡️ DeepSeek Qualitäts-Audit aktivieren", value=bool(deepseek_key))

        st.caption("Chats bleiben im Browser gespeichert, bis Sie bewusst „Neuer Chat“ wählen.")

# ----------------- HAUPTBEREICH (SO LEER UND AUFGERÄUMT WIE DIE GOOGLE-SUCHSEITE) -----------------
glossary_context = parse_glossary_query(st.query_params)
if glossary_context and glossary_context["request_id"] != st.session_state.get("last_glossary_request_id"):
    # Query-based glossary launches reload the Streamlit document. Defer the
    # question until browser-local chat history has been hydrated, otherwise the
    # answer would be written into a temporary empty session.
    st.session_state.pending_glossary_context = glossary_context

# If no messages yet: Google-like centered landing view
if len(st.session_state.messages) == 0:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 52vh; text-align: center; padding: 20px 10px;">
        <img src="{logo_b64}" style="max-height: 120px; width: auto; object-fit: contain; filter: drop-shadow(0 12px 24px rgba(0,0,0,0.8)); margin-bottom: 22px;" alt="Conciliamus AI Advisor Logo" />
        <h1 style="font-size: 32px; font-weight: 800; color: #ffffff; margin: 0 0 10px 0; letter-spacing: -0.5px;">Conciliamus AI Advisor</h1>
        <p style="font-size: 15.5px; color: #cbd5e1; font-weight: 500; max-width: 580px; margin: 0 auto 18px auto; line-height: 1.55;">
            Senior SAP BTP Cloud Integration Specialist &amp; Enterprise Architect
        </p>
        <div style="display: inline-flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 700; color: #38bdf8; background: rgba(14, 165, 233, 0.18); border: 1.5px solid rgba(56, 189, 248, 0.4); padding: 6px 16px; border-radius: 9999px;">
            <span>Google OKF v0.2</span> • <span>{len(concepts)} Konzepte</span> • <span>12 verifizierte ADRs</span> • <span>Gemini &amp; DeepSeek</span>
        </div>
        <p style="font-size: 13.5px; color: #94a3b8; font-weight: 500; margin-top: 26px;">
            💡 Wählen Sie links eine Beispielfrage aus der Seitenleiste ⇦ oder tippen Sie unten in das Eingabefeld.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Render Chat Conversation
    for msg in st.session_state.messages:
        avatar = USER_AVATAR_URL if msg["role"] == "user" else ASSISTANT_AVATAR_URL
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
    st.markdown('<div class="conversation-safe-space" aria-hidden="true"></div>', unsafe_allow_html=True)

# ----------------- RIGIDLY FIXED MODERN CHAT INPUT (SCREENSHOT 1 + SPRACHEINGABE) -----------------
component_dir = os.path.join(os.path.dirname(__file__), "components", "modern_chat_input")
custom_modern_input = None
if os.path.exists(component_dir):
    try:
        import streamlit.components.v1 as components
        custom_modern_input = components.declare_component("modern_chat_input", path=component_dir)
    except Exception as e:
        custom_modern_input = None

user_input = None
if custom_modern_input:
    # Pill label matching Screenshot 1: Gemini 3.8 Flash High ⚡ ^ (or active model)
    active_label = st.session_state.get("selected_model_label", "Gemini 3.6 Flash High")

    comp_res = custom_modern_input(
        placeholder="Ask anything, @ to mention, / for actions",
        initial_model=active_label,
        chat_store_json=serialize_store(st.session_state.chat_store),
        storage_hydrated=bool(st.session_state.get("chat_store_hydrated")),
        key="modern_input_widget"
    )

    if comp_res and isinstance(comp_res, dict):
        action = comp_res.get("action")
        ts = comp_res.get("timestamp")
        if ts and ts != st.session_state.get("last_handled_input_ts"):
            st.session_state["last_handled_input_ts"] = ts
            if action == "submit" and comp_res.get("text"):
                user_input = comp_res.get("text")
            elif action == "hydrate":
                bind_session(st.session_state, comp_res.get("text"))
                st.session_state["chat_store_hydrated"] = True
                st.rerun()
            elif action == "glossary" and comp_res.get("text"):
                try:
                    incoming_context = json.loads(comp_res.get("text"))
                except (TypeError, ValueError):
                    incoming_context = None
                request_id = incoming_context.get("request_id") if isinstance(incoming_context, dict) else None
                if request_id and request_id != st.session_state.get("last_glossary_request_id"):
                    st.session_state["last_glossary_request_id"] = request_id
                    st.session_state["current_glossary_context"] = incoming_context
                    user_input = build_glossary_visible_question(incoming_context)
            elif action == "model_change":
                new_model_label = comp_res.get("model")
                st.session_state["selected_model_label"] = new_model_label
                if "DeepSeek Reasoner" in new_model_label or "R1" in new_model_label:
                    st.session_state["active_provider"] = "DeepSeek (Direkt via DeepSeek API)"
                    st.session_state["active_model"] = "deepseek-reasoner"
                elif "DeepSeek V3" in new_model_label:
                    st.session_state["active_provider"] = "DeepSeek (Direkt via DeepSeek API)"
                    st.session_state["active_model"] = "deepseek-chat"
                elif "Dual" in new_model_label:
                    st.session_state["active_provider"] = "Dual-Inspector: Gemini + DeepSeek Verifier (Höchste Qualität)"
                elif "Pro" in new_model_label:
                    st.session_state["active_provider"] = "Google Gemini (Schnell & Quellentreu)"
                    st.session_state["active_model"] = "gemini-1.5-pro"
                elif "1.5" in new_model_label:
                    st.session_state["active_provider"] = "Google Gemini (Schnell & Quellentreu)"
                    st.session_state["active_model"] = "gemini-1.5-flash"
                else:
                    st.session_state["active_provider"] = "Google Gemini (Schnell & Quellentreu)"
                    st.session_state["active_model"] = "gemini-2.0-flash"
                st.rerun()
else:
    user_input = st.chat_input("Ask anything, @ to mention, / for actions")

pending_glossary_context = st.session_state.get("pending_glossary_context")
if should_dispatch_pending_glossary(
    pending_glossary_context,
    bool(st.session_state.get("chat_store_hydrated")),
    st.session_state.get("last_glossary_request_id"),
):
    st.session_state["last_glossary_request_id"] = pending_glossary_context["request_id"]
    st.session_state["current_glossary_context"] = pending_glossary_context
    st.session_state.pop("pending_glossary_context", None)
    user_input = build_glossary_visible_question(pending_glossary_context)

if "current_prompt" in st.session_state and st.session_state.current_prompt:
    user_input = st.session_state.current_prompt
    st.session_state.current_prompt = None

if user_input:
    active_glossary_context = st.session_state.pop("current_glossary_context", None)
    analysis_input = (
        build_glossary_analysis_prompt(active_glossary_context)
        if active_glossary_context
        else user_input
    )
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=USER_AVATAR_URL):
        st.markdown(user_input)

    touch_active_chat(st.session_state.chat_store, active_glossary_context.get("term") if active_glossary_context else None)
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR_URL):
        relevant_docs, confidence, meta = retrieve_relevant_docs(analysis_input, top_k=5)

        # CONFIDENCE GATE: Warn user cleanly if no matching architecture docs found
        if confidence < 25 or not relevant_docs:
            answer = (
                f"⚠️ **Konfidenz-Warnung (Relevanz-Score: {confidence}%)**\n\n"
                f"Zu Ihrer Frage konnten im Wissensgraphen keine hinreichend spezifischen Architektur-, Implementierungs-, Betriebs- "
                f"oder Acronym-Digest-Konzepte identifiziert werden.\n\n"
                f"💡 **Empfehlung:**\n"
                f"- Öffnen Sie links einen Themenblock und wählen Sie eine vorbereitete, OKF-basierte Frage.\n"
                f"- Oder verwenden Sie konkrete Begriffe wie *'ADR-007'*, *'CSRF'*, *'Dual-iFlow'*, *'ProcessDirect'*, *'BTP'* oder *'Camel'*."
            )
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            touch_active_chat(st.session_state.chat_store)
            st.rerun()

        # Check API key configuration
        active_gemini_key = api_key or get_secret("GEMINI_API_KEY", "")
        active_deepseek_key = deepseek_key or get_secret("DEEPSEEK_API_KEY", "") or get_secret("OPENROUTER_API_KEY", "")

        answer = ""
        answer_stream = None
        if "DeepSeek" in provider_choice and "Dual" not in provider_choice and active_deepseek_key:
            answer_stream = stream_deepseek_or_openrouter(active_deepseek_key, "DeepSeek", model_choice, analysis_input, relevant_docs)
        elif "OpenRouter" in provider_choice and active_deepseek_key:
            answer_stream = stream_deepseek_or_openrouter(active_deepseek_key, "OpenRouter", model_choice, analysis_input, relevant_docs)
        elif active_gemini_key:
            answer_stream = stream_gemini(active_gemini_key, model_choice, analysis_input, relevant_docs)
        elif active_deepseek_key:
            answer_stream = stream_deepseek_or_openrouter(active_deepseek_key, "DeepSeek", "deepseek-chat", analysis_input, relevant_docs)

        if answer_stream is not None:
            try:
                answer = st.write_stream(smooth_stream(answer_stream)) or ""
            except Exception:
                answer = ""

        # Quiet fail-safe: render exactly one grounded response if streaming was unavailable.
        if not answer:
            best = relevant_docs[0]
            note_suffix = " (Lokales Grounding aktiv)" if not active_gemini_key and not active_deepseek_key else " (Provider nicht erreichbar – OKF-Direkt-Grounding aktiv)"
            answer = (
                f"> [!NOTE]\n"
                f"> **🏛️ Verifizierte Architektur-Antwort{note_suffix} • Konfidenz: {confidence}%**\n"
                f"> *(Direkte quellengetreue Extraktion aus dem Google OKF v0.2 Repository für `{best['id']}`)*\n\n"
                f"### {best['title']}\n\n"
                f"{best['content']}\n"
            )
            if active_glossary_context:
                answer = polish_glossary_answer(answer)
            answer = st.write_stream(iter_text_chunks(answer)) or answer

        # Citations & Source Links
        if relevant_docs:
            with st.expander(f"📚 Herangezogene Quellen & Relationen (Konfidenz: {confidence}%)"):
                for d in relevant_docs:
                    st.markdown(f"- **[{d['title']}](https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/knowledge/{d['path']})** (`{d['type']}`)")

        st.session_state.messages.append({"role": "assistant", "content": answer})
        touch_active_chat(st.session_state.chat_store)
        persisted_store = json.dumps(serialize_store(st.session_state.chat_store))
        components.html(
            f"""
            <script>
              try {{ window.parent.localStorage.setItem('conciliamus.ai-advisor.chats.v1', {persisted_store}); }} catch (error) {{}}
              try {{
                const main = window.parent.document.querySelector('[data-testid="stMain"]');
                if (main) main.scrollTo({{ top: main.scrollHeight, behavior: 'smooth' }});
              }} catch (error) {{}}
            </script>
            """,
            height=0,
        )
        st.markdown('<div id="advisor-scroll-anchor" aria-hidden="true"></div>', unsafe_allow_html=True)
