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

### The 'add' Element

The `add` element computes the mathematical sum of multiple child elements.

### Evaluation Rules

1. The `<add>` element MUST contain two or more child elements representing mathematical expressions or numerical representations.
2. The evaluation engine MUST process each child expression and calculate their sum sequentially.
3. If any child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

#### Mathematical Definition

The operation is evaluated iteratively over $n$ arguments as follows:

$$\text{add}(x_1, x_2, \dots, x_n) = \sum_{i=1}^{n} x_i$$

##### XML Example

The following example demonstrates how to add a character's base physical attribute value, their proficiency modifier, and a flat circumstantial magic equipment bonus:

```xml
<add>
  <attribute ref="strength"/>
  <attribute ref="proficiency_bonus"/>
  <integer value="2"/>
</add>
```

#### The 'subtract' Element

The `<subtract>` element computes the mathematical difference by sequentially subtracting subsequent child expressions from the first child element.

##### Evaluation Rules

1. The `<subtract>` element MUST contain two or more child elements representing mathematical expressions.
2. The evaluation engine MUST treat the first child expression as the base minuend ($x_1$).
3. The evaluation engine MUST sequentially subtract each subsequent child expression ($x_2, x_3, \dots, x_n$) from the accumulated value.
4. If any child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated iteratively over $n$ arguments as follows:

$$\text{subtract}(x_1, x_2, \dots, x_n) = x_1 - \sum_{i=2}^{n} x_i$$

##### XML Example

The following example demonstrates how to subtract an armor encumbrance penalty and an active wound modifier from a character's base speed attribute:

```xml
<subtract>
  <attribute ref="base_speed"/>
  <attribute ref="armor_encumbrance_penalty"/>
  <integer value="5"/>
</subtract>
```

#### The 'multiply' Element

The `<multiply>` element computes the mathematical product of multiple child expressions.

##### Evaluation Rules

1. The `<multiply>` element MUST contain two or more child elements representing mathematical expressions.
2. The evaluation engine MUST process each child expression and calculate their product sequentially.
3. If any child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated iteratively over $n$ arguments as follows:

$$\text{multiply}(x_1, x_2, \dots, x_n) = \prod_{i=1}^{n} x_i$$

##### XML Example

The following example demonstrates how to calculate a critical hit's double weapon damage by multiplying the weapon's base damage attribute by a flat modifier:

```xml
<multiply>
  <attribute ref="weapon_damage_base"/>
  <integer value="2"/>
</multiply>
```

#### The 'divide' Element

The `<divide>` element computes the mathematical quotient of two elements.

##### Evaluation Rules

1. The `<divide>` element MUST contain exactly two child elements representing mathematical expressions.
2. The children MUST be evaluated in strict positional order:
    * **Argument 1 (Dividend/Numerator):** The value to be divided.
    * **Argument 2 (Divisor/Denominator):** The value by which the dividend is divided.
3. If Argument 2 (the divisor) evaluates to zero (`0` or `0.0`), the evaluation engine MUST treat the execution as a critical runtime error and fail gracefully rather than returning an invalid or infinite value.
4. If either child expression evaluates to a non-numeric type, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated over exactly two arguments as follows:

$$\text{divide}(x, y) = \frac{x}{y} \quad \text{where } y \neq 0$$

##### XML Example

The following example demonstrates how a character's calculated base score (an attribute reference) is divided by a flat integer scaling factor to determine a final mechanical modifier (e.g., converting a raw ability score into a +2 modifier):

```xml
<divide>
  <attribute ref="strength_score"/>
  <integer value="2"/>
</divide>
```

#### The 'round' Element

The `<round>` element adjusts the precision of a nested numerical mathematical expression to a specified number of decimal places using a designated rounding strategy.

##### Evaluation Rules

1. The `<round>` element MUST contain exactly one child element representing a mathematical expression.
2. The `decimalPlaces` attribute is OPTIONAL and MUST default to `0` if omitted. It specifies the total number of digits to retain to the right of the decimal point. Negative values MUST be supported to round to the nearest tens, hundreds, etc.
3. The `method` attribute is OPTIONAL and MUST default to `half-up` if omitted. The evaluation engine MUST implement the rounding strategy specified by this attribute value.
4. If the child expression evaluates to a non-numeric type, the execution engine MUST treat the evaluation as an error.

