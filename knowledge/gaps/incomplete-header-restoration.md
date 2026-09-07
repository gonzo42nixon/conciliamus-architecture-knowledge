---
id: gaps/incomplete-header-restoration
type: Knowledge and Implementation Gap
title: "Nicht nachgewiesene Header-Wiederherstellung nach Request-Reply"
description: Der API-Key wird als Property gesichert, im exportierten Modell nach dem GET aber nicht explizit als Header wiederhergestellt.
resource: btp://conciliamus/gaps/incomplete-header-restoration
tags: [gap, camel, header, request-reply, api-key]
status: draft
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: references, target: /conformance/adr-012-property-conformance.md }
---

# Nicht nachgewiesene Header-Wiederherstellung

Vor POST und PATCH sollte ein expliziter Content Modifier den Header `APIKey` aus `property.sandboxApiKey` setzen. Alternativ muss ein Laufzeit-Trace belegen, dass der Header nach dem GET erhalten bleibt. Die gleiche Regel gilt künftig für CSRF-Token und Session-Cookie.
