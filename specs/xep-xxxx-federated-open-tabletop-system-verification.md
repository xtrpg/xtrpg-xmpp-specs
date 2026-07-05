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

This document defines a federated, content-addressed distribution standard. By utilizing structured Uniform Resource Names (URNs) mapped to cryptographic file fingerprints, this protocol allows decentralized game engines to verify, cache, and safely run game mechanics across a federated network.

## Requirements

TODO: Document fingerprint generation.

### Vendor Managed Systems

Defines the immutable foundational math laws, attribute pools, and sheet wireframes.

* **Format:** `urn:xmpp:xtrpg:sys:vendor:[vendor]:[game]:[edition]`
* **Example:** `urn:xmpp:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1` *(First Edition DaggerHeart by Darrington Press)*
* **Example:** `urn:xmpp:xtrpg:sys:vendor:com.wizards:dnd:5.5` *(Dungeons and Dragons 5.5 (2024) Edition by Wizards of the Coast)*

### Locally Managed Systems

Bypasses network validation entirely for homebrew testing or offline sessions.

* **Format:** `urn:xmpp:xtrpg:sys:local:[project-name]`
* **Example:** `urn:xmpp:xtrpg:sys:local:my-example-game`

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


### Verifying Against a Trusted Registry (Client to Server)

A user has obtained the system of rules for a Tabletop System and want to validate that their copy is inline with the official ruleset.

The client send an IQ-get stanza to the registry server, requesting the fingerprint for a specified game system of rules.

The following example shows a verification request being made to the registry server for a single game system.

```xml
<iq from='juliet@capulet.com/character'
    to='registry.verona.com'
    type='get'
    id='verify-1'>
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1' />
  </query>
</iq>
```

Upon a successful request the server will respond with the verification details.
The response is wrapped inside the same query stanza that was in the request.
The server include an `<item>` stanza with a urn matching the item from the request and adds the `status='active'` attribute.
Inside the item stanza, the server will include a `<fingerprint>` item for each fingerprint it knows corresponds to the requested game system.
The fingerprint includes information about:
- which cryptographic algorithm was used in its generation,
- a source of where it obtained the fingerprint from (allowed values are dns, registry and manual)
- the timestamp of when the registry recorded the fingerprint
- and if it was sourced from another server, the JID of the server it was sourced from.

```xml
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='result'
    id='verify-1'>
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
      <fingerprint algo='sha3-256'
                   source='manual'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>
  </query>
</iq>
```

Once the user has received a response from the registry, they can calculate their own fingerprint, from the system of rules they have on their system, and compare it against the response from the registry.
If the two fingerprints align, then the user can be sure that their copy of the system of rules is a match for what the Registry recognizes.


### Verifying Multiple Items In A Single Request (Client to Server)

The client is able to submit multiple `<item>` elements within the body of the query in order to bulk-verify a collection of systems.

```xml
<iq from='juliet@capulet.com/character'
    to='registry.verona.com'
    type='get'
    id='batch-verify-2'>
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:org.fitd:blades:1' />
    <item urn='urn:xmpp:xtrpg:sys:vendor:games.offworld:scum:1' />
    <item urn='urn:xmpp:xtrpg:sys:vendor:games.homebrew:hyperdrive-overhaul:2' />
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
    <item urn='urn:xmpp:xtrpg:sys:vendor:org.fitd:blades:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>fa721669b934ca495991b7852b855e3b0c44298fc1c149afbf4c8996fb92427ae</fingerprint>
    </item>
    <item urn='urn:xmpp:xtrpg:sys:vendor:games.offworld:scum:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>
    <item urn='urn:xmpp:xtrpg:sys:vendor:games.homebrew:hyperdrive-overhaul:2'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>ddd0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>
  </query>
</iq>
```

### Validating Against a Campaign Room (Client to Room Server)

A user has joined a campaign and wants to verify the system of rules that campaign is using.

The client sends an IQ stanza to the active campaign room to verify the exact rules authorized by the campaign owner.
The format of the request is similar to if the client was polling a truster registry.

```xml
<iq from='juliet@capulet.com/character'
    to='orchard@muc.verona.lit'
    type='get'
    id='muc-verona-verify-2'>
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1' />
  </query>

</iq>
```

The room server confirms the request item matches the GM's campaign setting.

