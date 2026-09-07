---
id: digest/dom
type: Architecture Concept
title: "Document Object Model (W3C)"
description: "Baumorientierte In-Memory-Repräsentation von XML- und HTML-Dokumenten mit Traversierungs-API."
resource: btp://conciliamus/digest/dom
tags: ["digest","concept","xml-parsing","web-ui-frameworks","year-1998"]
status: verified
layer: 5
impact: 80
category: "XML & Parsing"
year: "1998"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# Document Object Model (W3C)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `DOM`
- **Meilenstein / Epoche:** Jahr 1998
- **Kategorie:** `XML & Parsing`
- **Architektur-Ebene:** `Layer 5: Web, UI & Frameworks`
- **Impact-Score:** `80 / 100`

## Bedeutung in der SAP-Welt
Vollständiges In-Memory Parsing von XML-Nachrichten (hoher RAM-Bedarf bei großen Batches!)

## Fundamentale technische Bedeutung (Real World)
Baumorientierte In-Memory-Repräsentation von XML- und HTML-Dokumenten mit Traversierungs-API.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Führt bei Großnachrichten zu Out-of-Memory! In iFlow 1 bewusst durch Streaming-Splitter vermieden (Folie 09).