##### Supported Rounding Methods

The `method` attribute restricts rounding behavior to the following predefined strategies:

* **`floor`**: Rounds the value down towards negative infinity.
* **`ceiling`**: Rounds the value up towards positive infinity.
* **`up`**: Rounds the value away from zero (magnifying its absolute magnitude).
* **`down`**: Rounds the value towards zero (truncating any remaining decimals).
* **`half-up`**: Rounds towards the nearest neighbor. If the discarded fractional part is exactly equidistant (a midpoint of `0.5`), the value is rounded up (away from zero for positive numbers). This represents standard textbook rounding.
* **`half-down`**: Rounds towards the nearest neighbor. If the discarded fractional part is a midpoint of `0.5`, the value is rounded down.
* **`half-even`**: Rounds towards the nearest neighbor. If the discarded fractional part is a midpoint of `0.5`, the value is rounded toward the nearest even digit. This is commonly referred to as Banker's Rounding.

##### XML Example

The following example shows how to calculate a standard d20 ability modifier ($\lfloor(\text{Score} - 10) / 2\rfloor$) by using the `floor` method to round a division calculation down to `0` decimal places:

```xml
<round decimalPlaces="0" method="floor">
  <divide>
    <subtract>
      <attribute ref="intelligence_score"/>
      <integer value="10"/>
    </subtract>
    <integer value="2"/>
  </divide>
</round>
```

#### The 'min' Element

The `<min>` element evaluates a sequence of child elements and returns the lowest numerical value among them. It allows for dynamic floor thresholds or choosing the least advantageous modifier in systems that utilize disadvantage mechanics.

##### Evaluation Rules

1. The `<min>` element MUST contain two or more child elements representing mathematical expressions.
2. The evaluation engine MUST process and evaluate every child expression sequentially.
3. The evaluation engine MUST compare the results and return the smallest numerical value derived from the child expressions.
4. If any child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated over $n$ arguments as follows:

$$\text{min}(x_1, x_2, \dots, x_n) = \min \{x_i \mid 1 \le i \le n\}$$

##### XML Example

The following example demonstrates choosing the lowest value between a character's maximum possible carry capacity and an encumbrance threshold modified by an active status effect:

```xml
<min>
  <attribute ref="max_carry_weight"/>
  <attribute ref="exhaustion_encumbrance_limit"/>
</min>
```

#### The 'max' Element

The `<max>` element evaluates a list of child expressions and returns the highest (maximum) numerical value among them.

##### Evaluation Rules

1. The `<max>` element MUST contain two or more child elements representing mathematical expressions.
2. The evaluation engine MUST process all child expressions and compare their resolved values.
3. The engine MUST return the maximum numerical value found among the evaluated children.
4. If any child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated over $n$ arguments as follows:

$$\text{max}(x_1, x_2, \dots, x_n) = \max(\{x_1, x_2, \dots, x_n\})$$

##### XML Example

The following example demonstrates how to determine a character's starting hit points by taking the maximum value between a flat class minimum threshold and a calculated dynamic formula (e.g., Constitution score + a die roll):

```xml
<max>
  <integer value="10"/>
  <add>
    <attribute ref="constitution_score"/>
    <integer value="4"/> </add>
</max>
```

### The 'clamp' Element

The `<clamp>` element restricts a numerical value so that it falls within a specified minimum and maximum range.

#### Evaluation Rules

1. The `<clamp>` element MUST contain exactly three child elements representing mathematical expressions.
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
<clamp>
  <!-- Argument 1: The value to test (e.g., a speed modifier attribute) -->
  <attribute ref="speed_modifier"/>

  <!-- Argument 2: The minimum allowed value -->
  <number value="0"/>

  <!-- Argument 3: The maximum allowed value -->
  <number value="5"/>
