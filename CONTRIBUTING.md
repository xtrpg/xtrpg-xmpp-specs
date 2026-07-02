Thank you for contributing to this XMPP extension ecosystem! This project uses a Docs-as-Code philosophy. We manage specifications, validation schemas, and sample payloads like software assets.

Please read through this guide to understand our repository structure, formatting requirements, and automated validation pipeline before opening a Pull Request.

## Repository Layout

All additions and modifications must align with our structured repository blueprint. Do not introduce loose root-level design documents.

- `/specs` Contains the draft protocol specifications within as Markdown files.
- `/schemas` Contains the formal XML Schema Definitions (`.xsd`) defining the structure syntax.
- `/examples/{schema-name}` Contains isolated XML snippet files used to verify protocol examples against the schemas.
- `/scripts` Contains local build automation tool scripts, writtin in Python.

## Structuring Specification Files

To ensure our Markdown specifications can automatically translate into official XEP XML Templates when we are ready to publish, all specification files must strictly follow this structural format:

### 1. Mandatory YAML Front Matter

Every specification Markdown file must begin with a YAML front-matter block enclosed by triple-dashed lines (---). Our automated compilation pipeline uses this metadata to construct the header of the XEP XML document.

```yml
---
Title: Rules Engine
Abstract: ABSTRACT
---
```

### 2. Specification Body Layout

Use standard Markdown headings hierarchically. When compiling to the XEP format, headings translate directly to <section1>, <section2>, etc.

Use ## (H2) for primary architectural sections (e.g., Introduction, Requirements, Protocol).

Use ### (H3) for distinct protocol operations or element types.

### 3. XML Examples Block Syntax

All protocol example snippets within the specification must be isolated using standard Markdown code fences. You must explicitly label the code fence language as xml.

Additionally, ensure every XML example block is completely self-contained, specifies its appropriate namespace attributes, and is syntactically well-formed:

````markdown
### 3.1 Active Character Announcement

When a user selects or swaps their active character, they MUST emit a standard MUC presence containing the `<active-character/>` extension:

```xml
<presence to='campaign_room@muc.dnd-server.lit/Player'>
  <x xmlns='[http://jabber.org/protocol/muc'/](http://jabber.org/protocol/muc'/)>
  <active-character xmlns='[https://yourdomain.tld/protocol/dnd-campaign](https://yourdomain.tld/protocol/dnd-campaign)'
                    id='char-uuid-8f3b-4c21-99a1' />
</presence>
```

````
