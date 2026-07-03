# XTRPG XMPP Specification

An open, decentralized, and federated protocol framework for hosting Tabletop Role-Playing Games (TTRPGs) and Virtual Tabletops (VTTs) natively over the XMPP protocol.

This repository houses the formal specifications, XML schemas, and verification payloads for a multi-part ecosystem designed to liberate tabletop data from monolithic, proprietary cloud ecosystems.

## 🌌 The Vision
Our goal is to treat game mechanics exactly like the web: open, text-driven, and highly adaptable. By utilizing XMPP’s federated nature, players and GMs can host campaigns, manage character sheets, and share custom homebrew modules without relying on a single source of truth or paying recurring platform subscriptions.

## 🏗️ The XEP Architecture
To maintain absolute system-agnostic flexibility—supporting everything from D&D and Pathfinder to Daggerheart and indie homebrew, the protocol is split into five modular layers:

1. **XEP-0000: Federated Artifact and Schema Discovery.** 
2. **XEP-0001: TTRPG Core Mechanics Syntax and Evaluation.** The core mathematical grammar and XML token definitions for evaluating dice notation, resource costs, and game logic attributes.
3. **XEP-0002: TTRPG System Manifest and Schema Definition.** The architectural blueprints that define specific game systems (e.g., mapping the core stats, skill trees, and rule mechanics of D&D 5e vs. a custom system).
4. **XEP-0003: TTRPG Actor State and Profile Formats.** Live player state persistence, hosted locally or via personal PubSub/PEP nodes, ensuring players entirely own their character history.
5. **XEP-0004: TTRPG Content Compendium and Asset Schemas.** Content-addressable packages for items, spells, bestiaries, and adventure modules that dynamically map back to System Manifests.
6. **XEP-0005: TTRPG Session State and Campaign Management.**
7. **XEP-0006: TTRPG Spatial State and Real-Time VTT Sync.** The real-time session engine that choreographs Multi-User Chats (MUC), initiative tracking, dice rolling logs, and combat orchestration.

## 🌐 Unofficial Namespace Protocol

This project utilizes an unofficial, custom namespace to uniquely identify schemas, protocol rules, and game mechanics data structures.

* **Base URI:** `https://protocol.xenosnowfox.com/xtrpg/`

### URI Structure

All identifiers within this namespace follow a strict hierarchical structure:

```text
https://protocol.xenosnowfox.com/xtrpg/{category}/{version}/{resource}
```

## ⚙️ Docs-as-Code & Validation
This repository follows a strict **Docs-as-Code** philosophy. All protocol changes are verified automatically via CI/CD. Our automated GitHub Actions test all raw XML payload examples against our strict `.xsd` schemas on every pull request, ensuring our documentation is always verified, accurate, and completely production-ready.

## Reference Materials

- [RFC 3921](https://xmpp.org/rfcs/rfc3921.html)
- [XEPS](https://github.com/xsf/xeps)
- [XMPP Extensions](https://xmpp.org/extensions/index.html)
- [XEP-0045: Multi-User Chat](https://xmpp.org/extensions/xep-0045.html)
- [XEP-0471: Calendar Events](https://xmpp.org/extensions/xep-0471.html)
- [XEP-0030: Service Discovery](https://xmpp.org/extensions/xep-0030.html)
- [XEP-0313: Message Archive Management](https://xmpp.org/extensions/xep-0313.html)
- [XEP-0508: Forums](https://xmpp.org/extensions/xep-0508.html)
