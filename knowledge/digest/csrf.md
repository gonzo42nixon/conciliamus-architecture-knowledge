---
id: digest/csrf
type: Architecture Concept
title: "CSRF-Schutz & Two-Legged Handshake"
description: "Sicherheitsstandard (OWASP Top 10), der verhindert, dass unautorisierte Befehle im Namen eines authentifizierten Benutzers übertragen werden."
resource: btp://conciliamus/digest/csrf
tags: ["digest","concept","web-security","security-governance-kritis","year-2006"]
status: verified
layer: 6
impact: 88
category: "Web & Security"
year: "2006"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# CSRF-Schutz & Two-Legged Handshake

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `CSRF`
- **Meilenstein / Epoche:** Jahr 2006
- **Kategorie:** `Web & Security`
- **Architektur-Ebene:** `Layer 6: Security, Governance & KRITIS`
- **Impact-Score:** `88 / 100`

## Bedeutung in der SAP-Welt
Schutzmechanismus der SAP S/4HANA Gateway Foundation gegen Cross-Site Request Forgery. Verlangt vor schreibenden Aufrufen (POST/PATCH) ein dynamisches Token.

## Fundamentale technische Bedeutung (Real World)
Sicherheitsstandard (OWASP Top 10), der verhindert, dass unautorisierte Befehle im Namen eines authentifizierten Benutzers übertragen werden.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Wird im IFL_MDM_BP_Item_Processor nach ADR-007 zweistufig implementiert: GET-Call mit x-csrf-token: fetch + Cookie-Preservation, gefolgt vom Schreibaufruf.
