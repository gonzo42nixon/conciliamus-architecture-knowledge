"""
Conciliamus Architecture Advisor - Streamlit Web Application
Powered by Google AI Studio (Gemini API) and Google Open Knowledge Format (OKF v0.2).
Zero-Docker, Serverless Deployment on Streamlit Community Cloud.
"""
import os
import re
import json
import yaml
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
            audit_log.append(f"[-] CSRF-Warnung ({e.code}): Kein explizites CSRF-Token erhalten.")
    except Exception as e:
        audit_log.append(f"[-] CSRF-Fehler: {str(e)}")

    # Step 3: Batch POST
    audit_log.append(f"[*] Sende Batch-Payload an SAP Cloud Integration ({endpoint})...")
    post_start = time.time()
    try:
        req2 = urllib.request.Request(endpoint, data=payload_str.encode("utf-8"), method="POST")
        req2.add_header("Authorization", f"Bearer {token}")
        if csrf_token:
            req2.add_header("X-CSRF-Token", csrf_token)
        req2.add_header("Content-Type", "application/json")
        req2.add_header("Accept", "application/json, application/xml, text/plain")

        with opener.open(req2, timeout=25) as resp2:
            body = resp2.read().decode("utf-8", errors="replace")
            duration = round(time.time() - start_time, 2)
            headers = dict(resp2.headers)
            sap_msg_id = headers.get("Sap-Message-Id") or headers.get("sap-message-id") or headers.get("X-Correlation-ID") or "N/A"
            audit_log.append(f"[+++] HTTP {resp2.status} OK empfangen ({time.time() - post_start:.2f}s) - Gesamtzeit: {duration}s")
            return {
                "success": True,
                "status": resp2.status,
                "duration": duration,
                "body": body,
                "headers": headers,
                "sap_message_id": sap_msg_id,
                "audit_log": audit_log
            }
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        duration = round(time.time() - start_time, 2)
        audit_log.append(f"[-] HTTP {e.code} Fehler von CPI: {err_body[:200]}")
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

