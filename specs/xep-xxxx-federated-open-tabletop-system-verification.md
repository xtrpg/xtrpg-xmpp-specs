---

Title: Federated Open Tabletop System Verification
Abstract: This specification provides documentation on verifying the legitimacy of a Tabletop system of rules.
Number: XXXX
Status: Draft
Version: 0.0.0
Namespace: urn:xmpp:xtrpg:verify:0

---

## Introduction

Virtual Tabletops (VTTs) and digital character managers traditionally operate inside isolated, centralized silos. When a game system receives a balance patch, an item typo fix, or a new setting book release, data models drift out of sync across players, causing structural friction at the table.

This document defines a federated, content-addressed distribution standard. By utilizing structured Uniform Resource Names (URNs) mapped to cryptographic file fingerprints, this protocol allows decentralized game engines to discover, verify, cache, and safely run game mechanics, character sheets, item catalogs, and adventure modules across a federated network.

## Requirements

TODO: Document system urn naming.

### Vendor Managed Systems

Defines the immutable foundational math laws, attribute pools, and sheet wireframes.

* **Format:** `urn:xtrpg:sys:vendor:[vendor]:[game]:[edition]`
* **Example:** `urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1` *(First Edition DaggerHeart by Darrington Press)*
* **Example:** `urn:xtrpg:sys:vendor:com.wizards:dnd:5.5` *(Dungeons and Dragons 5.5 (2024) Edition by Wizards of the Coast)*

### Locally Managed Systems

Bypasses network validation entirely for homebrew testing or offline sessions.

* **Format:** `urn:xtrpg:sys:local:[project-name]`
* **Example:** `urn:xtrpg:sys:local:my-example-game`

TODO: Document a system of generating a fingerprint hash.

TODO: DNS TXT records

```
v=xtrpg:0 sys=daggerheart:1 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

- `v=xtrpg:0` Indicates that this is a XTRPG based record
- `sys=daggerheart:1` Indicates the name of the game system and edition, this should match the "game" and "edition" segments of the system urn.
- `sha256=...` Is the computed hash of the game system.

## Glossary

TODO: Homebrew

TODO: User

TODO: Vendor

TODO: System of Rules

TODO: Trusted Registry

## Use Cases


### Verifying Against a Trusted Registry

A user has obtained the system of rules for a Tabletop System and want to validate that their copy is inline with the official ruleset.

The client send an IQ-get stanza to the registry server, requesting the fingerprint for a specified game system of rules.

```xml
<iq from='juliet@capulet.com/character'
    to='registry.verona.com'
    type='get'
    id='verify-1'>

  <!-- Set the custom query namespace to match our platform -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <!-- Provide one or more items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1' />
  </query>

</iq>
```

Upon a successful request the server will respond with the verification details.

```xml
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='result'
    id='verify-1'>

  <!-- Set the custom query namespace to match our platform -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- Provide one or more items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          fingerprint='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
          algo='sha256'
          status='active' />

    </item>
  </query>

</iq>
```

In the event that the server does not contain the verification details of a given system then a standard inline XMPP Protocol Error Block is returned.

```xml
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='error'
    id='verify-1'>

  <!-- The original query block is echoed back to preserve context -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- Provide one or more items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          status='error'>

      <!-- Standard XMPP Protocol Error Block -->
      <error type='cancel'>
        <!-- Authoritative XMPP error condition primitive -->
        <item-not-found xmlns='urn:ietf:params:xml:ns:xmpp-stanzas' />

        <!-- Application-specific text hint for developer diagnostics -->
        <text xmlns='urn:ietf:params:xml:ns:xmpp-stanzas' xml:lang='en'>
          The requested TTRPG asset uniform resource name or specific version footprint is unknown to this registry.
        </text>
      </error>

    </item>
  </query>

</iq>
```

### Verifying Multiple Items In A Single Request

The client is able to submit multiple `<item>` elements within the body of the query in order to bulk-verify a collection of systems.

```xml
<iq from='juliet@capulet.com/character'
    to='registry.verona.com'
    type='get'
    id='batch-verify-2'>

  <!-- Set the custom query namespace to match our platform -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- Provide multiple items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:org.fitd:blades:1' />
    <item urn='urn:xtrpg:sys:vendor:games.offworld:scum:1' />
    <item urn='urn:xtrpg:sys:vendor:games.homebrew:hyperdrive-overhaul:2' />
  </query>

</iq>
```

The server must respond with the verification details for each item it has data for, returning an inline error block for those that it does not.

```xml
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='result'
    id='batch-verify-2'>

  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- SUCCESS 1: This system is verified -->
    <item urn='urn:xtrpg:sys:vendor:org.fitd:blades:1'
          fingerprint='fa721669b934ca495991b7852b855e3b0c44298fc1c149afbf4c8996fb92427ae'
          algo='sha256'
          status='active'>
      <mirrors>
        <mirror provider='https://github.com/xtrpg-hub/fitd-framework-1e-package/releases/download/v1.0.0/dist.xml' priority='1' />
      </mirrors>
    </item>

    <!-- SUCCESS 2: This system is verified -->
    <item urn='urn:xtrpg:sys:vendor:games.offworld:scum:1'
          fingerprint='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
          algo='sha256'
          status='active'>
      <mirrors>
        <mirror provider='https://github.com/xtrpg-hub/offworld-scum-and-villainy-1e-package/releases/download/v1.0.0/dist.xml' priority='1' />
      </mirrors>
    </item>

    <!-- FAILURE 3: This system does not exist on this registry -->
    <item urn='urn:xtrpg:sys:vendor:games.homebrew:hyperdrive-overhaul:2'
          status='error'>

      <!-- Inline error block scopes the failure strictly to this asset -->
      <error type='cancel'>
        <!-- Standard XMPP error condition primitive -->
        <item-not-found xmlns='urn:ietf:params:xml:ns:xmpp-stanzas' />
        <text xmlns='urn:ietf:params:xml:ns:xmpp-stanzas' xml:lang='en'>
          Module not found in this registry.
        </text>
      </error>

    </item>

  </query>
</iq>
```

### Validating Against a Campaign Room

A user has joined a campaign and want to verify the system of rules that campaign is using.

### Vendor Submits Their System to a Trusted Registry

A vendor has created or update the System of Rules for their Tabletop System. The vendor wants to submit their system's fingerprint to a Trusted Registry so that users may validate their copies against.



## Business Rules

TODO

## Implementation Notes

TODO

## Accessibility Considerations

TODO

## Internationalization Considerations

TODO: Possibility of disconnected systems. Allowing the same game to have different System of Rules.

## Security Considerations

TODO

## Privacy Considerations

TODO

## IANA Considerations

TODO

## XMPP Registrar Considerations

TODO

## Design Considerations

TODO

## XML Schema

TODO

## Acknowledgements

TODO

