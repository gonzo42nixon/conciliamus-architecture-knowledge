---
id: digest/jwt-json-web-token
type: Architecture Concept
title: "JSON Web Token (RFC 7519)"
description: "Kompaktes, URL-sicheres Mittel zur Darstellung signierter Claims zwischen zwei Parteien."
resource: btp://conciliamus/digest/jwt-json-web-token
tags: ["digest","concept","security","security-governance-kritis","year-2015"]
status: verified
layer: 6
impact: 78
category: "Security"
year: "2015"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# JSON Web Token (RFC 7519)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `JWT JSON Web Token`
- **Meilenstein / Epoche:** Jahr 2015
- **Kategorie:** `Security`
- **Architektur-Ebene:** `Layer 6: Security, Governance & KRITIS`
- **Impact-Score:** `78 / 100`

## Bedeutung in der SAP-Welt
XSUAA-Token mit verschachtelten SAP-Scopes, Tenant-IDs und User-Attributes

## Fundamentale technische Bedeutung (Real World)
Kompaktes, URL-sicheres Mittel zur Darstellung signierter Claims zwischen zwei Parteien.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Autorisierung aller Inbound-Calls an den BTP-Tenant via Bearer-Header (Folie 07).
