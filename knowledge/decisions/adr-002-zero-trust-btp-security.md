---
id: decisions/adr-002-zero-trust-btp-security
type: Decision Record
title: "ADR-002: Zero-Trust & BTP PaaS Security Architecture"
description: Einsatz der SAP BTP Integration Suite als Managed PaaS und Etablierung einer strikten Zero-Trust-Sicherheitsarchitektur ab Sekunde Null (OAuth2, XSUAA, TLS 1.3, Vault).
resource: btp://conciliamus/decisions/ADR-002
tags: [adr, architecture-decision, security, zero-trust, oauth2, xsuaa, tls13, credential-store, btp-paas]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T22:45:00Z"
relations:
  - { type: implements, target: /architecture/dual-iflow-pattern.md }
  - { type: dependsOn, target: /iflows/batch-receiver-iflow.md }
sources:
  - id: btp-sec-guide
    resource: https://help.sap.com/docs/btp/sap-business-technology-platform/security
    title: SAP BTP Security Guide & Best Practices
    author: "SAP SE"
---

# ADR-002: Zero-Trust & BTP PaaS Security Architecture

## Status
Akzeptiert (Accepted)

## Kontext
Die Conciliamus GmbH integriert Geschäftspartnerdaten für Krankenhäuser und Pflegeeinrichtungen der Johannesstift Diakonie. Diese Daten unterliegen als Teil der kritischen Gesundheits- und Sozialinfrastruktur strengsten regulatorischen Vorgaben (DSGVO, BSI IT-Grundschutz, ISO 27001). Konventionelle Integrationsarchitekturen mit statischer Basic Authentication (Benutzername/Passwort im Klartext), offenen Firewall-Ports oder unverschlüsselten Endpunkten stellen ein untragbares Sicherheitsrisiko dar.

## Entscheidung
Wir haben entschieden, die Integrationslösung auf der **SAP BTP Integration Suite als Managed PaaS** mit einer kompromisslosen **Zero-Trust-Architektur** zu betreiben:

1. **PaaS statt On-Premises-Infrastruktur:**
   - Nutzung der cloudbasierten SAP BTP Integration Suite. Sicherheits-Patches, Betriebssystem- und Java-Laufzeitupdates sowie Hochverfügbarkeit werden vollautomatisch von SAP gemanagt.
2. **Strikte OAuth2-Authentifizierung (Zero Basic Auth):**
   - Jeder Inbound-Aufruf an den `IFL_MDM_BP_Batch_Receiver` erfordert ein gültiges OAuth2-Bearer-Token (Client Credentials Grant via SAP BTP XSUAA Service-Instanz).
   - Basic Authentication ist tenant-weit deaktiviert.
3. **Transportverschlüsselung:**
   - Zwingender Einsatz von TLS 1.3 mit modernen Cipher Suites und Perfect Forward Secrecy (PFS).
4. **Credential Isolation im BTP Security Material Vault:**
   - Zugangsdaten für das Zielsystem SAP S/4HANA werden niemals im iFlow-Quellcode oder im Git hinterlegt, sondern liegen verschlüsselt im SAP BTP Keystore / Security Material Store.

## Konsequenzen
- **Positiv:**
  - Höchste Audit-Konformität ab Sekunde Null (KRITIS- und DSGVO-sicher).
  - Automatisierte Token-Expirierung verhindert Missbrauch kompromittierter Anmeldedaten.
  - Zero-Maintenance für Server- und Patch-Management.
- **Negativ / Trade-offs:**
  - Quellsysteme müssen zwingend den vorgelagerten OAuth2-Token-Abruf (Handshake) unterstützen.
