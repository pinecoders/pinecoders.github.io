<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-147975914-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-147975914-1');
</script>

[<img src="https://www.pinecoders.com/images/PineCodersLong.png">](https://www.pinecoders.com/)

# Pine Script Coding Conventions
The goal of these Coding Conventions is to present a set of best practices and style guidelines for Pine Script. By making Pine scripts easier to read, these guidelines make open source code more usable, while also providing safeguards that minimize the risk of errors for developers.

### Table of Contents

- [Script Structure](#script-structure)
- [Naming Conventions](#naming-conventions)
- [Spacing](#spacing)
- [Line Wrapping](#line-wrapping)
- [Example Scripts](#example-scripts)


<br>

## Script Structure

The Pine compiler is not very strict on exact positioning of specific statements or compiler directives. While many other arrangements are syntactically correct, these guidelines aim to provide a standard way of ordering elements in scripts:

1. The first line of a script should be the [``//@version=X``](https://www.tradingview.com/pine-script-docs/en/v4/language/Versions.html) compiler directive, where `X` is replaced by the version of Pine the script is written for. While the compiler defaults to Pine version 1 when no directive is used, scripts written using version 1 of Pine should nonetheless contain the `//@version=1` directive on their first line.

1. **Comments** describing the script are usually placed immediately after the `//@version` compiler directive.

1. The first Pine statement in the script should be either the [``study()``](https://www.tradingview.com/pine-script-reference/v4/#fun_study) or [``strategy()``](https://www.tradingview.com/pine-script-reference/v4/#fun_strategy) declaration statement.

1. The next lines should contain the following sections, properly identified if they are long:

    - Constant initializations
    - Inputs
    - Functions
    - Calculations
    - Strategy calls (for strategies)
    - Plots
    - Alerts

Notes:

- All Pine functions must be defined in the script's global scope. Nested function definitions are not allowed. If functions use global variables, they must appear after their definition, which sometimes entails they cannot be placed in the same function section of your code as the other functions.
- Variable initializations are often easier to refer to when done just before the calculations using them. Variables used throughout the script can be declared in the constants section at the top of the script. Local variables must be declared in the local block where they are used.

Here is an example of a complete script:

```js
//@version=4
// MACD indicator, a Gerald Appel concept.
// Author: TradingView, mods by PineCoders, v1.0, 2019.07.31
study("MACD")

// ————— Inputs
i_fast = input(12, "Fast Length")
// Calculates slow length from fast length and normalizes it if needed.
f_getSlowLength(_len) =>
    _tempLen = _len * 2
    if _tempLen < 20 or _tempLen > 30
        _tempLen := 25
    _tempLen
slow = f_getSlowLength(i_fast)

// ————— Calculations
fastMa = ema(close, i_fast)
slowMa = ema(close, slow)
macd = fastMa - slowMa
signal = sma(macd, 9)

// ————— Plots
plot(macd, color = color.blue)
plot(signal, color = color.orange)
```


<br>

## Naming Conventions

### Constants

Constants are variables whose value will not change during script execution. Use all caps snake case for constants, and declare them using the [``var``](https://www.tradingview.com/pine-script-reference/v4/#op_var) keyword so they are only initialized when the script executes at bar zero, when [``barstate.isfirst``](https://www.tradingview.com/pine-script-reference/v4/#var_barstate{dot}isfirst) is true. Example:

```js
// ———————————————————— Constants {

// ————— Input `options` selections.
var string RT1 = "MAs and Oscillators"
var string RT2 = "MAs"
var string RT3 = "Oscillators"

var string ON  = "On"
var string OFF = "Off"

// Levels determining "Strong Buy/Sell" and "Buy/Sell" ratings.
var float LEVEL_STRONG = 0.5
var float LEVEL_WEAK   = 0.1

// Color constants.
var color C_AQUA    = #0080FFff
var color C_BLACK   = #000000ff
// }
```

The curly braces at the beginning and end of this code section allow you to collapse/expand it using the little triangle in the Editor's left margin.

### Variable Names

We recommend using camelCase for variable names. Example: `emaLength`, `obLevel`, `showSignal2`, `aLongVariableName`.

For large projects, you may find it useful to use prefixes for a few types of variables, to make them more readily identifiable. The following prefixes can then be used:

- `i_` for variables initialized through [``input()``](https://www.tradingview.com/pine-script-reference/v4/#fun_input) calls.
- `c_` for variables containing colors.
- `p_` for variables used as [``plot()``](https://www.tradingview.com/pine-script-reference/v4/#fun_plot) or [``hline()``](https://www.tradingview.com/pine-script-reference/v4/#fun_hline) identifiers in [``fill()``](https://www.tradingview.com/pine-script-reference/v4/#fun_fill) calls.
- All caps for constants, i.e., variables often initialized at the beginning of scripts whose value will not change during execution.

We also recommend declaring the type of variables explicitly—even if the compiler does not require it. This make it easier for readers to distinguish initializations, which are done using ``=``, from reassignments, which use ``:=``. Example:

```js
//@version=4
study("", "", true)

// ————— Calculate all-time high.
// This line declares the variable on the first bar only.
// On successive bars, its value is thus preserved bar to bar, until it is assigned a new value.
var float allTimeHigh = high
allTimeHigh := max(allTimeHigh, high)

// ————— Detect changes in the all-time high.
bool newAllTimeHigh = change(allTimeHigh)

plot(allTimeHigh)
plotchar(newAllTimeHigh, "newAllTimeHigh", "•", location.top, size = size.tiny)
```

We first calculate the all-time high. We start by declaring the ``allTimeHigh`` variable as being of type "float", and assign it the value of the bar's ``high`` at bar zero. This line will no longer be executed after bar zero. When the script runs on each successive bar and on each realtime update of the feed, the variable is re-assigned with the maximum of either the variable's last value or the current bar's ``high``.

We then declare the ``newAllTimeHigh`` variable as a being of type "boolean", and on each bar, the script will assign it the value of the change in ``allTimeHigh`` between the previous and the current bar. This "float" value is then cast to a "boolean" in such a way that it is false when zero, and true otherwise.

### Function Names

For function names, we recommend using a Hungarian-style `f_` prefix in combination with the usual camelCase. The `f_` prefix guarantees disambiguation between user-defined and built-in functions. Example: `f_sinh`, `f_daysInMonth`.

### Function Parameter Names

Function parameters should be prefixed with the underscore in order to differentiate them from global scope variables. Example:
```js
daysInMonth(_year, _month) =>
```

### Function Dependencies

When a function requires global scope variables to perform its calculations, these dependencies should be documented in comments. Dependencies are to be avoided whenever possible, as they jeopardize function portability and make code more difficult to read.
```js
i_lenMultiplier = input(2, "Length Multiplier")

f_getSlowLength(_len) =>
    // Dependencies: i_lenMultiplier (initialized in inputs). 
    _tempLen = _len * i_lenMultiplier
    if _tempLen < 20 or _tempLen > 30
        _tempLen := 25
    _tempLen
```

This is a preferable way to write the same function, which eliminates dependencies:
```js
f_getSlowLength(_len, _mult) =>
    _tempLen = _len * _mult
    if _tempLen < 20 or _tempLen > 30
        _tempLen := 25
    _tempLen
```

### Local Scope Variable Names

The same underscore prefix used for function parameters should also be used for all local variables. Example:
```js
f_getSlowLength(_len) =>
    _tempLen = _len * 2
    if _tempLen < 20 or _tempLen > 30
        _tempLen := 25
    _tempLen
```
```js
if something
    _myLocalVar = something
```
```js
for _i = 0 to 100
    _myLocalVar = something[_i]
```


<br>

## Spacing

A space should be used on both sides of all operators, whether they be assignment, arithmetic (binary or unary) or logical. A space should also be used after commas. Example:
```js
a = close > open ? 1 : -1
var newLen = 2
newLen := min(20, newlen + 1)
a = - b
c = d > e ? d - e : d
index = bar_index % 2 == 0 ? 1 : 2
plot(series, color = color.red)
```


<br>

## Line Wrapping

When lines need to be continued on the next, use two spaces to indent each continuation line. Example:
```js
plot(
  series = close,
  title = "Close",
  color = color.blue,
  show_last = 10
  )
```

Tabs may be used to line up elements in order to increase readability.
```js
plot(
  series    = close,
  title     = "Close",
  color     = color.blue,
  show_last = 10
  )
```

<br>

## Example Scripts

These are examples of scripts by authors who use our Coding Conventions systematically:
- [Relative Volume at Time](https://www.tradingview.com/script/n0f50JKv-Relative-Volume-at-Time/)
- [Tape [LucF]](https://www.tradingview.com/script/8mVFTxPg-Tape-LucF/)
- [[e2] Absolute Retracement](https://www.tradingview.com/script/X87V5IBs-e2-Absolute-Retracement/)
- [MTF Oscillator Framework [PineCoders]](https://www.tradingview.com/script/Wvcqygsx-MTF-Oscillator-Framework-PineCoders/)


<br>

**[Back to top](#table-of-contents)**
