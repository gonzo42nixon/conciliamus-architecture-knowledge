---
id: digest/post
type: Architecture Concept
title: "HTTP POST (RFC 9110)"
description: "Standard-HTTP-Methode zur Übermittlung von Daten zur Erzeugung neuer untergeordneter Ressourcen."
resource: btp://conciliamus/digest/post
tags: ["digest","concept","http-verb","web-ui-frameworks","year-1991"]
status: verified
layer: 5
impact: 82
category: "HTTP-Verb"
year: "1991"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# HTTP POST (RFC 9110)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `POST`
- **Meilenstein / Epoche:** Jahr 1991
- **Kategorie:** `HTTP-Verb`
- **Architektur-Ebene:** `Layer 5: Web, UI & Frameworks`
- **Impact-Score:** `82 / 100`

## Bedeutung in der SAP-Welt
OData V2 Neuanlage via Deep Insert sowie Inbound-Batch-Übermittlung von JSD-MDM

## Fundamentale technische Bedeutung (Real World)
Standard-HTTP-Methode zur Übermittlung von Daten zur Erzeugung neuer untergeordneter Ressourcen.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
iFlow 1 empfängt Batches per POST; iFlow 2 legt neue Partner in S/4HANA an (7 von 10 Sätzen).
