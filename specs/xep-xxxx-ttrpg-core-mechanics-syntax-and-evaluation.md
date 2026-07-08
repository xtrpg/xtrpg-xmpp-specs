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
<ternary>
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
*   **`<xor>`**: MUST contain two or more binary operations. Evaluates to `true` if an odd number of child elements equate to `true`.
*   **`<nand>`**: MUST contain two or more binary operations. Evaluates to `true` if one or more child elements equate to `false`.
*   **`<nor>`**: MUST contain two or more binary operations. Evaluates to `true` if all child elements equate to `false`.
*   **`<xnor>`**: MUST contain two or more binary operations. Evaluates to `true` if an even number of child elements equate to `true`.
*   **`<not>`**: MUST contain exactly one child mathematical operation. Evaluates to `true` if the child expression evaluates to `false` or `0`.



#### The 'and' Element

The `<and>` element performs a logical conjunction across multiple child binary operations. It resolves to a boolean value.

##### Evaluation Rules

1. The `<and>` element MUST contain two or more child elements belonging to the binary operations group.
2. The evaluation engine MUST evaluate the child operations.
3. If all child operations evaluate to `true` (or a non-zero numerical value if implicit conversion is supported), the `<and>` element MUST return `true`.
4. If any child operation evaluates to `false` (or `0`), the `<and>` element MUST immediately return `false`.
5. The evaluation engine SHOULD implement short-circuit evaluation; if any child expression evaluates to `false`, subsequent child expressions within the same `<and>` block do not need to be processed.

##### Mathematical Definition

The operation is evaluated iteratively over $n$ boolean arguments as follows:

$$\text{and}(b_1, b_2, \dots, b_n) = b_1 \land b_2 \land \dots \land b_n$$

##### XML Example

The following example demonstrates how to check if a character has both an active stealth state and a specific rogue talent before applying an incoming modifier:

```xml
<and>
  <attribute ref="is_stealthed"/>

  <attribute ref="has_ambush_talent"/>
</and>
```



#### The 'or' Element

The `<or>` element performs a logical disjunction (OR operation) across multiple child conditions. It evaluates to `true` if at least one of its child expressions resolves to `true`.

##### Evaluation Rules

1. The `<or>` element MUST contain two or more child elements representing binary operations.
2. The evaluation engine MUST process the child elements sequentially.
3. If any child element evaluates to `true`, the engine MAY short-circuit and immediately return `true` without evaluating any remaining child elements.
4. If all child elements evaluate to `false`, the element MUST return `false`.

##### Mathematical Definition

The operation is evaluated over $n$ boolean arguments as follows:

$$\text{or}(b_1, b_2, \dots, b_n) = b_1 \lor b_2 \lor \dots \lor b_n$$

##### XML Example

The following example checks if a character satisfies either condition to gain access to a specific feat or ability: having a `strength` attribute greater than or equal to 16, OR possessing a specialized boolean attribute flag named `bypasses_strength_requirement`:

```xml
<or>
  <greater-than boundary="inclusive">
    <attribute ref="strength"/>
    <integer value="16"/>
  </greater-than>
  <attribute ref="bypasses_strength_requirement"/>
</or>
```



#### The 'xor' Element

The `<xor>` element performs an exclusive-OR logical evaluation across multiple child binary operations.

##### Evaluation Rules

1. The `<xor>` element MUST contain two or more child elements representing binary operations.
2. The evaluation engine MUST evaluate all child binary operations.
3. The element MUST evaluate to `true` if, and only if, an odd number of child elements evaluate to `true`. If an even number of child elements evaluate to `true` (including zero), the element MUST evaluate to `false`.
4. If any child expression fails to resolve to a valid boolean state, the execution engine MUST treat the evaluation as an error.

##### Mathematical / Logical Definition

The operation is evaluated over $n$ boolean arguments as follows:

$$\text{xor}(b_1, b_2, \dots, b_n) = \left( \sum_{i=1}^{n} \text{int}(b_i) \right) \pmod 2 \equiv 1$$

*(Where $\text{int}(true) = 1$ and $\text{int}(false) = 0$.)*

##### XML Example

The following example returns `true` if a character has *either* the "sneaking" status or the "invisible" status active, but evaluates to `false` if they have both or neither:

```xml
<xor>
  <attribute ref="is_sneaking"/>
  <attribute ref="is_invisible"/>
</xor>
```


#### The 'nand' Element

The `<nand>` element (Not-AND) performs a negative-conjunction logical operation across multiple child evaluations. It evaluates to `true` if at least one of its child elements evaluates to `false`.

##### Evaluation Rules

1. The `<nand>` element MUST contain two or more child elements representing binary operations.
2. The evaluation engine MUST evaluate the child operations. If any child element evaluates to `false` (or a numerical `0`), the `<nand>` expression MUST immediately short-circuit and return `true`.
3. The `<nand>` element MUST only evaluate to `false` if every single nested child operation evaluates to `true`.

