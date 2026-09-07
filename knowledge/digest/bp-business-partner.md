---
id: digest/bp-business-partner
type: Architecture Concept
title: "Business Partner (Geschäftspartner)"
description: "Klassische relationale Stammdaten-Entität mit Rollen, Adressen und steuerlichen Identifikatoren."
resource: btp://conciliamus/digest/bp-business-partner
tags: ["digest","concept","sap-domaene","enterprise-erp-sap-btp","year-1998"]
status: verified
layer: 4
impact: 72
category: "SAP Domäne"
year: "1998"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# Business Partner (Geschäftspartner)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `BP Business Partner`
- **Meilenstein / Epoche:** Jahr 1998
- **Kategorie:** `SAP Domäne`
- **Architektur-Ebene:** `Layer 4: Enterprise ERP & SAP BTP`
- **Impact-Score:** `72 / 100`

## Bedeutung in der SAP-Welt
Zentrales Stammdatenobjekt in S/4HANA (Transaktion BP; ersetzt alte getrennte Debitoren/Kreditoren)

## Fundamentale technische Bedeutung (Real World)
Klassische relationale Stammdaten-Entität mit Rollen, Adressen und steuerlichen Identifikatoren.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Kernobjekt der Synchronisation: JSD-MDM Partner werden nach S/4HANA synchronisiert (Folie 01, 04, 10).
