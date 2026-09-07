---
id: digest/cors
type: Architecture Concept
title: "Cross-Origin Resource Sharing"
description: "W3C-Standard zur Einschränkung von Cross-Origin HTTP-Requests im Webbrowser."
resource: btp://conciliamus/digest/cors
tags: ["digest","concept","web-security","web-ui-frameworks","year-2006"]
status: verified
layer: 5
impact: 75
category: "Web & Security"
year: "2006"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# Cross-Origin Resource Sharing

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `CORS`
- **Meilenstein / Epoche:** Jahr 2006
- **Kategorie:** `Web & Security`
- **Architektur-Ebene:** `Layer 5: Web, UI & Frameworks`
- **Impact-Score:** `75 / 100`

## Bedeutung in der SAP-Welt
Browser-Sicherheitsmechanismus; von SAP BTP Integration Suite standardmäßig blockiert

## Fundamentale technische Bedeutung (Real World)
W3C-Standard zur Einschränkung von Cross-Origin HTTP-Requests im Webbrowser.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Per ADR-006 elegant gelöst durch Streamlit Cloud Serverless Proxy: Serverseitig kein CORS (Folie 05).