##### Mathematical Definition

The operation is evaluated over $n$ logical arguments as follows (equivalent to negating an AND gate):

$$\text{nand}(b_1, b_2, \dots, b_n) = \neg(b_1 \land b_2 \land \dots \land b_n)$$

##### XML Example

The following example returns `true` unless a character is *both* wearing heavy armor and lacks the required strength score (meaning it outputs `true` if they are safe, and `false` only if the penalty condition is fully active):

```xml
<nand>
  <attribute ref="is_wearing_heavy_armor"/>
  <less-than>
    <attribute ref="strength"/>
    <attribute ref="armor_strength_requirement"/>
  </less-than>
</nand>
```



#### The 'nor' Element

The `<nor>` element performs a logical NOT-OR operation across multiple child conditions. It evaluates whether none of the nested conditions are true.

##### Evaluation Rules

1. The `<nor>` element MUST contain two or more child elements representing binary operations.
2. The evaluation engine MUST evaluate the child elements sequentially.
3. If any child element evaluates to `true`, the engine MUST immediately short-circuit and return `false`.
4. The `<nor>` element MUST evaluate to `true` if, and only if, all child elements evaluate to `false`.

##### Mathematical Definition

The operation is evaluated over $n$ boolean arguments as follows:

$$\text{nor}(x_1, x_2, \dots, x_n) = \neg \left( \bigvee_{i=1}^{n} x_i \right)$$

##### XML Example

The following example demonstrates a conditional check ensuring a character is neither under a "stunned" condition nor currently "unconscious" before allowing an action:

```xml
<nor>
  <attribute ref="is_stunned"/>
  <attribute ref="is_unconscious"/>
</nor>
```



#### The 'xnor' Element

The `<xnor>` element performs an Exclusive NOR logical operation across multiple child binary operations. It resolves to a single boolean value.

##### Evaluation Rules

1. The `<xnor>` element MUST contain two or more child elements representing binary operations.
2. The evaluation engine MUST evaluate all child binary operations to determine the total count of expressions that resolve to `true`.
3. The element MUST evaluate to `true` if an even number of child expressions resolve to `true` (including zero).
4. The element MUST evaluate to `false` if an odd number of child expressions resolve to `true`.

##### Mathematical Definition

The operation is evaluated over $n$ boolean arguments as follows:

$$\text{xnor}(b_1, b_2, \dots, b_n) = \left( \sum_{i=1}^{n} \text{int}(b_i) \right) \pmod 2 \equiv 0$$

Where $\text{int}(b_i)$ converts `true` to 1 and `false` to 0.

##### XML Example

The following example evaluates whether a character matches an even distribution of specific conditional binary flags (e.g., verifying consistency between an automated status and a manual override constraint):

```xml
<xnor>
  <attribute ref="is_poisoned"/>
  <boolean value="true"/>
</xnor>
```



#### The 'not' Element

The `<not>` element performs a logical negation (inversion) on a single child expression. It converts a truth value to false, and a false value to true.

##### Evaluation Rules

1. The `<not>` element MUST contain exactly one child element representing a binary or mathematical expression.
2. The evaluation engine MUST evaluate the child expression first.
3. If the child expression evaluates to `true` (or a non-zero numerical value), the `<not>` element MUST return `false`.
4. If the child expression evaluates to `false` (or a numerical value of `0`), the `<not>` element MUST return `true`.

##### Mathematical Definition

The operation is evaluated as follows:

$$\text{not}(x) = \neg x$$

##### XML Example

The following example demonstrates how to invert a boolean check, evaluating to `true` only if the character does *not* possess the `is_encumbered` status attribute:

```xml
<not>
  <attribute ref="is_encumbered"/>
</not>
```





#### Comparison Operators

Comparison operators evaluate numerical mathematical operations to produce a boolean result.



#### The 'greater-than' Element

The `<greater-than>` element evaluates whether the numerical outcome of a primary mathematical expression is greater than (or greater than or equal to) a secondary baseline expression. It resolves to a binary boolean result (`true` or `false`).

##### Evaluation Rules

1. The `<greater-than>` element MUST contain exactly two child elements representing mathematical expressions.
2. The children MUST be evaluated in strict positional order:
    * **Argument 1:** The primary expression to be evaluated.
    * **Argument 2:** The baseline expression compared against Argument 1.
3. The element MUST support an optional `boundary` attribute to control threshold inclusivity:
    * **`exclusive` (Default):** The comparison evaluates to `true` if and only if Argument 1 is strictly greater than Argument 2 ($>$).
    * **`inclusive`:** The comparison evaluates to `true` if Argument 1 is greater than or equal to Argument 2 ($\ge$).
