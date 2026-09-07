---
id: digest/options-preflight
type: Architecture Concept
title: "HTTP OPTIONS (CORS Preflight)"
description: "RFC 9110 Methode zur Ermittlung der Kommunikationsoptionen und CORS-Zugriffserlaubnis."
resource: btp://conciliamus/digest/options-preflight
tags: ["digest","concept","http-verb","web-ui-frameworks","year-1996"]
status: verified
layer: 5
impact: 68
category: "HTTP-Verb"
year: "1996"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# HTTP OPTIONS (CORS Preflight)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `OPTIONS (Preflight)`
- **Meilenstein / Epoche:** Jahr 1996
- **Kategorie:** `HTTP-Verb`
- **Architektur-Ebene:** `Layer 5: Web, UI & Frameworks`
- **Impact-Score:** `68 / 100`

## Bedeutung in der SAP-Welt
CORS-Preflight-Request von Browsern; wird von SAP BTP Integration Suite blockiert (401)

## Fundamentale technische Bedeutung (Real World)
RFC 9110 Methode zur Ermittlung der Kommunikationsoptionen und CORS-Zugriffserlaubnis.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Ursache des BTP CORS-Dilemmas, per ADR-006 über den Streamlit Cloud Serverless Proxy gelöst.