</clamp>
```

#### The 'abs' Element

The `<abs>` element calculates the absolute value of a nested mathematical expression, converting any negative numerical outcome into its non-negative equivalent representing its distance from zero.

##### Evaluation Rules

1. The `<abs>` element MUST contain exactly one child element representing a mathematical expression.
2. The evaluation engine MUST first fully evaluate the inner child expression.
3. If the evaluated child outcome is less than zero, the engine MUST multiply the result by `-1`. If the outcome is greater than or equal to zero, it MUST be returned unmodified.
4. If the child expression evaluates to a non-numeric type, or if the structural child node is completely missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated on a single argument as follows:

$$\text{abs}(x) = |x| = \begin{cases} x & \text{if } x \ge 0 \\ -x & \text{if } x < 0 \end{cases}$$

##### XML Example

The following example demonstrates how to find the absolute difference between two attributes (such as comparing a character's current high-score roll against a target threshold to find the flat margin of deviation regardless of success or failure):

```xml
<abs>
  <subtract>
    <attribute ref="character_roll_total"/>
    <attribute ref="target_difficulty_class"/>
  </subtract>
</abs>
```

#### The 'mod' Element

The `<mod>` element computes the mathematical remainder (modulo operation) of the division of the first child expression by the second child expression.

##### Evaluation Rules

1. The `<mod>` element MUST contain exactly two child elements representing mathematical expressions.
2. The children MUST be evaluated in strict positional order:
    * **Argument 1 (Dividend):** The base value to be divided.
    * **Argument 2 (Divisor):** The value to divide by.
3. If Argument 2 (the divisor) evaluates to `0`, the execution engine MUST treat it as a division-by-zero runtime error and fail gracefully.
4. If either child expression evaluates to a non-numeric type, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation evaluates the remainder $r$ of the division of dividend $a$ by divisor $n$:

$$\text{mod}(a, n) = a - n \cdot \left\lfloor \frac{a}{n} \right\rfloor$$

##### XML Example

The following example shows how to calculate a character's progress toward their next attribute increment milestone if thresholds occur at every 4 levels (e.g., computing `current_level mod 4`):

```xml
<mod>
  <attribute ref="current_level"/>
  <integer value="4"/>
</mod>
```

#### The 'ternary' Element

The `<ternary>` element provides inline conditional branching logic for mathematical expressions, mimicking a traditional if-then-else programming structure. It uses the outcome of a boolean evaluation to determine which mathematical path to calculate.

##### Evaluation Rules

1. The `<ternary>` element MUST contain exactly three structural child groupings in sequential order:
    * **Child 1**: Exactly one binary operation element or logical gate group.
    * **Child 2**: The mathematical expression to evaluate if Child 1 is `true`.
    * **Child 3**: The mathematical expression to evaluate if Child 1 is `false`.
2. The evaluation engine MUST process the nested binary operation (Child 1) first.
3. If the binary condition evaluates to `true` (or a boolean value equivalent to `1`), the engine MUST evaluate and return the result of Child 2. The engine MUST NOT evaluate Child 3.
4. If the binary condition evaluates to `false` (or a boolean value equivalent to `0`), the engine MUST evaluate and return the result of Child 3. The engine MUST NOT evaluate Child 2.
5. If any of the required child structures are missing, misplaced, or fail to evaluate, the engine MUST treat the execution tree as malformed and throw an evaluation error.

##### Mathematical Definition

The conditional operation maps to the following piecewise mathematical function:

$$f(\text{condition}, \text{trueBranch}, \text{falseBranch}) = \begin{cases} \text{trueBranch} & \text{if condition} = \text{true} \\ \text{falseBranch} & \text{if condition} = \text{false} \end{cases}$$

##### XML Example

The following example evaluates if a character's `is_bloodied` boolean attribute is `true`. If it evaluates to `true`, a flat rage bonus of `5` is applied; otherwise, it branches to a value of `0`:

```xml
<ternary xmlns="urn:xmpp:xtrpg:system:0">
  <attribute ref="is_bloodied"/>
  <integer value="5"/>
  <integer value="0"/>
</ternary>
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

Because game manifests can feature deeply nested calculation trees or trigger dynamic attribute database queries via `<attribute ref="..." />`, executing both branches is highly inefficient[cite: 4, 6]. By evaluating the binary condition first, the engine can completely skip parsing or looking up attributes contained within the unused branch. This safeguards application performance and ensures that any structural or evaluation errors present in an inactive conditional branch do not prematurely crash the engine runtime.

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