4. If either child expression evaluates to a non-numeric type, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated based on the specified boundary attribute:

$$\text{greater-than}(x_1, x_2) =
\begin{cases}
x_1 > x_2 & \text{if boundary = "exclusive"} \\
x_1 \ge x_2 & \text{if boundary = "inclusive"}
\end{cases}$$

##### XML Examples

###### Example A: Exclusive Boundary (Strict Comparison)
The following example checks if a character's current hit points are strictly greater than 0:

```xml
<greater-than boundary="exclusive">
  <attribute ref="current_hp"/>
  <integer value="0"/>
</greater-than>
```



#### The 'less-than' Element

The `<less-than>` element performs a comparison operation between exactly two numerical child expressions, evaluating to a boolean value. It determines if the value of the first expression is numerically smaller than the second.

##### Evaluation Rules

1. The `<less-than>` element MUST contain exactly two child elements representing mathematical expressions.
2. The children MUST be evaluated in strict positional order:
    * **Argument 1**: The primary expression to evaluate.
    * **Argument 2**: The baseline expression compared against Argument 1.
3. The element MUST support an optional `boundary` attribute to toggle threshold inclusion logic:
    * **`exclusive` (Default)**: Evaluates to `true` if Argument 1 is strictly less than Argument 2 ($<$).
    * **`inclusive`**: Evaluates to `true` if Argument 1 is less than or equal to Argument 2 ($\le$).
4. If either child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated based on the state of the `boundary` attribute:

$$\text{less-than}(x, y) =
\begin{cases}
x < y & \text{if } \text{boundary} = \text{"exclusive"} \\
x \le y & \text{if } \text{boundary} = \text{"inclusive"}
\end{cases}$$

##### XML Example

The following example checks if a character's current weight burden exceeds or is equal to their maximum carry capacity. In this instance, it returns `true` if the current weight has successfully remained below or equal to the maximum threshold:

```xml
<less-than boundary="inclusive">
  <attribute ref="current_weight"/>
  <attribute ref="max_carry_capacity"/>
</less-than>
```



#### The 'equals' Element

The `<equals>` element performs an equality comparison across multiple child mathematical expressions. It evaluates whether all provided arguments resolve to the exact same numerical value.

##### Evaluation Rules

1. The `<equals>` element MUST contain two or more child elements representing mathematical expressions.
2. The evaluation engine MUST compute the numerical result of every child expression.
3. The element MUST evaluate to `true` if, and only if, the resolved values of all child expressions are identical. If any child expression results in a different value, the element MUST evaluate to `false`.
4. If any child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated over $n$ arguments as follows:

$$\text{equals}(x_1, x_2, \dots, x_n) = (x_1 = x_2 = \dots = x_n)$$

##### XML Example

The following example checks if a character's current hit points have dropped to exactly match their minimum allowable health bound (typically 0) to determine if they are incapacitated:

```xml
<equals>
  <attribute ref="current_hp"/>
  <integer value="0"/>
</equals>
```



#### The 'not-equals' Element

The `<not-equals>` element performs an inequality comparison across multiple child expressions. It evaluates to `true` if the evaluated child expressions do not all result in the same numerical value.

##### Evaluation Rules

1. The `<not-equals>` element MUST contain two or more child elements representing mathematical expressions.
2. The evaluation engine MUST evaluate all child expressions to their final numerical values.
3. The element MUST evaluate to `true` if at least one child expression value differs from any other child expression value (i.e., they are not all mutually identical). If all child expressions resolve to the exact same value, it MUST evaluate to `false`.
4. If any child expression evaluates to a non-numeric type, or if a structural child node is missing, the execution engine MUST treat the evaluation as an error.

##### Mathematical Definition

The operation is evaluated iteratively over $n$ arguments as follows:

$$\text{not-equals}(x_1, x_2, \dots, x_n) = \neg(x_1 = x_2 = \dots = x_n)$$

##### XML Example

The following example evaluates whether a character's current hit points have deviated from their maximum hit points (which would indicate they are currently damaged or boosted):

```xml
<not-equals>
  <attribute ref="current_hp"/>
  <attribute ref="max_hp"/>
</not-equals>
```







## Implementation Notes

TODO

## Implementation Notes

### Short-Circuit Evaluation of Ternary Expressions
When building an evaluation engine for the `<ternary>` element, developers SHOULD implement short-circuit (lazy) evaluation.

Because game manifests can feature deeply nested calculation trees or trigger dynamic attribute database queries via `<attribute ref="..." />`, executing both branches is highly inefficient. By evaluating the binary condition first, the engine can completely skip parsing or looking up attributes contained within the unused branch. This safeguards application performance and ensures that any structural or evaluation errors present in an inactive conditional branch do not prematurely crash the engine runtime.

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
