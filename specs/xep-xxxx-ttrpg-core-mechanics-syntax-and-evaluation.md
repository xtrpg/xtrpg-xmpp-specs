---

Title: Open Tabletop Core Mechanics Syntax and Evaluation
Abstract: This specification provides documentation on defining a system of rules for tabletop game systems.
Number: XXXX
Status: Draft
Version: 0.0.0
Namespace: urn:xmpp:xtrpg:system:0

---

## Introduction

TODO

## Requirements

TODO

## Glossary

TODO

## Use Cases

TODO

## Business Rules

TODO

### Mathematical Expressions

### The 'clamp' Element

The `<clamp>` element restricts a numerical value so that it falls within a specified minimum and maximum range.

#### Evaluation Rules

1. The `<clamp>` element MUST contain exactly three child elements representing mathematical expressions[cite: 3].
2. The children MUST be evaluated in strict positional order:
    * **Argument 1 (Value):** The expression to be evaluated and potentially restricted.
    * **Argument 2 (Minimum):** The lower bound allowed for the expression.
    * **Argument 3 (Maximum):** The upper bound allowed for the expression.
3. If Argument 2 (Minimum) evaluates to a value greater than Argument 3 (Maximum), the evaluation engine MUST treat the schema as malformed or throw an evaluation error.

#### Mathematical Definition

The operation is evaluated as follows:

$$ \text{clamp}(x, \text{min}, \text{max}) = \max(\text{min}, \min(x, \text{max})) $$

#### XML Example

The following example clamps a character's calculated speed modifier (which could be negative or highly boosted) between a minimum of 0 and a maximum of 5:

```xml
<clamp xmlns="urn:xmpp:xtrpg:system:0">
  <!-- Argument 1: The value to test (e.g., a speed modifier attribute) -->
  <attribute ref="speed_modifier"/>

  <!-- Argument 2: The minimum allowed value -->
  <number value="0"/>

  <!-- Argument 3: The maximum allowed value -->
  <number value="5"/>
</clamp>
```

### Binary Operations

Binary operations are used to perform boolean evaluation logic, resolving to either `true` or `false`. They are primarily evaluated inside conditional structural blocks such as the `<ternary>` mathematical element.

#### Logical Gates (And, Or, Not, Nor, Xor, Xnor)

Logical gate elements evaluate their nested conditions recursively.

*   **`<and>`**: MUST contain two or more binary operations. Evaluates to `true` if, and only if, all child elements equate to `true`.
*   **`<or>`**: MUST contain two or more binary operations. Evaluates to `true` if one or more child elements equate to `true`.
*   **`<not>`**: MUST contain exactly one child mathematical operation. Evaluates to `true` if the child expression evaluates to `false` or `0`.
*   **`<nor>`**: MUST contain two or more binary operations. Evaluates to `true` if all child elements equate to `false`.
*   **`<xor>`**: MUST contain two or more binary operations. Evaluates to `true` if an odd number of child elements equate to `true`.
*   **`<xnor>`**: MUST contain two or more binary operations. Evaluates to `true` if an even number of child elements equate to `true`.

#### Comparison Operators

Comparison operators evaluate numerical mathematical operations to produce a boolean result.

##### The '<greater-than>' and '<less-than>' Elements

These elements compare exactly two mathematical expressions. They accept an optional `boundary` attribute to define inclusive or exclusive threshold boundaries.

*   **Argument 1**: The primary expression to evaluate.
*   **Argument 2**: The baseline expression compared against Argument 1.

The `boundary` attribute MUST support the following values:
*   **`exclusive` (Default)**: The threshold is strict comparison ($>$ or $<$).
*   **`inclusive`**: The threshold includes equal boundaries ($\ge$ or $\le$).

##### The '<equals>' and '<not-equals>' Elements

*   **`<equals>`**: MUST contain two or more mathematical expressions. Evaluates to `true` if all child expression evaluations result in the identical numerical value.
*   **`<not-equals>`**: MUST contain two or more mathematical expressions. Evaluates to `true` if any child expression value differs from the others.

#### Example: Ternary Choice Using Binary Operations

The following example evaluates if a character's `strength` attribute is greater than or equal to 15. If true, it returns a bonus value of `2`, otherwise it returns `0`:

```xml
<ternary xmlns="urn:xmpp:xtrpg:system:0">
  <!-- 1st Child: The Binary Operation Condition -->
  <greater-than boundary="inclusive">
    <attribute ref="strength"/>
    <integer value="15"/>
  </greater-than>

  <!-- 2nd Child: Expression evaluated if TRUE -->
  <integer value="2"/>

  <!-- 3rd Child: Expression evaluated if FALSE -->
  <integer value="0"/>
</ternary>
```

#### The 'ternary' Element

The `<ternary>` element provides conditional branching logic for mathematical expressions.

##### Evaluation Rules
1. The `<ternary>` element MUST contain exactly three child components: one binary operation group followed by exactly two mathematical expressions.
2. The implementation MUST evaluate the child binary operation first.
3. If the binary operation evaluates to `true`, the implementation MUST evaluate and return the outcome of the second child element (the truth branch). The third child element MUST NOT be evaluated.
4. If the binary operation evaluates to `false`, the implementation MUST evaluate and return the outcome of the third child element (the false branch). The second child element MUST NOT be evaluated.

TODO

## Implementation Notes

TODO

## Implementation Notes

### Short-Circuit Evaluation of Ternary Expressions
When building an evaluation engine for the `<ternary>` element, developers SHOULD implement short-circuit (lazy) evaluation.

Because game manifests can feature deeply nested calculation trees or trigger dynamic attribute database queries via `<attribute ref="..." />`, executing both branches is highly inefficient[cite: 4, 6]. [cite_start]By evaluating the binary condition first, the engine can completely skip parsing or looking up attributes contained within the unused branch. This safeguards application performance and ensures that any structural or evaluation errors present in an inactive conditional branch do not prematurely crash the engine runtime.

## Accessibility Considerations

TODO

## Internationalization Considerations

TODO

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
