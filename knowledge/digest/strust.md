---
id: digest/strust
type: Architecture Concept
title: "Trust Manager / Zertifikatsverwaltung (SAP GUI)"
description: "Integrierter X.509 TrustStore und Keystore für TLS-Zertifikatsketten und Gegenstellen-Validierung."
resource: btp://conciliamus/digest/strust
tags: ["digest","concept","sap-transaktion","enterprise-erp-sap-btp"]
status: verified
layer: 4
impact: 65
category: "SAP Transaktion"
year: ""
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# Trust Manager / Zertifikatsverwaltung (SAP GUI)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `STRUST`
- **Meilenstein / Epoche:** Klassisch / Zeitlos
- **Kategorie:** `SAP Transaktion`
- **Architektur-Ebene:** `Layer 4: Enterprise ERP & SAP BTP`
- **Impact-Score:** `65 / 100`

## Bedeutung in der SAP-Welt
Verwaltung von SSL-Client- und Server-PSEs, Wurzelzertifikaten und Public Keys im SAP-System

## Fundamentale technische Bedeutung (Real World)
Integrierter X.509 TrustStore und Keystore für TLS-Zertifikatsketten und Gegenstellen-Validierung.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Hier werden die BTP-Zertifikate hinterlegt, um verschlüsselte HTTPS/mTLS-Aufrufe abzusichern (Folie 07).
