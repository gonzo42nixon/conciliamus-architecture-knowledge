---
id: digest/head
type: Architecture Concept
title: "HTTP HEAD (RFC 9110)"
description: "HTTP-Methode wie GET, überträgt jedoch ausschließlich Response-Header ohne Message-Body."
resource: btp://conciliamus/digest/head
tags: ["digest","concept","http-verb","web-ui-frameworks"]
status: verified
layer: 5
impact: 65
category: "HTTP-Verb"
year: ""
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# HTTP HEAD (RFC 9110)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `HEAD`
- **Meilenstein / Epoche:** Klassisch / Zeitlos
- **Kategorie:** `HTTP-Verb`
- **Architektur-Ebene:** `Layer 5: Web, UI & Frameworks`
- **Impact-Score:** `65 / 100`

## Bedeutung in der SAP-Welt
Vorschalt-Call zur Beschaffung von Anti-CSRF-Token und Session-Cookies (X-CSRF-Token: Fetch)

## Fundamentale technische Bedeutung (Real World)
HTTP-Methode wie GET, überträgt jedoch ausschließlich Response-Header ohne Message-Body.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Step 1 unseres Two-Legged Handshakes (Folie 12): Holt CSRF-Token vor POST/PATCH ab.
