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
import streamlit as st

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
KNOWLEDGE_DIR = ROOT_DIR / "knowledge"
GRAPH_PATH = ROOT_DIR / "graph" / "knowledge-graph.json"
MANIFEST_PATH = ROOT_DIR / "manifest" / "agent.yaml"

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

        response = client.models.generate_content(
            model=model_name,
            contents=user_content,
            config=config
        )
        return response.text
    except Exception as e:
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
        ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
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

tab_chat, tab_adrs, tab_specs = st.tabs(["💬 Architektur-Chat", "📜 Architecture Decisions (ADRs)", "📐 OpenAPI & Schemas"])

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

# ----------------- TAB 2: ADRs -----------------
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

# ----------------- TAB 3: SPECS -----------------
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
