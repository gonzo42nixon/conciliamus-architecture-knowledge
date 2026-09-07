---
id: digest/put
type: Architecture Concept
title: "HTTP PUT (RFC 9110)"
description: "Idempotente HTTP-Methode zur vollständigen Ersetzung des Zielressourcen-Zustands durch die Payload."
resource: btp://conciliamus/digest/put
tags: ["digest","concept","http-verb","web-ui-frameworks","year-1996"]
status: verified
layer: 5
impact: 74
category: "HTTP-Verb"
year: "1996"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# HTTP PUT (RFC 9110)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `PUT`
- **Meilenstein / Epoche:** Jahr 1996
- **Kategorie:** `HTTP-Verb`
- **Architektur-Ebene:** `Layer 5: Web, UI & Frameworks`
- **Impact-Score:** `74 / 100`

## Bedeutung in der SAP-Welt
Vollständiges Überschreiben einer OData-Entität (in modernen APIs meist durch PATCH ersetzt)

## Fundamentale technische Bedeutung (Real World)
Idempotente HTTP-Methode zur vollständigen Ersetzung des Zielressourcen-Zustands durch die Payload.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
In unserer Schnittstelle bewusst durch PATCH ersetzt, um Teil-Updates ohne Datenverlust zu sichern.
