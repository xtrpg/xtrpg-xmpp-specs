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
<!-- The user Juliet is requesting verification information from a registry server -->
<iq from='juliet@capulet.com/character'
    to='registry.verona.com'
    type='get'
    id='verify-1'>

  <!-- Juliet's request is wrapped within a Query stanza. -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- Juliet is requesting the verification information for Darrington Press's Daggerheart 1st Edition system of rules. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1' />
  </query>

</iq>
```

Upon a successful request the server will respond with the verification details.

```xml
<!-- The registy responds back to Juliet with the verification information. -->
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='result'
    id='verify-1'>

  <!-- The Registry's response is wrapped in a Query stanza. -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- The Registry is returninf the verification information for the URN that Juliet requested. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          status='active'>
      <!-- At a minimum we recommend providing a sha256 fingerprint -->
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>

      <!-- The Registry may also return additional fingerprints, that utilize alternative algorithms. -->
      <fingerprint algo='sha3-256'
                   source='manual'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>

  </query>

</iq>
```

Once the user has received a response from the registry, they can calculate their own fingerprint, from the system of rules they have on their system, and compare it against the response from the registry. If the two fingerprints align, then the user can be sure that their copy of the system of rules is a match for what the Registry recognizes.




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
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>fa721669b934ca495991b7852b855e3b0c44298fc1c149afbf4c8996fb92427ae</fingerprint>
    </item>

    <!-- SUCCESS 2: This system is verified -->
    <item urn='urn:xtrpg:sys:vendor:games.offworld:scum:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
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

A user has joined a campaign and wants to verify the system of rules that campaign is using.

The client sends an IQ stanza to the active campaign room to verify the exact rules authorized by the campaign owner. The format of the request is similar to if the client was polling a truster registry.

```xml
<iq from='juliet@capulet.com/character'
    to='orchard@muc.verona.lit'
    type='get'
    id='muc-verona-verify-2'>

  <!-- Set the custom query namespace to match our platform -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <!-- Provide one or more items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1' />
  </query>

</iq>
```

The room server confirms the request item matches the GM's campaign setting.

```xml
<iq from='orchard@muc.verona.lit'
    to='juliet@capulet.com/character'
    type='error'
    id='muc-verona-verify-2'>

  <!-- The original query block is echoed back to preserve context -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- Provide one or more items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          status='active'>
      <!-- At a minimum we recommend providing a sha256 fingerprint -->
      <fingerprint algo='sha256'
                   source='registry'
                   jid='registry.verona.com'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>

      <!-- The specification allows for returning multiple fingerprint based on different algorithms -->
      <fingerprint algo='sha3-256'
                   source='registry'
                   jid='registry.verona.com'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>

  </query>

</iq>
```



### Vendor Creates a Public DNS Record

A vendor has created or update the System of Rules for their Tabletop System. The vendor wants to submit their system's fingerprint to a Trusted Registry so that users may validate their copies against.

The vendor will first need to generate a URN for their system of rules. Following the standard this might look like the following:

```plaintext
urn:xtrpg:sys:vendor:com.verona-houses:fencing-mechanics:1

Vendor: com.verona-houses
Game System: fencing-mechanics
Edition: 1

Extracted Authority Domain:  verona-houses.com
Target DNS SEC host:         _xtrpg.verona-houses.com
```

Since we use a reverse domain for the vendor identifier, we can assume the DNS server is located at `verona-houses.com`. The vendor can then create a TXT record on their DNS server to indicate their ownership and point to the fingerprint of their verified system of rules content.

```plaintext
_xtrpg.verona-houses.com. IN TXT "v=xtrpg:0 sys=fencing-mechanics:1 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Once this is uploaded, any client, server or registry can query the secure public domain for their fingerprint records and be able to record, or propagate, the officially supported fingerprint for that game system. A server that collects this DNS record, updates their local copy , sets the source as `dns` and records the UTC timestamp of when they obtained it.

```xml
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='result'
    id='verify-1'>

  <!-- Set the custom query namespace to match our platform -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- Provide one or more items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:com.verona-houses:fencing-mechanics:1'
          status='active'>

      <!-- At a minimum we recommend providing a sha256 fingerprint -->
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-05T01:55:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>

    </item>

  </query>

</iq>
```

### Community Registry Syncs Fingerprints With Venders Official Registry

The Community Registry sends a request to the Vendors Registry for a collection of systems they are interested in.

```xml
<iq from='registry.capulet-community.com'
    to='registry.verona-official.com'
    type='get'
    id='community-verify-1'>

  <!-- Set the custom query namespace to match our platform -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- Provide multiple items for the systems the user wants to have returned. -->
    <item urn='urn:xtrpg:sys:vendor:com.verona-official:fencing-mechanics:1' />
    <item urn='urn:xtrpg:sys:vendor:com.verona-official:shakespearean-insults:2' />
  </query>

</iq>
```

As per any normal request the Vendor Registry responds with the fingerprints for each of these systems.


```xml
<iq from='registry.verona-official.com'
    to='registry.capulet-community.com'
    type='result'
    id='community-verify-1'>

  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- SUCCESS 1: This system is verified -->
    <item urn='urn:xtrpg:sys:vendor:com.verona-official:fencing-mechanics:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>fa721669b934ca495991b7852b855e3b0c44298fc1c149afbf4c8996fb92427ae</fingerprint>
    </item>

    <!-- SUCCESS 2: This system is verified -->
    <item urn='urn:xtrpg:sys:vendor:com.verona-official:shakespearean-insults:2'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>

  </query>
</iq>
```

Lastly the Community Registry updates their records to indicate their fingerprints were obtained from another registry, the JID of that registry and the timestamp of when they resolved that request.

```xml
<iq from='registry.capulet-community.com'
    to='juliet@capulet.com/character'
    type='result'
    id='batch-verify-2'>

  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- SUCCESS 1: This system is verified -->
    <item urn='urn:xtrpg:sys:vendor:com.verona-official:fencing-mechanics:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='registry'
                   jid='registry.verona-official.com'
                   verified='2026-07-04T09:15:00Z'>fa721669b934ca495991b7852b855e3b0c44298fc1c149afbf4c8996fb92427ae</fingerprint>
    </item>

    <!-- SUCCESS 2: This system is verified -->
    <item urn='urn:xtrpg:sys:vendor:com.verona-official:shakespearean-insults:2'
          status='active'>
      <fingerprint algo='sha256'
                   source='registry'
                   jid='registry.verona-official.com'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>

  </query>
</iq>
```

## Business Rules

TODO

## Implementation Notes

### Respnding to a request for a non-existant item.

In the event that the server does not contain the verification details of the item it the request they are responding to, then a standard inline XMPP Protocol Error Block is returned.

```xml
<!-- The Registry to replying to a request from Juliet. -->
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='error'
    id='verify-1'>

  <!-- The Registry must wrap its response within a Query stanza. -->
  <query xmlns='urn:xmpp:xtrpg:verify:0'>

    <!-- The Registry sends back an item for the requested URN with an error status. -->
    <item urn='urn:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          status='error'>

      <!-- The Registry must also include a Standard XMPP Protocol Error Block with details about the issue hat occurred. -->
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

