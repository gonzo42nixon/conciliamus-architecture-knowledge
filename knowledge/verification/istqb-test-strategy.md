---
id: verification/istqb-test-strategy
type: Test Evidence
title: ISTQB Teststrategie & Testfallmatrix
description: Systematische Testabdeckung nach ISTQB CTFL Prinzipien (Äquivalenzklassen, Grenzwertanalyse, Fehlerfall-Prüfung).
resource: btp://conciliamus/evidence/istqb-strategy
tags: [evidence, istqb, testing, test-matrix, qa]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: verifies, target: /architecture/existence-check-and-routing.md }
  - { type: verifies, target: /architecture/resilience-and-dead-letter.md }
sources:
  - id: test-evidences
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/test_evidences.md
    title: Prüfungs- & Testnachweise
    author: "Dieter Rüffler"
---

# ISTQB Teststrategie & Testfallmatrix

## Angewandte Testverfahren
1. **Äquivalenzklassenbildung:**
   - Klasse A: Existierender Partner im S/4HANA (Treffermenge = 1) ➔ Erwartung: PATCH
   - Klasse B: Neuer Partner (Treffermenge = 0) ➔ Erwartung: POST
   - Klasse C: Mehrdeutiger Partner (Treffermenge > 1) ➔ Erwartung: FAILED_BUSINESS
2. **Grenzwertanalyse:**
   - Maximale Feldlängen (`externalId` 20 Zeichen, `company` 40 Zeichen).
   - ISO-2 Ländercodes (exakt 2 Zeichen, Validierung von `DE` vs. ungültigen Kürzeln).
3. **Negative Testing:**
   - Fehlende Pflichtfelder, Syntaxfehler in E-Mail-Adresse, abweichender Sandbox-Status.

## Testfallmatrix

| # | Testfall | Input-Daten | Erwartetes Ergebnis | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Existierender Partner 1 | `CUST15` | GET Treffer: `1000015` ➔ PATCH | ✅ Pass |
| **TC-02** | Existierender Partner 2 | `BECHTLE AG` | GET Treffer: `1000020` ➔ PATCH | ✅ Pass |
| **TC-03** | Existierender Partner 3 | `XYZ-PEPPOL` | GET Treffer: `1000035` ➔ PATCH | ✅ Pass |
| **TC-04** | Neuanlage Partner | `JSD-BP-100001` | GET 0 Treffer ➔ POST Deep Insert | ✅ Pass |
| **TC-05** | Ungültige E-Mail | `invalid-mail` | `FAILED_BUSINESS`, kein Retry | ✅ Pass |
| **TC-06** | Ungültiger Ländercode | `DEU` statt `DE` | `FAILED_BUSINESS`, kein Retry | ✅ Pass |
| **TC-07** | Technischer Timeout | Mock HTTP 504 | `FAILED_TECHNICAL`, Data Store DLQ | ✅ Pass |
