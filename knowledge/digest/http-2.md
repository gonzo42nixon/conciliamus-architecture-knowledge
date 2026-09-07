---
id: digest/http-2
type: Architecture Concept
title: "HTTP/2 Binary Framing & Multiplexing (RFC 7540 Mai 2015)"
description: "Binäres Framing-Protokoll: Multiplexing mehrerer Requests über eine einzige TCP-Verbindung, HPACK-Header-Kompression."
resource: btp://conciliamus/digest/http-2
tags: ["digest","concept","http-protokoll","os-netzwerk-transport","year-2015"]
status: verified
layer: 2
impact: 85
category: "HTTP Protokoll"
year: "2015"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# HTTP/2 Binary Framing & Multiplexing (RFC 7540 Mai 2015)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `HTTP/2`
- **Meilenstein / Epoche:** Jahr 2015
- **Kategorie:** `HTTP Protokoll`
- **Architektur-Ebene:** `Layer 2: OS, Netzwerk & Transport`
- **Impact-Score:** `85 / 100`

## Bedeutung in der SAP-Welt
Standardmäßig im SAP Cloud Connector und BTP API Management zur Latenzminimierung aktiv

## Fundamentale technische Bedeutung (Real World)
Binäres Framing-Protokoll: Multiplexing mehrerer Requests über eine einzige TCP-Verbindung, HPACK-Header-Kompression.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Beseitigt Head-of-Line-Blocking auf HTTP-Ebene und beschleunigt Fiori Launchpads mit hunderten Tile-Aufrufen.