```xml
<iq from='orchard@muc.verona.lit'
    to='juliet@capulet.com/character'
    type='error'
    id='muc-verona-verify-2'>
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='registry'
                   jid='registry.verona.com'
                   verified='2026-07-04T09:15:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
    </item>
  </query>
</iq>
```


### Community Registry Syncs Fingerprints With Venders Official Registry (Server to Server)

The Community Registry sends a request to the Vendors Registry for a collection of systems they are interested in.

```xml
<iq from='registry.capulet-community.com'
    to='registry.verona-official.com'
    type='get'
    id='community-verify-1'>
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.verona-official:fencing-mechanics:1' />
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.verona-official:shakespearean-insults:2' />
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
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.verona-official:fencing-mechanics:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-04T09:15:00Z'>fa721669b934ca495991b7852b855e3b0c44298fc1c149afbf4c8996fb92427ae</fingerprint>
    </item>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.verona-official:shakespearean-insults:2'
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
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.verona-official:fencing-mechanics:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='registry'
                   jid='registry.verona-official.com'
                   verified='2026-07-04T09:15:00Z'>fa721669b934ca495991b7852b855e3b0c44298fc1c149afbf4c8996fb92427ae</fingerprint>
    </item>
    <item urn='urn:xmppurn:xtrpg:sys:vendor:com.verona-official:shakespearean-insults:2'
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

### Responding to a request for a non-existent item.

In the event that the server does not contain the verification details of the item it the request they are responding to, then a standard inline XMPP Protocol Error Block is returned.

```xml
<iq from='registry.verona.com'
    to='juliet@capulet.com/character'
    type='error'
    id='verify-1'>
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.darringtonpress:daggerheart:1'
          status='error'>
      <error type='cancel'>
        <item-not-found xmlns='urn:ietf:params:xml:ns:xmpp-stanzas' />
        <text xmlns='urn:ietf:params:xml:ns:xmpp-stanzas' xml:lang='en'>
          The requested TTRPG asset uniform resource name or specific version footprint is unknown to this registry.
        </text>
      </error>
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
  <query xmlns='urn:xmpp:xtrpg:verify:0'>
    <item urn='urn:xmpp:xtrpg:sys:vendor:com.verona-houses:fencing-mechanics:1'
          status='active'>
      <fingerprint algo='sha256'
                   source='dns'
                   verified='2026-07-05T01:55:00Z'>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</fingerprint>
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

```xml
<?xml version='1.0' encoding='UTF-8'?>
<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'
           targetNamespace='urn:xmpp:xtrpg:verify:0'
           xmlns='urn:xmpp:xtrpg:verify:0'
           elementFormDefault='qualified'>

  <xs:element name='query'>
    <xs:complexType>
      <xs:sequence>
        <xs:element name='item' type='itemType' minOccurs='1' maxOccurs='unbounded'/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:complexType name='itemType'>
    <xs:sequence>
      <xs:element name='fingerprint' type='fingerprintType' minOccurs='0' maxOccurs='unbounded' />
      <xs:element name='error' type='errorType' minOccurs='0' maxOccurs='1'/>
    </xs:sequence>
    <xs:attribute name='urn' type='xs:anyURI' use='required'/>
    <xs:attribute name="status" type='statusType' />
  </xs:complexType>

  <xs:complexType name='fingerprintType'>
    <xs:simpleContent>
      <xs:extension base='xs:string'>
        <xs:attribute name='algo' type='xs:string' default='sha256'/>
        <xs:attribute name='source' type='sourceType' />
        <xs:attribute name='jid' type='xs:string' use='optional' />
        <xs:attribute name='verified' type='xs:dateTime' />
      </xs:extension>
    </xs:simpleContent>
  </xs:complexType>

  <xs:complexType name='errorType'>
    <xs:sequence>
      <xs:any namespace='urn:ietf:params:xml:ns:xmpp-stanzas' processContents='lax' minOccurs='1' maxOccurs='unbounded' />
    </xs:sequence>
    <xs:attribute name='type' type='xs:string' use='required'/>
  </xs:complexType>

  <xs:simpleType name="statusType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="error"/>
      <xs:enumeration value="active"/>
    </xs:restriction>
  </xs:simpleType>

  <xs:simpleType name="sourceType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="dns"/>
      <xs:enumeration value="registry"/>
      <xs:enumeration value="manual"/>
    </xs:restriction>
  </xs:simpleType>

</xs:schema>
```


## Acknowledgements

TODO