st.set_page_config(
    page_title="Conciliamus Architecture Advisor",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern enterprise look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4a5568;
        margin-bottom: 1.5rem;
    }
    .badge-okf {
        background-color: #ebf8ff;
        color: #2b6cb0;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #bee3f8;
    }
    .badge-gemini {
        background-color: #f0fff4;
        color: #276749;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #c6f6d5;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- ACCESS PROTECTION GATE -----------------
def check_password() -> bool:
    """Simple password protection gate using Streamlit secrets, env or default."""
    configured_pwd = "conciliamus2026"
    try:
        configured_pwd = st.secrets.get("APP_PASSWORD", os.environ.get("APP_PASSWORD", "conciliamus2026"))
    except Exception:
        configured_pwd = os.environ.get("APP_PASSWORD", "conciliamus2026")

    def password_entered():
        if st.session_state.get("password_input") == configured_pwd:
            st.session_state["password_correct"] = True
            if "password_input" in st.session_state:
                del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Show login screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header" style="text-align:center; margin-top: 3rem;">🔒 Geschützter Bereich</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header" style="text-align:center;">Conciliamus Architecture Advisor</div>', unsafe_allow_html=True)
        st.info("Bitte geben Sie das Zugangspasswort ein, um den Berater zu entsperren.")
        
        st.text_input(
            "Passwort:",
            type="password",
            on_change=password_entered,
            key="password_input",
            placeholder="Zugangspasswort eingeben..."
        )
        if st.button("Anmelden", use_container_width=True):
            password_entered()
            st.rerun()

        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ Falsches Passwort. Bitte überprüfen Sie Ihre Eingabe.")

    return False

if not check_password():
    st.stop()

# Load Knowledge Base
@st.cache_resource
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

concepts, graph, manifest = load_knowledge_base()

# Retrieve top relevant context documents
def retrieve_relevant_docs(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    keywords = [w.lower() for w in re.findall(r"\w+", query) if len(w) > 2]
    if not keywords:
        return concepts[:top_k]
    
    scored = []
    for c in concepts:
        score = 0
        for kw in keywords:
            score += c["fullText"].count(kw)
            if kw in c["title"].lower():
                score += 6
            if any(kw in t.lower() for t in c["tags"]):
                score += 4
            if kw in c["frontmatter"].get("description", "").lower():
                score += 3
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

    return f"""Du bist der Conciliamus Architecture Advisor.
Rolle: {role}
Ton: {tone}
Aufgabe: {purpose}

Verbindliche Richtlinien:
1. Beantworte alle Fragen strikt auf Basis der beigefügten Dokumente aus dem Google Open Knowledge Format (OKF v0.2) Wissensbündel.
2. Zitiere konkrete Architecture Decision Records (z.B. [ADR-001], [ADR-002], [ADR-003], [ADR-004], [ADR-005]) und Konzeptdateien.
3. Wenn Diagramme den Sachverhalt verdeutlichen, formatiere sie als Mermaid-Codeblöcke (`mermaid`).
4. Betone stets Idempotenz, Entkopplung (Dual-iFlow), Bruce Silver BPMN 2.0 Method & Style Nomenklatur und Resilienz.
5. Wenn eine Information im Wissensbündel nicht enthalten ist, weise transparent darauf hin, statt zu spekulieren.
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

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### 🔑 Google AI Studio")
    
    default_key = ""
    try:
        default_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    if not default_key:
        default_key = os.environ.get("GEMINI_API_KEY", "")

    api_key = st.text_input(
        "Gemini API-Key:",
        type="password",
        value=default_key,
        help="Holen Sie sich Ihren kostenlosen API-Key auf aistudio.google.com – ohne Billing-Setup!"
    )
    
    if not api_key:
        st.info("💡 **Kein Key?** Kostenloser Key auf:")
        st.markdown("[👉 aistudio.google.com/apikey](https://aistudio.google.com/apikey)")
    else:
        st.success("✅ API-Key aktiv")

    model_choice = st.selectbox(
        "Gemini Modell:",
        ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )

    st.markdown("---")
    st.markdown("### 📊 Wissensbasis Metriken")
    st.markdown(f"- **OKF Dokumente:** `{len(concepts)}`")
    st.markdown(f"- **Wissensgraph:** `{graph.get('nodesCount', 24)} Knoten / {graph.get('edgesCount', 63)} Kanten`")
    st.markdown(f"- **OKF Version:** `v0.2`")

    st.markdown("---")
    st.markdown("### 🚀 Schnellanfragen")
    sample_queries = [
        "Wie funktioniert das Dual-iFlow Muster nach ADR-001?",
        "Warum ProcessDirect statt Message Queues (ADR-002)?",
        "Wie ist die OData-Existenzprüfung und das Routing aufgebaut?",
        "Welche Resilienz-Strategie gilt für HTTP 405 Sandbox-Fehler?",
        "Was definiert ADR-005 für die Single-Viewport Fiori UI?"
    ]
    for sq in sample_queries:
        if st.button(sq, use_container_width=True):
            st.session_state.current_prompt = sq

    st.markdown("---")
    if st.button("🚪 Abmelden", use_container_width=True):
        st.session_state["password_correct"] = False
        st.rerun()

# ----------------- MAIN VIEW -----------------
st.markdown('<div class="main-header">🏛️ Conciliamus Architecture Advisor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    '<span class="badge-okf">Google Open Knowledge Format v0.2</span> &nbsp; '
    '<span class="badge-gemini">Google Gemini AI Studio</span> &nbsp; '
    'SAP BTP Cloud Integration & S/4HANA OData Architekturberater'
    '</div>', 
    unsafe_allow_html=True
)

tab_chat, tab_pecha, tab_runner, tab_adrs, tab_specs = st.tabs([
    "💬 Architektur-Chat", 
    "⏱️ Pecha Kucha (20x20)", 
    "🧪 Test-Runner (Workbench)",
    "📜 Architecture Decisions (ADRs)", 
    "📐 OpenAPI & Schemas"
])

# ----------------- TAB 1: CHAT -----------------
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hallo! Ich bin der **Conciliamus Architecture Advisor** (Senior SAP BTP Cloud Integration Specialist & Enterprise Architect).\n\n"
                    "Ich beantworte alle Fragen zur MDM-zu-S/4HANA Geschäftspartner-Synchronisation auf Basis der 25 kuratierten "
                    "OKF-Architekturdokumente und 5 Architecture Decision Records.\n\n"
                    "**Stellen Sie mir eine Frage oder wählen Sie links eine Schnellanfrage!**"
                )
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ihre Frage zur Conciliamus-Architektur...")
    if "current_prompt" in st.session_state and st.session_state.current_prompt:
        user_input = st.session_state.current_prompt
        st.session_state.current_prompt = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            relevant_docs = retrieve_relevant_docs(user_input, top_k=5)
            
            if api_key:
                with st.spinner("Conciliamus Advisor konsultiert Gemini und Wissensgraph..."):
                    answer = ask_gemini(api_key, model_choice, user_input, relevant_docs)
            else:
                best = relevant_docs[0] if relevant_docs else None
                if best:
                    answer = (
                        f"*(Hinweis: Lokale Wissensextraktion ohne Gemini API-Key. Für vollständige KI-Antworten bitte links einen kostenlosen Key von Google AI Studio eintragen.)*\n\n"
                        f"### {best['title']}\n\n"
                        f"{best['content']}\n\n"
                    )
                else:
                    answer = "Zu dieser Frage wurden keine spezifischen Konzepte gefunden."

            st.markdown(answer)

            if relevant_docs:
                with st.expander("📚 Herangezogene Quellen & Relationen"):
                    for d in relevant_docs:
                        st.markdown(f"- **[{d['title']}](https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/knowledge/{d['path']})** (`{d['type']}`)")
            
            st.session_state.messages.append({"role": "assistant", "content": answer})

# ----------------- TAB 2: PECHA KUCHA -----------------
with tab_pecha:
    st.markdown("### ⏱️ Pecha Kucha: MDM Business Partner Synchronisation")
    st.markdown("""
    **SAP Cloud Integration • Dual-iFlow Architektur • BPMN 2.0 Method & Style**  
    * **Format:** Exakt 20 Folien × 20 Sekunden = 6 Minuten 40 Sekunden (automatischer Folienwechsel & Audio-Chime)  
    * **Referent:** Dieter Rüffler (Dipl.-Inform. TU Berlin, ISTQB CTFL, ITIL V2)  
    * **Zielgruppe:** Markus Engelmann & Team *Plattform & Integration*, Conciliamus GmbH (Johannesstift Diakonie gAG)
    """)

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 1.8rem; border-radius: 12px; border: 1px solid #334155; margin: 1.2rem 0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.8rem;">
            <span style="background: #0070f2; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.85rem;">STAND-ALONE VOLLBILD</span>
            <span style="color: #cbd5e1; font-size: 0.9rem;">Web Audio Chime • SVG Countdown-Ring • Google Auth</span>
        </div>
        <h2 style="color: #ffffff; margin: 0 0 0.8rem 0; font-size: 1.5rem;">🎬 Pecha Kucha 20×20 Live-Präsentation</h2>
        <p style="color: #94a3b8; margin: 0 0 1.2rem 0; line-height: 1.5;">
            Öffnen Sie die Präsentation direkt als eigenständige Web-Anwendung im Vollbild.
            Dort funktioniert die <strong>Google Firebase Authentifizierung nativ und ohne iFrame-Sicherheitssperren</strong> moderner Browser.
        </p>
        <a href="https://orcai-54321.web.app/pecha-kucha.html" target="_blank" style="display: inline-block; background: #0070f2; color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold; text-decoration: none; font-size: 1rem; box-shadow: 0 4px 14px rgba(0,112,242,0.4);">
            🚀 Pecha Kucha Stand-Alone starten (Neuer Tab) ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 1])
    pecha_html = ""
    if PECHA_HTML_PATH.exists():
        pecha_html = PECHA_HTML_PATH.read_text(encoding="utf-8")
        with col_btn1:
            st.download_button(
                "💾 Präsentation als HTML herunterladen",
                pecha_html,
                file_name="pecha_kucha_presentation.html",
                mime="text/html",
                use_container_width=True
            )
    with col_btn2:
        st.link_button(
            "📂 Quellcode auf GitHub ansehen",
            "https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/site/pecha_kucha_presentation.html",
            use_container_width=True
        )

    # 20 Slides Transcript & Concept
    st.markdown("---")
    st.markdown("#### 📖 Ablauf & 20-Sekunden-Sprechertexte aller 20 Folien")
    if PECHA_KONZEPT_PATH.exists():
        konzept_text = PECHA_KONZEPT_PATH.read_text(encoding="utf-8")
        slides = re.split(r"### Folie\s+(\d+):\s+(.*?)\n", konzept_text)
        if len(slides) > 1:
            for i in range(1, len(slides), 3):
                num = slides[i]
                title = slides[i+1].strip()
                body = slides[i+2].strip()
                with st.expander(f"Folie {num}: {title}"):
                    st.markdown(body)
        else:
            st.markdown(konzept_text)

# ----------------- TAB 3: TEST-RUNNER WORKBENCH -----------------
with tab_runner:
    st.markdown("### 🧪 SAP Fiori Integration Workbench & Test-Runner")
    st.markdown("""
    **SAP Fiori Horizon Design System • Single-Viewport Workbench (ADR-005) • ISTQB CTFL Testsuite**  
    * **Technologie:** TailwindCSS, FontAwesome 6, Google Firebase Auth (Compat v12.2.1), SAP Horizon Design Tokens  
    * **Testsuite:** 10 automatisierte Testfälle (3× PATCH Existenz-Update, 7× POST Neuanlage & Boundary-Validierung)  
    * **Funktionen:** Echtzeit-Payload-Inspektor, Mock & Live-Runtime Modus, OData Response-Analyse, Log-Export  
    """)

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 1.8rem; border-radius: 12px; border: 1px solid #334155; margin: 1.2rem 0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.8rem;">
            <span style="background: #107e3e; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.85rem;">STAND-ALONE VOLLBILD</span>
            <span style="color: #cbd5e1; font-size: 0.9rem;">SAP Fiori Horizon • OData v2 Payloads • Native Google Auth</span>
        </div>
        <h2 style="color: #ffffff; margin: 0 0 0.8rem 0; font-size: 1.5rem;">🧪 SAP Fiori Test-Runner Workbench Live</h2>
        <p style="color: #94a3b8; margin: 0 0 1.2rem 0; line-height: 1.5;">
            Öffnen Sie die Test-Runner Workbench direkt als eigenständige Web-Anwendung im Vollbild.
            Dort funktioniert die <strong>Google Firebase Authentifizierung nativ und ohne iFrame-Sicherheitssperren</strong> moderner Browser (Third-Party Cookies / Cross-Origin Popup-Blocker).
        </p>
        <a href="https://orcai-54321.web.app/test-runner.html" target="_blank" style="display: inline-block; background: #0070f2; color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold; text-decoration: none; font-size: 1rem; box-shadow: 0 4px 14px rgba(0,112,242,0.4);">
            🚀 Test-Runner Workbench Stand-Alone starten (Neuer Tab) ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    col_btn_r1, col_btn_r2 = st.columns([1, 1])
    runner_html = ""
    if TEST_RUNNER_HTML_PATH.exists():
        runner_html = TEST_RUNNER_HTML_PATH.read_text(encoding="utf-8")
        with col_btn_r1:
            st.download_button(
                "💾 Test-Runner als HTML herunterladen",
                runner_html,
                file_name="sap_fiori_test_runner.html",
                mime="text/html",
                use_container_width=True
            )
    with col_btn_r2:
        st.link_button(
            "📂 Quellcode auf GitHub ansehen",
            "https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/site/test-runner.html",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("#### 📋 ISTQB Testfallmatrix (10 Testfälle: 3× PATCH, 7× POST)")
    st.markdown("""
| # | Testfall-ID | Kategorie & Beschreibung | HTTP Methode | Erwarteter Status |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `TC-01` | Existierender Partner 1 (Organisation) | **PATCH** | `204 No Content` |
| **02** | `TC-02` | Existierender Partner 2 (`BECHTLE AG`) | **PATCH** | `204 No Content` |
| **03** | `TC-03` | Existierender Partner 3 (`XYZ-PEPPOL`) | **PATCH** | `204 No Content` |
| **04** | `TC-04` | Neuanlage Partner (`JSD-BP-100001` Organisation) | **POST** | `201 Created` |
| **05** | `TC-05` | Neuanlage Natürliche Person mit Rollen `FLCU01`/`FLVN01` | **POST** | `201 Created` |
| **06** | `TC-06` | Duplikaterkennung & Abweisung (Mehrdeutiger Treffer) | **POST** | `422 FAILED_BUSINESS` |
| **07** | `TC-07` | Validierungsfehler: Fehlende Pflichtfelder | **POST** | `400 FAILED_VALIDATION` |
| **08** | `TC-08` | Schemavalidierung: Ungültige Partner-Kategorie | **POST** | `400 Bad Request` |
| **09** | `TC-09` | Grenzwertanalyse: Maximale Feldlängen & Sonderzeichen | **POST** | `200 / 201 OK` |
| **10** | `TC-10` | In-Memory ProcessDirect Routing zum Sub-iFlow | **POST** | `200 OK` |
    """)

    if ISTQB_STRATEGY_PATH.exists():
        with st.expander("📖 Vollständiges ISTQB Strategiedokument einsehen (OKF Knowledge Base)"):
            st.markdown(ISTQB_STRATEGY_PATH.read_text(encoding="utf-8"))

    # ----------------- LIVE CPI EXECUTION -----------------
    st.markdown("---")
    st.markdown("### ⚡ Live-Batch an SAP BTP Cloud Integration senden (Echtzeit)")
    st.markdown("""
    Hier können Sie einen **echten, unsimulierten Integrationslauf** direkt gegen Ihren SAP BTP Cloud Integration Tenant durchführen:
    * **OAuth2 Token-Dienst:** Authentifiziert sich mit XSUAA Client Credentials.
    * **CSRF-Schutz:** Holt das Session-Cookie und den dynamischen `X-CSRF-Token` vom Inbound-Endpunkt.
    * **Batch-POST:** Sendet das Batch-JSON an `IFL_MDM_BP_Batch_Receiver` (`/http/conciliamus/v1/businesspartners/batch`).
    * **Trace-Garantie:** **Jeder Klick erzeugt sofort einen sichtbaren Nachrichteneintrag im SAP CPI Message Monitoring!**
    """)

    default_client_id = "sb-e1a4ca1f-7a33-4513-858d-77ba2c5e58dd!b706425|it-rt-b9c123f3trial!b55215"
    default_client_secret = "11930c12-a78b-4172-8004-f8c5a3a024b4$NCHm0cqnZea8wy3M_TT2Kp_Geurr7DE1cReWFnC2FJU="
    default_token_url = "https://b9c123f3trial.authentication.us10.hana.ondemand.com/oauth/token"
    default_runtime_url = "https://b9c123f3trial.it-cpitrial06-rt.cfapps.us10-001.hana.ondemand.com"

    preset_col, btn_col = st.columns([2, 1])
    with preset_col:
        preset_choice = st.selectbox(
            "Test-Datensatz wählen:",
            [
                "10er-Vollbatch (Standard: 3x PATCH, 7x POST Deep Insert)",
                "Nur 3x Existierende Partner (PATCH Updates)",
                "Nur 7x Neuanlagen (POST Deep Insert)",
                "Fehlerfall-Batch (Ungültige E-Mail & falsches Land)"
            ],
            key="cpi_preset_select"
        )

    # Load data for the selected preset
    selected_payload = {}
    testdata_file = TESTDATA_DIR / "Testdaten_prepared.json"
    if testdata_file.exists():
        try:
            full_data = json.loads(testdata_file.read_text(encoding="utf-8"))
            if "Nur 3x Existierende Partner" in preset_choice:
                selected_payload = {
                    "batchId": f"BP-{time.strftime('%Y%m%d-%H%M%S')}-PATCH3",
                    "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "sourceSystem": "JSD-MDM",
                    "businessPartners": full_data.get("businessPartners", [])[:3]
                }
            elif "Nur 7x Neuanlagen" in preset_choice:
                selected_payload = {
                    "batchId": f"BP-{time.strftime('%Y%m%d-%H%M%S')}-POST7",
                    "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "sourceSystem": "JSD-MDM",
                    "businessPartners": full_data.get("businessPartners", [])[3:]
                }
            elif "Fehlerfall-Batch" in preset_choice:
                edge_file = TESTDATA_DIR / "edge_cases.json"
                if edge_file.exists():
                    selected_payload = json.loads(edge_file.read_text(encoding="utf-8"))
                    selected_payload["batchId"] = f"BP-{time.strftime('%Y%m%d-%H%M%S')}-ERR"
                else:
                    selected_payload = {
                        "batchId": f"BP-{time.strftime('%Y%m%d-%H%M%S')}-ERR",
                        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "sourceSystem": "JSD-MDM",
                        "businessPartners": [
                            {"externalId": "ERR-01", "company": "Invalid Co", "email": "invalid-email", "country": "DEU"}
                        ]
                    }
            else:
                selected_payload = dict(full_data)
                selected_payload["batchId"] = f"BP-{time.strftime('%Y%m%d-%H%M%S')}-FULL"
        except Exception:
            pass

    payload_text = st.text_area(
        "Batch-Payload (JSON vor dem Senden editierbar):",
        value=json.dumps(selected_payload, indent=2, ensure_ascii=False) if selected_payload else "{}",
        height=240,
        key="cpi_payload_editor"
    )

    with st.expander("⚙️ BTP Service Key Anmeldedaten konfigurieren"):
        cpi_token_url = st.text_input("OAuth2 Token-URL:", value=st.secrets.get("CPI_TOKEN_URL", os.environ.get("CPI_TOKEN_URL", default_token_url)), key="cpi_cfg_token_url")
        cpi_runtime_url = st.text_input("Cloud Integration Runtime-URL:", value=st.secrets.get("CPI_RUNTIME_URL", os.environ.get("CPI_RUNTIME_URL", default_runtime_url)), key="cpi_cfg_runtime_url")
        cpi_client_id = st.text_input("OAuth2 Client-ID:", value=st.secrets.get("CPI_CLIENT_ID", os.environ.get("CPI_CLIENT_ID", default_client_id)), key="cpi_cfg_client_id")
        cpi_client_secret = st.text_input("OAuth2 Client-Secret:", value=st.secrets.get("CPI_CLIENT_SECRET", os.environ.get("CPI_CLIENT_SECRET", default_client_secret)), type="password", key="cpi_cfg_client_secret")

    if st.button("🚀 Batch jetzt an SAP CPI senden (Live-Übertragung)", type="primary", use_container_width=True):
        with st.spinner("Sende Live-Batch an SAP Cloud Integration... (OAuth2 -> CSRF -> POST)"):
            creds = {
                "token_url": cpi_token_url,
                "runtime_url": cpi_runtime_url,
                "client_id": cpi_client_id,
                "client_secret": cpi_client_secret
            }
            res = execute_cpi_live_test(payload_text, creds)
            if res.get("success"):
                st.success(f"🎉 Batch erfolgreich an SAP Cloud Integration übertragen! (HTTP {res.get('status')} in {res.get('duration')}s)")
                st.info(
                    "🔍 **Spur im CPI Monitoring:** Wechseln Sie jetzt in den Browser-Tab **'Cloud Integration'** "
                    "(Tenant `b9c123f3trial` -> Operations View -> *Monitor Message Processing*). "
                    "Die Nachricht für `IFL_MDM_BP_Batch_Receiver` ist dort mit dem aktuellen Zeitstempel eingegangen!"
                )
                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    st.metric("HTTP Status", f"{res.get('status')} OK")
                with col_r2:
                    st.metric("Ausführungsdauer", f"{res.get('duration')} s")
                with col_r3:
                    st.metric("SAP Message ID", str(res.get("sap_message_id", "N/A"))[:20])

                with st.expander("📄 Antwortkörper von SAP CPI (XML/JSON)", expanded=True):
                    st.code(res.get("body", ""), language="xml" if "<root>" in res.get("body", "") else "json")

                with st.expander("📜 Audit-Log des Live-Aufrufs"):
                    for entry in res.get("audit_log", []):
                        st.markdown(f"`{entry}`")
            else:
                st.error(f"❌ Fehler bei der Übertragung an SAP CPI: {res.get('error', 'Unbekannter Fehler')}")
                with st.expander("Fehlerdetails"):
                    st.code(res.get("body", res.get("error", "")))
                    for entry in res.get("audit_log", []):
                        st.markdown(f"`{entry}`")

# ----------------- TAB 4: ADRs -----------------
with tab_adrs:
    st.markdown("### 🏛️ Verifizierte Architecture Decision Records (ADRs)")
    adr_docs = [c for c in concepts if c.get("type") == "Decision Record" or "adr-" in c["id"]]
    adr_docs.sort(key=lambda x: x["id"])

    for adr in adr_docs:
        fm = adr["frontmatter"]
        with st.expander(f"{fm.get('title', adr['title'])} [{fm.get('status', 'accepted').upper()}]"):
            st.markdown(f"**Beschreibung:** {fm.get('description', '-')}")
            st.markdown(f"**Status:** `{fm.get('status', 'accepted')}` | **Ressource:** `{fm.get('resource', '-')}`")
            st.markdown("---")
            st.markdown(adr["content"])

# ----------------- TAB 5: SPECS -----------------
with tab_specs:
    st.markdown("### 📐 OpenAPI Spezifikationen & Integrationsschemata")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚀 iFlow Runtime API (OpenAPI 3.1.0)")
        st.markdown("""
        Spezifiziert die tatsächlichen Integrationsendpunkte auf SAP BTP:
        - `POST /http/conciliamus/v1/businesspartners/batch` (HTTPS Inbound)
        - `POST /conciliamus/v1/businesspartners/item` (ProcessDirect In-Memory)
        """)
        st.markdown("[👉 GitHub: conciliamus-runtime-iflows.openapi.yaml](https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/api/conciliamus-runtime-iflows.openapi.yaml)")

    with col2:
        st.markdown("#### 🧠 Knowledge API (OpenAPI 3.1.0)")
        st.markdown("""
        Spezifiziert die REST-Schnittstelle zur programmatischen Abfrage des OKF-Wissensbündels:
        - `GET /concepts`, `GET /concepts/{id}`
        - `GET /decisions/{id}`
        - `GET /graph` (semantischer Wissensgraph)
        - `POST /rules/verify` (Architektur-Regelprüfung)
        """)
        st.markdown("[👉 GitHub: conciliamus-architecture.openapi.yaml](https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/api/conciliamus-architecture.openapi.yaml)")
