---
id: digest/idempotenz
type: Architecture Concept
title: "Idempotente Nachrichtenverarbeitung (Idempotency Pattern)"
description: "Mathematische Eigenschaft: f(f(x)) = f(x). Ein zweiter Aufruf mit identischen Parametern führt exakt zum selben Endzustand wie der erste."
resource: btp://conciliamus/digest/idempotenz
tags: ["digest","concept","architektur","enterprise-erp-sap-btp","year-1960"]
status: verified
layer: 4
impact: 94
category: "Architektur"
year: "1960"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# Idempotente Nachrichtenverarbeitung (Idempotency Pattern)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `Idempotenz`
- **Meilenstein / Epoche:** Jahr 1960
- **Kategorie:** `Architektur`
- **Architektur-Ebene:** `Layer 4: Enterprise ERP & SAP BTP`
- **Impact-Score:** `94 / 100`

## Bedeutung in der SAP-Welt
Garantie, dass eine Nachricht auch bei mehrfacher Übertragung (z.B. nach Netzwerk-Retries) das Backend nicht korrumpiert oder Duplikate erzeugt.

## Fundamentale technische Bedeutung (Real World)
Mathematische Eigenschaft: f(f(x)) = f(x). Ein zweiter Aufruf mit identischen Parametern führt exakt zum selben Endzustand wie der erste.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Im Item Processor nach ADR-006 umgesetzt: Synchrone OData-Prüfung ($filter=SearchTerm1 eq externalId) entscheidet dynamisch zwischen POST (Neuanlage) und PATCH (Update).
