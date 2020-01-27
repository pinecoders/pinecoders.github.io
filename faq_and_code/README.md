<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-147975914-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-147975914-1');
</script>

[<img src="http://pinecoders.com/images/PineCodersLong.png">](http://pinecoders.com)

# FAQ & Code

This is a compendium of frequently asked questions on Pine. Answers often give code examples or link to the best sources on the subject.

Do not make the mistake of assuming this is strictly beginner's material; some of the questions and answers explore advanced techniques.

> **Reusing this code**: You are welcome to reuse this code in your open source scripts only. No permission is required from PineCoders. Credits are appreciated.

### Table of Contents

- [Built-in variables](#built-in-variables)
- [Built-in functions](#built-in-functions)
- [Operators](#operators)
- [Math](#math)
- [Plotting](#plotting)
- [Indicators (a.k.a. studies)](#indicators)
- [Strategies](#strategies)
- [Time and dates](#time-and-dates)
- [Other intervals (MTF)](#other-intervals-mtf)
- [Alerts](#alerts)
- [Editor](#editor)
- [Techniques](#techniques)
- [Debugging](#debugging)

<br><br>
## BUILT-IN VARIABLES


### What is the variable name for the current price? 
The `close` variable holds both the price at the close of historical bars and the current price when an **indicator** is running on the realtime bar. If the script is a **strategy** running on the realtime bar, by default it runs only at the bar's close. If the `calc_on_every_tick` parameter of the `strategy()` declaration statement is set to `true`, the strategy will behave as an indicator and run on every price change of the realtime bar.

To access the close of the previous bar's close in Pine, use `close[1]`. In Pine, brackets are used as the [history-referencing operator](https://www.tradingview.com/pine-script-docs/en/v4/language/Operators.html#history-reference-operator).

### What is the code for a green candle?
```js
greenCandle = close > open
```
Once you have defined the `greenCandle` variable, if you wanted a boolean variable to be `true` when the last three candles were green ones, you could write:
```js
threeGreenCandles = greenCandle and greenCandle[1] and greenCandle[2]
```
> Note that the variable name `3GreenCandles` would have caused a compilation error. It is not legal in Pine as it begins with a digit.

If you need to define up and down candles, then make sure one of those definitions allows for the case where the `open` and `close` are equal:
```js
upCandle = close >= open
downCandle = close < open
```

**[Back to top](#table-of-contents)**



<br><br>
## BUILT-IN FUNCTIONS


### Why do I get an error message when using `highest()` or `lowest()`?
Most probably because you are trying to use a series integer instead of a simple integer as the second parameter (the length). Either use a [simple integer](https://www.tradingview.com/pine-script-docs/en/v4/language/Type_system.html#simple) or use the [RicardoSantos](https://www.tradingview.com/u/RicardoSantos/#published-scripts) replacements [here](https://www.tradingview.com/script/32ohT5SQ-Function-Highest-Lowest/). If you don't know Ricardo, take the time to look at his indicators while you're there. Ricardo is among the most prolific and ingenious Pine coders out there.

### How can I work with arrays in Pine?
There is currently no array data type in Pine. RicardoSantos has some pseudo-array code [here](https://www.tradingview.com/script/sQxpiBL8-RS-Function-Pseudo-Array-Example/).

### How can I use a variable length argument in certain functions ?
The `sma`, `variance`, `stdev`, `correlation` functions don't allow a **series** as their length argument which must be a **simple int**. The following equivalent functions allow you to use a series as the length argument :

```
Sum(src,p) => a = cum(src), a - a[p]

Sma(src,p) => a = cum(src), (a - a[p])/p

Variance(src,p) => p == 1 ? 0 : Sma(src*src,p) - pow(Sma(src,p),2)

Stdev(src,p) => p == 1 ? 0 : sqrt(Sma(src*src,p) - pow(Sma(src,p),2))

Covariance(x,y,p) => Sma(x*y,p) - Sma(x,p)*Sma(y,p)

Correlation(x,y,p) => Covariance(x,y,p)/(Stdev(x,p)*Stdev(y,p))
```

If `p` is a decimal number then `p` is automatically rounded to the nearest integer. Most of the functions in the script are dependent on the `Sma` function except `Sum`, therefore if you want to use a function don't forget to include the `Sma` function in your script. The rolling correlation `Cor` make use of the `Cov` and `Stdev` function, so you must include them if you plan to use `Cor`.

Make sure the series you use as length argument is greater than 0, else the functions will return `na`. When using a series as length argument, the following error might appear : *Pine cannot determine the referencing length of a series. Try using max_bars_back in the study or strategy function*, this can be frequent if you plan to use `barssince(condition)` where `condition` is a relatively rare event. You can fix it by making use of `max_bars_back` as follows :

`study("Title",overlay=true,max_bars_back=5000)`

*Note that the rolling variance/standard deviation/covariance are computed using the naïve algorithm.*

**[Back to top](#table-of-contents)**



<br><br>
## OPERATORS


### What's the difference between `==`, `=` and `:=`?
`==` is a [comparison operator](https://www.tradingview.com/pine-script-docs/en/v4/language/Operators.html#comparison-operators) used to test for true/false conditions.<br>
`=` is used to [declare and initialize variables](https://www.tradingview.com/pine-script-docs/en/v4/language/Expressions_declarations_and_statements.html#variable-declaration).<br>
`:=` is used to [assign values to variables](https://www.tradingview.com/pine-script-docs/en/v4/language/Expressions_declarations_and_statements.html#variable-assignment) after initialization, transforming them into *mutable variables*.
```js
//@version=3
study("")
a = 0
b = 1
plot(a == 0 ? 1 : 2)
plot(b == 0 ? 3 : 4, color = orange)
a := 2
plot(a == 0 ? 1 : 2, color = aqua)
```

### Can I use the `:=` operator to assign values to past values of a series?
No. Past values in Pine series are read-only, as is the past in real life. Only the current bar instance (`variableName[0]`) of a series variable can be assigned a value, and when you do, the `[]` history-referencing operator must **not** be used—only the variable name.

What you can do is create a series with the values you require in it as the script is executed, bar by bar. The following code creates a new series called `range` with a value containing the difference between the bar's `close` and `open`, but only when it is positive. Otherwise, the series value is zero.
```js
range = close > open ? close - open : 0.0
```
In the previous example, we could determine the value to assign to the `range` series variable as we were going over each bar in the dataset because the condition used to assign values was known on that bar. Sometimes, you will only obtain enough information to identify the condition after a number of bars have elapsed. In such cases, a `for` loop must be used to go back in time and analyse past bars. This will be the case in situations where you want to identify fractals or pivots. See the [Pivots Points High/Low](https://www.tradingview.com/pine-script-docs/en/v4/essential/Drawings.html#pivot-points-high-low) from the User Manual, for example.

### Why do some logical expressions not evaluate as expected when na values are involved?
Pine logical expressions have 3 possible values: `true`, `false` and `na`. Whenever an `na` value is used in a logical expression, the result of the logical expression will be na. Thus, contrary to what could be expected, `na == na`, `na == true`, `na == false` or `na != true` all evaluate to `na`. Furthermore, when a logical expression evaluates to `na`, the false branch of a conditional statement will be executed. This may lead to unexpected behavior and entails that special cases must be accounted for if you want your code to handle all possible logical expression results according to your expectations.

Let's take a case where, while we are debugging code, we want to compare two variables that should always have the same value, but where one of the variables or both can have an na value. When that is the case, neither `a == b` nor `a != b` will return true or false, as they both return na.

When we undestand this, we can see why the first `bgcolor()` line in the following code shows no background. While you could expect the `a != b` logical expression to be true and thus the background to appear lime because the value of variable `a` does not equal the value of `b`, this is not the case. Because the logical expression returns `na`, the false branch of the ternary is executed and no color is plotted in the background.

The second `bgcolor()` line will produce the behavior we expect. You will see this if you comment out the first one and uncomment this second line. The other lines show different variations of the concept.
```js
//@version=4
study("")
int a = 1
int b = na
bgcolor(a != b ? color.lime : na, transp = 20) // na, so goes to false branch.
// bgcolor(a == b ? na : color.red, transp = 20) // na, so goes to false branch.
// bgcolor(na((a != b)) ? color.orange : na, transp = 20) // true, so works.
// bgcolor(a != b or na(a != b) ? color.fuchsia : na, transp = 20) // true, so works.
```
This code shows a more practical example using a test for pivots.

```js
//@version=4
study("Logical expressions evaluate to true, false or na", "", precision=10)
// Truncated Stoch RSI built-in
smoothK = input(3, minval=1)
lengthRSI = input(14, minval=1)
lengthStoch = input(14, minval=1)
src = input(close, title="RSI Source")
capMin = input(false)
showEquals = input(true)
rsi1 = rsi(src, lengthRSI)
kCapped = max(10e-10, sma(stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK))
kNormal = sma(stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK)
k = capMin ? kCapped : kNormal
plot(k, color=color.blue)
hline(0, "", color.gray)
pLo = pivotlow(k, 1, 1)

// Usual way which doesn't work when a pivot occurs at value 0.
var usualSignal = 0.
if pLo
    usualSignal := 85
else
    // Note that this else clause catches all non-true values, so both 0 (false) AND na values.
    usualSignal := 15
plot(usualSignal, "Usual Signal", color.teal, 10, transp = 10)

// Bad way because we're comparing the pivot's value to 1 (true) and 0 (false), 
// so the logical expressions will only be true if a pivot occurs at those values, which is almost never.
var badSignal = 0.
if pLo == true
    // This conditions only catches pivots when they occur at value == 1, so almost never happens.
    badSignal := 85
else
    // This conditions only catches pivots when they occur at value == 0, so almost never happens.
    if pLo == false
        badSignal := 15
    else
        // This catches all the rest of conditions, which is almost always.
        badSignal := 50
plot(badSignal, "Bad Signal", color.purple, 10, transp = 60)

// Proper way to test so that we do not miss any pivots.
var goodSignal = 0.
if not na(pLo)
    // This identifies all pivot occurrences (including at value == 0) because it tests for values that are not na.
    goodSignal := 85
else
    goodSignal := 15
plot(goodSignal, "Good Signal", color.orange, 2, transp = 0)
    
// Our background color also misses pivots when they occur at value == 0.
bgcolor(pLo ? color.red : na, transp = 70)

// This line identifies pivots which occur at value == 0.
plotchar(not na(pLo) and pLo == 0., "", "•", location.top, color.fuchsia, 0, text = "Missed\nlow pivot", textcolor = color.new(color.red, 0), size = size.small)

// Debugging plots for Data Window.
plotchar(pLo, "pLo", "", location.top)
plotchar(pLo == true, "pLo == true", "", location.top)
plotchar(pLo == false, "pLo == false", "", location.top)
plotchar(na(pLo), "na(pLo)", "", location.top)
plotchar(true, "true", "", location.top)
plotchar(false, "false", "", location.top)
```
![.](https://www.tradingview.com/x/zk9ZOrd2/ "Logical expressions")


**[Back to top](#table-of-contents)**

## MATH

### How can I round a fraction in 0.5 increments?
```js
//@version=4
study("Round fraction")
f_roundFraction(_n) =>
    _whole = floor(abs(_n))
    _fraction = abs(_n) - _whole
    sign(_n) * (_whole + (_fraction >=  0.75 ? 1. : _fraction >=  0.25 ? 0.5 : 0.))
    
val = input(0.75, step = 0.01)
plot(f_roundFraction(val))
```

### How do I calculate averages?
1. If you just want the average between two values, you can use `avg(val1, val2)` or `(val1 + val2)/2`. Note that [`avg()`](https://www.tradingview.com/pine-script-reference/v4/#fun_avg) accepts up to 6 values.
1. To average the last x values in a series, you can use `sma(series, x)`.

### How can I calculate an average only when a certain condition is true?
[This script](https://www.tradingview.com/script/isSfahiX-Averages-PineCoders-FAQ/) shows how to calculate a conditional average using three different methods.

### How can I generate a random number?
Because Pine scripts do not have direct access to the hardware timer it is impossible to create a real random number generator. This function gives authors the closest thing. It will generate a different seed every time the script is first run in *uncached* mode on a symbol/timeframe, which occurs when it runs the first time after a browser refresh or because the script is saved from the Editor.

The function uses the fact that the [`timenow`](https://www.tradingview.com/pine-script-reference/v4/#var_timenow) built-in, which returns the current time, will be different on the first bar of a script for each *first execution* of the script. Because of the caching mechanism in the Pine runtime, this value will not change if you run the script once on a symbol/TF, change TF and return to the original TF.

The function allows a range to be specified. Credits to RicardoSantos for the [original code](https://www.tradingview.com/script/EgKBHFnb-RS-Function-Functions-to-generate-Random-values/).

```js
//@version=4
study("Seeded Randomizer")
f_random_number(_range) =>
    var _return = 1.0 + timenow
    _return := (3.14159 * _return % (bar_index + 1)) % _range

r = f_random_number(100)
plot(r, style = plot.style_circles)
```

**[Back to top](#table-of-contents)**


<br><br>
## PLOTTING


### Can I plot diagonals between two points on the chart?
Yes, using the [`line.new()`](https://www.tradingview.com/pine-script-reference/v4/#fun_line{dot}new) function available in v4. See the [Trendlines - JD](https://www.tradingview.com/script/mpeEgn5J-Trendlines-JD/) indicator by Duyck.

### How do I plot a line using start/stop criteria?
You'll need to define your start and stop conditions and use logic to remember states and the level you want to plot.

Note the `plot()` call using a combination of plotting `na` and the `style = plot.style_linebr` parameter to avoid plotting a continuous line, which would produce inelegant joins between different levels.

Also note how `plotchar()` is used to plot debugging information revealing the states of the boolean building blocks we use in our logic. These plots are not necessary in the final product; they are used to ensure your code is doing what you expect and can save you a lot of time when you are writing your code.
```js
//@version=4
study("Plot line from start to end condition", overlay=true)
lineExpiryBars = input(300, "Maximum bars line will plot", minval = 0)
// Stores "close" level when start condition occurs.
var savedLevel = float(na)
// True when the line needs to be plotted.
var plotLine = false
// This is where you enter your start and end conditions.
startCondition = pivothigh(close, 5, 2)
endCondition = cross(close, savedLevel)
// Determine if a line start/stop condition has occurred.
startEvent = not plotLine and startCondition
// If you do not need a limit on the length of the line, use this line instead: endEvent = plotLine and endCondition
endEvent = plotLine and (endCondition or barssince(startEvent) > lineExpiryBars)
// Start plotting or keep plotting until stop condition.
plotLine := startEvent or (plotLine and not endEvent)
if plotLine and not plotLine[1]
    // We are starting to plot; save close level.
    savedLevel := close
// Plot line conditionally.
plot(plotLine ? savedLevel : na, color = color.orange, style = plot.style_linebr)
// State plots revealing states of conditions.
plotchar(startCondition, "startCondition", "•", color = color.green, size=size.tiny, transp = 0)
plotchar(endCondition, "endCondition", "•", color = color.red, size=size.tiny, location = location.belowbar, transp = 0)
plotchar(startEvent, "startEvent", "►", color = color.green, size=size.tiny)
plotchar(endEvent, "endEvent", "◄", color = color.red, size=size.tiny, location = location.belowbar)
```

### How do I plot a support or a trend line?
To plot a continuous line in Pine, you need to either:
1. Look back into elapsed bars to find an occurrence that will return the same value over consecutive bars so you can plot it, or
1. Find levels and save them so that you can plot them. In this case your saving mechanism will determine how many levels you can save.
1. You may also use the [`line.new()`](https://www.tradingview.com/pine-script-reference/v4/#fun_line{dot}new) function available in v4.
These are examples of three different techniques used to determine and draw support lines:
- [Backtest Rookies](https://backtest-rookies.com/2018/10/05/tradingview-support-and-resistance-indicator/)
- [Auto-Support v 0.2 by jamc](https://www.tradingview.com/script/hBrQx1tG-Auto-Support-v-0-2/)
- [S/R Barry by likebike](https://www.tradingview.com/script/EHqtQi2g-S-R-Barry/)
- [Trendlines - JD by Duyck](https://www.tradingview.com/script/mpeEgn5J-Trendlines-JD/) is a v4 example.

### How many plots, security() calls, variables or lines of code can I use?
- The limit for plots is 64. Note than one plot statement can use up more than one allowed plot, depending on how it is structured. If you use series (conditional) color on the plot or text, each one will add a plot count. Starting with Pine v4, `alertcondition()` calls also count for one plot.
- When using labels or lines created with `label.new()` and `line.new()` a garbage collector will preserve only the last ~50 objects of each type.
- The limit for `security()` calls is 40.
- The limit for variables is 1000.
- We do not know of a limit to the number of lines in a script. There is, however a limit of 50K compiled tokens, but they don't correspond to code lines.

### How can I use colors in my indicator plots?
See [Working with colours](https://kodify.net/tradingview/colours/) by Kodify.

### How do I make my indicator plot over the chart?
Use `overlay=true` in `strategy()` or `study()` declaration statement, e.g.,:
```js
study("My Script", overlay = true)
```
If your indicator was already in a Pane before applying this change, you will need to use Add to Chart again for the change to become active.

### Can I use `plot()` calls in a `for` loop?
No, but you can use the v4 [`line.new()`](https://www.tradingview.com/pine-script-reference/v4/#fun_line{dot}new) function in `for` loops.

### How can I plot vertical lines on a chart?
You can use the `plot.style_columns` style to plot them:
```js
//@version=4
study("", "", true, scale = scale.none)
cond = close > open
plot(cond ? 10e20 : na, style = plot.style_columns, color = color.silver, transp=85)
```
There is a nice v4 function to plot a vertical line in this indicator: [vline() Function for Pine Script v4.0+](https://www.tradingview.com/script/EmTkvfCM-vline-Function-for-Pine-Script-v4-0/).

### How can I access normal bar OHLC values on a non-standard chart?
You need to use the `security()` function. This script allows you to view normal candles on the chart, although depending on the non-standard chart type you use, this may or may not make much sense:
```js
//@version=4
study("Plot underlying OHLC", "", true)

// ————— Allow plotting of underlying candles on chart.
plotCandles = input(true, "Plot Candles")
method      = input(1, "Using Method", minval = 1, maxval = 2)

// ————— Method 1: Only works when chart is on default exchange for the symbol.
o1 = security(syminfo.ticker, timeframe.period, open)
h1 = security(syminfo.ticker, timeframe.period, high)
l1 = security(syminfo.ticker, timeframe.period, low)
c1 = security(syminfo.ticker, timeframe.period, close)
// ————— Method 2: Works all the time because it use the chart's symbol and exchange information.
ticker = tickerid(syminfo.prefix, syminfo.ticker)
o2 = security(ticker, timeframe.period, open)
h2 = security(ticker, timeframe.period, high)
l2 = security(ticker, timeframe.period, low)
c2 = security(ticker, timeframe.period, close)
// ————— Get value corresponding to selected method.
o = method == 1 ? o1 : o2
h = method == 1 ? h1 : h2
l = method == 1 ? l1 : l2
c = method == 1 ? c1 : c2

// ————— Plot underlying close.
plot(c, "Underlying close", color = color.gray, linewidth = 3, trackprice = true)
// ————— Plot candles if required.
invisibleColor = color.new(color.white, 100)
plotcandle(plotCandles ? o : na, plotCandles ? h : na, plotCandles ? l : na, plotCandles ? c : na, color = color.orange, wickcolor = color.orange)
// ————— Plot label.
f_print(_txt) => t = time + (time - time[1]) * 3, var _lbl = label.new(t, high, _txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large), label.set_xy(_lbl, t, high + 3 * tr)
f_print("Underlying Close1 = " + tostring(c1) + "\nUnderlying Close2 = " + tostring(c2) + "\nChart's close = " + tostring(close) + "\n Delta = " + tostring(close - c))
```

### How can I keep only the last x labels or lines?
The first thing required is to maintain a series containing the ids of the labels or lines as they are created. This is accomplished by assigning the returning value of the `label.new()` or `line.new()` function to a variable. This creates a series with value `na` if no label or line was created from that bar, and with a value of type *label* or *line* when an element is created.

The next step will be to run a loop going back into the past from the current bar, jumping over a preset number of labels or lines and deleting all those following that, all the while doing nothing when an `na` value is found since this means no label or line was created on that bar.

This first example illustrates the technique using labels:
```js
//@version=4
//@author=LucF, for PineCoders
maxBarsBack = 2000
study("Keep last x labels", "", true, max_bars_back = maxBarsBack)
keepLastLabels = input(5, "Last labels to keep")

// ————— Label-creating condition: when close is above ma.
ma = sma(close,30)
var aboveMa = false
aboveMa := crossover(close, ma) or (aboveMa and not crossunder(close, ma))

// ————— Count number of bars since last crossover to show it on label.
var barCount = 0
barCount := aboveMa ? not aboveMa[1] ? 1 : barCount + 1 : 0

// ————— Create labels while keeping a trail of label ids in series "lbl".
// This is how we will later identify the bars where a label exist.
label lbl = na
if aboveMa
    lbl := label.new(bar_index, high, tostring(barCount), xloc.bar_index, yloc.price, size = size.small)

// ————— Delete all required labels.
// Loop from previous bar into the past, looking for bars where a label was created.
// Delete all labels found in last "maxBarsBack" bars after the required count has been left intact.
lblCount = 0
for i = 1 to maxBarsBack
    if not na(lbl[i])
        // We have identified a bar where a label was created.
        lblCount := lblCount + 1
        if lblCount > keepLastLabels
            // We have saved the required count of labels; delete this one.
            label.delete(lbl[i])

plot(ma)
```

The second example illustrates the technique using lines:
```js
//@version=4
//@author=LucF, for PineCoders
maxBarsBack = 2000
study("Keep last x lines", "", true, max_bars_back = maxBarsBack)

// On crossovers/crossunders of these MAs we will be recording the hi/lo reched until opposite cross.
// We will then use these hi/los to draw lines in the past.
ma1 = sma(close, 20)
ma2 = sma(close, 100)

// ————— Build lines.
// Highest/lowest hi/lo during up/dn trend.
var hi = 10e-10
var lo = 10e10
// Bar index of highest/lowest hi/lo.
var hiBar = 0
var loBar = 0
// Crosses.
crossUp = crossover(ma1, ma2)
crossDn = crossunder(ma1, ma2)
upTrend = ma1 > ma2

// Draw line in past when a cross occurs.
line lin = na
if crossUp or crossDn
    lin := line.new(bar_index[bar_index - hiBar], high[bar_index - hiBar], bar_index[bar_index - loBar], low[bar_index - loBar], xloc.bar_index, extend.none, color.black)

// Reset hi/lo and bar index on crosses.
if crossUp
    hi := high
    hiBar := bar_index
else
    if crossDn
        lo := low
        loBar := bar_index

// Update higher/lower hi/lo during trend.
if upTrend and high > hi
    hi := high
    hiBar := bar_index
else
    if not upTrend and low < lo
        lo := low
        loBar := bar_index

plot(ma1, "MA1", color.aqua, 1)
plot(ma2, "MA2", color.orange, 1)

// ————— Delete all required lines.
// Loop from previous bar into the past, looking for bars where a line was created.
// Delete all lines found in last "maxBarsBack" bars after the required count has been left intact.
keepLastLines = input(5)
lineCount = 0
for i = 1 to maxBarsBack
    if not na(lin[i])
        lineCount := lineCount + 1
        if lineCount > keepLastLines
            line.delete(lin[i])
```

### Is it possible to draw geometric shapes?
It's possible, but not trivial. See [this RicardoSantos script](https://www.tradingview.com/script/KhKqjR0J-RS-Function-Geometric-Line-Drawings/).


### How can I print a value at the top right of the chart?
We will use a label to print our value. Labels however, require positioning relative to the symbol's price scale, which is by definition fluid. The technique we use here is to create an indicator running in "No Scale" space, and then create an artificially large internal scale for it by using the `plotchar()` call which doesn't print anything. We then print the label at the top of that large scale, which does not affect the main chart display because the indicator is running in a separate scale.

Also note that we take care to only print the label on the last bar of the chart, which results in much more efficient code than if we deleted and re-created a label on every bar of the chart, as would be the case if the `if barstate.islast` condition didn't restrict calls to our `f_print()` label-creating function.
```js
//@version=4
//@author=LucF, for PineCoders
// Indicator needs to be on "no scale".
study("", "Daily ATR", true, scale = scale.none)
atrLength = input(14)
barsRight = input(5)
// Adjust the conversion formatting string to the instrument: e.g., "#.########" for crypto.
numberFormat = input("#.####")
// Plot invisible value to give a large upper scale to indie space.
plotchar(10e10, "", "")
// Fetch daily ATR. We want the current daily value so we use a repainting security() call.
dAtr = security(syminfo.tickerid, "D", atr(atrLength), lookahead = barmerge.lookahead_on)
// Label-creating function puts label at the top of the large scale.
f_print(_txt) => t = time + (time - time[1]) * 3, var _lbl = label.new(t, high, _txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large), label.set_xy(_lbl, t, high + 3 * tr)
// Print value on last bar only, so code runs faster.
if barstate.islast
    f_print(tostring(dAtr, numberFormat))
```

### How can I toggle `hline()` plots on and off?
```js
showHline = input(true)
hline(50, color = showHline ? color.blue : #00000000)
```

### How can I lift `plotshape()` text up?
You will need to use `\n` followed by a special non-printing character that doesn't get stripped out. Here we're using U+200E. While you don't see it in the following code's strings, it is there and can be copy/pasted. The special Unicode character needs to be the last one in the string for text going up, and the first one when you are plotting under the bar and text is going down:
```
//@version=4
study("Lift text", "", true)
// Use U+200E (Decimal 8206) as a non-printing space after the last "\n".
// The line will become difficult to edit in the editor, but the character will be there.
// You can use https://unicode-table.com/en/tools/generator/ to generate a copy/pastable character.
plotshape(true, "", shape.arrowup,      location.abovebar, color.green,     text="A")
plotshape(true, "", shape.arrowup,      location.abovebar, color.lime,      text="B\n‎")
plotshape(true, "", shape.arrowdown,    location.belowbar, color.red,       text="C")
plotshape(true, "", shape.arrowdown,    location.belowbar, color.maroon,    text="‎\nD")
```
![.](https://www.tradingview.com/x/MMMFiRZI/ "Lift text up with plotshape()")

**[Back to top](#table-of-contents)**



<br><br>
## INDICATORS


### Can I create an indicator that plots like the built-in Volume or Volume Profile indicators?
No. A few of the built-in indicators TradingView publishes are written in JavaScript because their behavior cannot be replicated in Pine. The Volume and Volume Profile indicators are among those.

### How can I use one script's output as an input into another?
Use the following in your code:
```js
ExternalIndicator = input(close, "External Indicator")
```
From the script's *Inputs* you will then be able to select a plot from another indicator if it present on your chart.
You can use only one such statement in your script. If you use more than one, the other indicator plots will not be visible from the *Inputs* dropdown. **You cannot use this technique in strategies.**

See how our [Signal for Backtesting-Trading Engine](https://www.tradingview.com/script/y4CvTwRo-Signal-for-Backtesting-Trading-Engine-PineCoders/) can be integrated as an input to our [Backtesting-Trading Engine](https://www.tradingview.com/script/dYqL95JB-Backtesting-Trading-Engine-PineCoders/).

### Can I write a script that plots like the built-in Volume Profile or Volume indicators?
No. TradingView uses special code for these that is not available to standard Pine scripts.

### Is it possible to export indicator data to a file?
No. The only way for now is through screen scraping.

### Can my script place something on the chart when it is running from a pane?
The only thing that can be changed on the chart from within a pane is the color of the bars. See the [`barcolor()`](https://www.tradingview.com/pine-script-docs/en/v4/annotations/Barcoloring_a_series_with_barcolor.html) function.

### Can I merge 2 or more indicators into one?
Sure, but start by looking at the scale each one is using. If you're thinking of merging a moving average indicator designed to plot on top of candles and in relation to them, you are going to have problems if you also want to include and indicator showing volume bars in the same script because their values are not on the same scale.

Once you've made sure your scales will be compatible (or you have devised a way of [normalizing/re-scaling them](#how-can-i-rescale-an-indicator-from-one-scale-to-another)), it's a matter of gathering the code from all indicators into one script and removing any variable name collisions so each indicator's calculations retain their independence and integrity.

> Note that if the indicators you've merged are CPU intensive, you may run into runtime limitations when executing the compound script.

**[Back to top](#table-of-contents)**



<br><br>
## STRATEGIES


### Why are my orders executed on the bar following my triggers?
TradingView backtesting evaluates conditions at the close of historical bars. When a condition triggers, the associated order is executed at the open of the **next bar**, unless `process_orders_on_close=true` in the [`strategy()`](https://www.tradingview.com/pine-script-reference/v4/#fun_strategy) declaration statement, in which case the broker emulator will try to execute orders at the bar's close.

In the real-time bar, orders may be executed on the *tick* (price change) following detection of a condition. While this may seem appealing, it is important to realize that if you use `calc_on_every_tick=true` in the `strategy()` declaration statement to make your strategy work this way, you are going to be running a different strategy than the one you tested on historical bars. See the [Strategies](https://www.tradingview.com/pine-script-docs/en/v4/essential/Strategies.html) page of the User Manual for more information.

### How do I implement date range filtering in strategies?
This piece of code does from/to dates. If you need to also filter on specific times, use [How To Set Backtest Time Ranges](https://www.tradingview.com/script/xAEG4ZJG-How-To-Set-Backtest-Time-Ranges/) by [allanster](https://www.tradingview.com/u/allanster/#published-scripts).
```js
DateFilter = input(false, "═════════════ Date Range Filtering")
FromYear = input(1900, "From Year", minval = 1900)
FromMonth = input(1, "From Month", minval = 1, maxval = 12)
FromDay = input(1, "From Day", minval = 1, maxval = 31)
ToYear = input(2999, "To Year", minval = 1900)
ToMonth = input(1, "To Month", minval = 1, maxval = 12)
ToDay = input(1, "To Day", minval = 1, maxval = 31)
FromDate = timestamp(FromYear, FromMonth, FromDay, 00, 00)
ToDate = timestamp(ToYear, ToMonth, ToDay, 23, 59)
TradeDateIsAllowed() => DateFilter ? (time >= FromDate and time <= ToDate) : true
```
You can then use the result of `TradeDateIsAllowed()` to confirm your entries using something like this:
```js
EnterLong = GoLong and TradeDateIsAllowed()
```
> Note that with this code snippet, date filtering can be enabled/disabled using a checkbox. This way you don't have to reset dates when filtering is no longer needed; just uncheck the box.

### Why is backtesting on Heikin Ashi and other non-standard charts not recommended?
Because non-standard chart types use non-standard prices which produce non-standard results. See our [Backtesting on Non-Standard Charts: Caution! - PineCoders FAQ](https://www.tradingview.com/script/q9laJNG9-Backtesting-on-Non-Standard-Charts-Caution-PineCoders-FAQ/) indicator and its description for a more complete explanation.

The TradingView Help Center also has a [good article](https://www.tradingview.com/house-rules/?solution=43000481029) on the subject.

### How can I save the entry price in a strategy?
Here are two ways you can go about it:
```js
//@version=4
// Mod of original code at https://www.tradingview.com/script/bHTnipgY-HOWTO-Plot-Entry-Price/
strategy("Plot Entry Price", "", true)

longCondition = crossover(sma(close, 14), sma(close, 28))
if (longCondition)
    strategy.entry("My Long Entry Id", strategy.long)
shortCondition = crossunder(sma(close, 14), sma(close, 28))
if (shortCondition)
    strategy.entry("My Short Entry Id", strategy.short)

// ————— Method 1: wait until bar following order and use its open.
var float entryPrice = na
if longCondition[1] or shortCondition[1]
    entryPrice := open
plot(entryPrice, "Method 1", color.orange, 3, plot.style_circles)

// ————— Method 2: use built-in variable.
plot(strategy.position_avg_price, "Method 2", color.gray, 1, plot.style_circles, transp = 0)
```

### How do I convert a strategy to a study in order to generate alerts for discretionary trading or a third-party execution app/bot?
The best way to go about this is to write your strategies in such a way that their behavior depends the least possible on `strategy.*` variables and `strategy.*()` call parameters, because these cannot be converted into an indicator.

The PineCoders [Backtesting-Trading Engine](https://www.tradingview.com/script/dYqL95JB-Backtesting-Trading-Engine-PineCoders/) is a framework that allows you to easily convert betweeen strategy and indicator modes because it manages trades using custom Pine code that does not depend on an involved setup of `strategy.*()` call parameters.

### Can my strategy generate orders through TV-supported brokers?
No. The brokers can only be used for manual trading. Currently, the only way to automate trading using TradingView is to:
- Create an indicator (a.k.a. *study*) from your strategy.
- Insert `alertcondition()` calls in your indicator using your buy/sell conditions.
- Create separate Buy and Sell alerts from TV Web.
- Link those alerts to a third-party app/bot which will relay orders to exchanges or brokers. See the [Automation](http://pinecoders.com/resources#automation) section of our Resources document.

**[Back to top](#table-of-contents)**



<br><br>
## TIME AND DATES


### How can I get the time of the first bar in the dataset?
``time[bar_index]`` will return that [time](https://www.tradingview.com/pine-script-reference/v4/#var_time) in Unix format, i.e., the number of milliseconds that have elapsed since 00:00:00 UTC, 1 January 1970.

### How can I know how many days are in the current month?
Use [this function](https://www.tradingview.com/script/mHHDfDB8-RS-Function-Days-in-a-Month/) by RicardoSantos.

### How can I detect the chart's last day?
To do this, we will use the [`security()`](https://www.tradingview.com/pine-script-reference/v4/#fun_security) function called at the 1D resolution and have it evaluate the [`barstate.islast`](https://www.tradingview.com/pine-script-reference/v4/#var_barstate{dot}islast) variable on that time frame, which returns true when the bar is the last one in the dataset, even if it is not a realtime bar because the market is closed. We also allow the `security()` function to lookahead, otherwise it will only return true on the last bar of the chart's resolution.
```js
//@version=4
study("")
lastDay = security(syminfo.tickerid, "D", barstate.islast, lookahead = barmerge.lookahead_on)
bgcolor(lastDay ? color.red : na)
```

### How can I detect if a bar's date is today?
```js
//@version=4
//@author=mortdiggiddy, for PineCoders
study("Detect today", "", true)
currentYear = year(timenow)
currentMonth = month(timenow)
currentDay = dayofmonth(timenow)
today = year == currentYear and month == currentMonth and dayofmonth == currentDay
bgcolor(today ? color.gray : na)
```

**[Back to top](#table-of-contents)**



<br><br>
## OTHER INTERVALS (MTF)
See the PineCoders [MTF Selection Framework](https://www.tradingview.com/script/90mqACUV-MTF-Selection-Framework-PineCoders-FAQ/) for a complete implementation of a higher timeframe RSI in a script.

### How do I define a higher interval that is a multiple of the current one?
Use the PineCoders ``f_MultipleOfRes()`` function.
```js
//@version=4
//@author=LucF, for PineCoders
study("Multiple of current TF v4", precision = 8)

// Get multiple.
resMult = input(2, minval = 1)

// Returns a multiple of current TF as a string usable with "security()".
f_multipleOfRes(_mult) => 
    // Convert target timeframe in minutes.
    _targetResInMin = timeframe.multiplier * _mult * (
      timeframe.isseconds   ? 1. / 60. :
      timeframe.isminutes   ? 1. :
      timeframe.isdaily     ? 1440. :
      timeframe.isweekly    ? 10080. :
      timeframe.ismonthly   ? 43800. : na)
      // Find best way to express the TF.
    _targetResInMin     <= 0.0417       ? "1S"  :
      _targetResInMin   <= 0.167        ? "5S"  :
      _targetResInMin   <= 0.376        ? "15S" :
      _targetResInMin   <= 0.751        ? "30S" :
      _targetResInMin   <= 1440         ? tostring(round(_targetResInMin)) :
      _targetResInMin   <= 43800        ? tostring(round(min(_targetResInMin / 1440, 365))) + "D" :
      tostring(round(min(_targetResInMin / 43800, 12))) + "M"

// ————— Get string corresponding to current and target resolution.
curResString = f_multipleOfRes(1)
resString = f_multipleOfRes(resMult)
// ————— Calculate current and target resolution RSI.
// Current TF rsi.
myRsi = rsi(close, 14)
// No repainting target resolution TF rsi.
myRsiHtf = security(syminfo.tickerid, resString, myRsi[1], lookahead = barmerge.lookahead_on)
// Repainting target resolution TF rsi.
myRsiHtf2 = security(syminfo.tickerid, resString, myRsi)

// ————— Plots
plot(myRsi, "Current TF RSI", color = color.silver)
plot(myRsiHtf, "Target TF no repainting RSI", color = color.green)
plot(myRsiHtf2, "Target TF repainting RSI", color = color.red)
hline(0)
hline(100)
// Show resolution information label.
var lbl = label(na)
if barstate.islast
    label.delete(lbl)
    lbl := label.new(bar_index, max(max(myRsiHtf, myRsi), myRsiHtf2) * 1.1,
      "Current Res = " + curResString + "\nMultiple = " + tostring(resMult) + "\n Target Res = " + resString,
      xloc = xloc.bar_index, yloc =  yloc.price)
```
For v3, use:
```js
//@version=3
//@author=LucF, for PineCoders
study("Multiple of current TF v3")

// Get multiple.
resMult = input(2, minval = 1)

// Returns a multiple of current TF as a string usable with "security()".
f_multipleOfRes(_mult) => 
    // Convert target timeframe in minutes.
    _targetResInMin = interval * _mult * (
      isseconds   ? 1. / 60. :
      isminutes   ? 1. :
      isdaily     ? 1440. :
      isweekly    ? 10080. :
      ismonthly  ? 43800. : na)
      // Find best way to express the TF.
    _targetResInMin     <= 0.0417       ? "1S"  :
      _targetResInMin   <= 0.167        ? "5S"  :
      _targetResInMin   <= 0.376        ? "15S" :
      _targetResInMin   <= 0.751        ? "30S" :
      _targetResInMin   <= 1440         ? tostring(round(_targetResInMin)) :
      _targetResInMin   <= 43800        ? tostring(round(min(_targetResInMin / 1440, 365))) + "D" :
      tostring(round(min(_targetResInMin / 43800, 12))) + "M"

// ————— Calculate current and target resolution RSI.
// Current TF rsi.
myRsi = rsi(close, 14)
// No repainting target resolution TF rsi.
myRsiHtf = security(tickerid, f_multipleOfRes(resMult), myRsi[1], lookahead = barmerge.lookahead_on)
// Repainting target resolution TF rsi.
myRsiHtf2 = security(tickerid, f_multipleOfRes(resMult), myRsi)

// ————— Plots
plot(myRsi, "Current TF RSI", color = silver)
plot(myRsiHtf, "Target TF no repainting RSI", color = green)
plot(myRsiHtf2, "Target TF repainting RSI", color = red)
hline(0)
hline(100)
```

### How can I get the current resolution in a uniform numeric format?
Use the PineCoders `f_resInMinutes()` function to get the current resolution expressed in minutes of type float.
You can then manipulate it and use the `f_resFromMinutes(_minutes)` function to obtain a string usable in `security()`.

```js
//@version=4
study("Resolution in minutes", "", true)
f_resInMinutes() => 
    // Converts current timeframe into minutes of type float.
    _resInMinutes = timeframe.multiplier * (
      timeframe.isseconds   ? 1. / 60. :
      timeframe.isminutes   ? 1. :
      timeframe.isdaily     ? 1440. :
      timeframe.isweekly    ? 10080. :
      timeframe.ismonthly   ? 43800. : na)

f_resFromMinutes(_minutes) =>
    // Converts a resolution expressed in minutes into a string usable by "security()"
    _minutes     <= 0.0417       ? "1S"  :
      _minutes   <= 0.167        ? "5S"  :
      _minutes   <= 0.376        ? "15S" :
      _minutes   <= 0.751        ? "30S" :
      _minutes   <= 1440         ? tostring(round(_minutes)) :
      _minutes   <= 43800        ? tostring(round(min(_minutes / 1440, 365))) + "D" :
      tostring(round(min(_minutes / 43800, 12))) + "M"

f_print(_txt) => t = time + (time - time[1]) * 3, var _lbl = label.new(t, high, _txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large), label.set_xy(_lbl, t, high + 3 * tr)

resInMinutes = f_resInMinutes()
resFromMinutes = f_resFromMinutes(resInMinutes)
f_print("f_resInMinutes() = " + tostring(resInMinutes) +"\nf_resFromMinutes(_minutes) = " + resFromMinutes)
```

### How can I get the resolution in minutes from a string in the `input.resolution` and `timeframe.period` format?
```
//@version=4
study("Resolution in minutes", "")
higherRes = input("1D", "Interval used for security() calls", type = input.resolution)

f_tfResInMinutes(_resolution) =>
    // Returns resolution of _resolution period in minutes.
    // _resolution: resolution of other timeframe (in timeframe.period string format).
    _mult = security(syminfo.tickerid, _resolution, timeframe.multiplier)
    _res = security(syminfo.tickerid, _resolution, timeframe.isseconds ? 1 : timeframe.isminutes ? 2 : timeframe.isdaily ? 3 : timeframe.isweekly ? 4 : timeframe.ismonthly ? 5 : na)
    _return = 
      _res == 1 ? _mult / 60 : 
      _res == 2 ? _mult : 
      _res == 3 ? _mult * 1440 : 
      _res == 4 ? _mult * 10080 : 
      _res == 5 ? _mult * 43800 : na

higherResInMinutes = f_tfResInMinutes(higherRes)

plot(higherResInMinutes, "higherResInMinutes", color.navy, linewidth = 10)
f_print(_txt) => t = time + (time - time[1]) * 3, var _lbl = label.new(t, high, _txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large), label.set_xy(_lbl, t, high + 3 * tr)
f_print("Higher Resolution = " + tostring(higherResInMinutes))
```

### Is it possible to use `security()` on lower intervals than the chart's current interval?
Yes but there are limits to using this technique:
1. It only works on historical bars.
1. You cannot reference intrabars at seconds resolutions. So you can call `security()` at 1m from a 15m chart, but not 30sec.
1. Alerts will currently not work reliably if you use this technique in your script.

If you call `security()` at a lower resolution using a series argument such as `close` or `volume` for its `expression=` parameter, `security()` returns the series' value at the last intrabar, as in the `lastClose` variable in the following script.

If you use a function as the `expression=` argument, then that function will be executed on each intrabar, starting from the earliest one and ending at the most recent, even if the number of intrabars is sometimes irregular. The two functions used in the following code illustrate how you can use `change(time(_res))` (where `_res` is the chart's current resolution) to detect the first intrabar the function is running on:

```js
//@version=4
study("Intrabar inspection")

insideBarNo = input(4, minval=1)
// Current chart resolution. This needs to reflect the chart resolution you want the code working from.
curRes = input("D", "Current resolution")
// Lower TF we are inspecting. Cannot be in seconds and must be lower that chart's resolution.
insideRes = input("60", "Inside resolution")

f_qtyIntrabars(_res) =>
    // Returns qty of intrabars in current chart bar.
    var int _initCnt = 0
    _initCnt := change(time(_res)) ? 1 : _initCnt + 1
    
f_valueAtIntrabar(_src, _bar, _res) =>
    // Returns series value at intrabar n. First intrabar is 1, starting from the earliest.
    var int _barNo = 0
    var float _value = na
    _barNo := change(time(_res)) ? 1 : _barNo + 1
    _value := _barNo == _bar ? _src : _value

// Returns close of last intrabar in "curRes" chart bar.
lastClose = security(syminfo.tickerid, insideRes, close)
// Returns volume at "insideBarNo" intrabar.
valueAtIntrabar = security(syminfo.tickerid, insideRes, f_valueAtIntrabar(volume, insideBarNo, curRes))
// Returns qty of "insideRes" intrabars in "curRes" chart bar.
qtyIntrabars = security(syminfo.tickerid, insideRes, f_qtyIntrabars(curRes))

plotchar(lastClose,"lastClose", "", location = location.top)
plotchar(valueAtIntrabar,"valueAtIntrabar", "", location = location.top)
plot(qtyIntrabars,"qtyIntrabars")
```
[This](https://www.tradingview.com/script/YFBNr8I6-Delta-Volume-Columns-LucF/) is an example of a script that uses the technique illustrated in the functions to calculate delta volume.


**[Back to top](#table-of-contents)**



<br><br>
## ALERTS


### How do I make an alert available from my indicator?
Two steps are required:
1. Insert an `alertcondition()` call in an indicator script.
2. Create an alert from the TV Web user interface (ALT-A) and choose the script's alert condition.

See the User Manual page on [`alertcondition()`](https://www.tradingview.com/pine-script-docs/en/v4/annotations/Alert_conditions.html). Code to create an alert condition looks like:
```js
triggerCondition = close > close[1]
alertcondition(triggerCondition, title = "Create Alert dialog box name", message = "Text sent with alert.")
```
When you need to create multiple alerts you can repeat the method above for every alert you want your indicator to generate, but you can also use the method shown in [this indicator](https://www.tradingview.com/script/8AUuFonD-5-MAs-w-alerts-LucF/). Here, all the different alert conditions are bunched up in one `alertcondition()` statement. In this case, you must provide the means for users to first select which conditions will trigger the alert in the *Inputs* dialog box. When all the required conditions are selected, the user creates an alert using the only alert this indicator makes available, but since TradingView remembers the state of the *Inputs* when creating an alert, only the selected conditions will trigger the alert once it’s created, even if *Inputs* selections are modified by the user after the alert is created.

When more than one condition can trigger a single alert, you will most probably need to have visual cues for each condition so that when users bring up a chart on which an alert triggered they can figure out which condition caused the alert to trigger. This is a method that allows users of your script to customize the alert to their needs.

When TradingView creates an alert, it saves a snapshot of the environment that will enable the alert to run on the servers. The elements saved with an alert are:
- Current symbol
- Current time frame
- State of the script's *Inputs* selections
- Current version of the script. Subsequent updates to the script’s code will not affect the alerts created with prior versions

> Note that while alert condition code will compile in strategy scripts, alerts are only functional in studies.

### I have a custom script that generates alerts. How do I run it on many symbols?
You need to create a separate alert for each symbol. There is currently no way to create an alert for all the symbols in a watchlist or for the Screener.

If one of the generic indicators supplied with the Screener suits your needs and your symbols are tagged with a color label, you can create an alert on those markets from within the Screener.

### Is it possible to use a string that varies as an argument to the `alertcondition()` function's `message=` parameter?
The string may vary conditionally, but it must be of type *const string*, which implies it **must be known at compile time**.

This requirement entails that neither the condition used to build the string nor values used to calculate the string itself can depend on:
- Variables that are only known with the current chart or interval information such as `syminfo.ticker` or `timeframe.period`.
- Calculations with results that can only be determined at runtime, e.g.,: `close > open`, `rsi(14)`, etc.
- Calculations with results known at compile time, but of a type that cannot be cast to *const string*, such as `tostring()`.

The first step when you are in doubt as to what can be used as an argument to a built-in function such as [`alertcondition()`](https://www.tradingview.com/pine-script-reference/v4/#fun_alertcondition) is to look up the Reference Manual:

![.](Refman_alertcondition.png "alertcondition()")

You now know that a *const string* is required as an argument.

The next step is to consult the automatic type casting rules diagram in the User Manual's [*Type system* page](https://www.tradingview.com/pine-script-docs/en/v4/language/Type_system.html#type-casting):

![.](TypeCasting_ConstString.png "Type Casting")

The diagram shows you where the *const string* type is situated in the casting rules, which allows you to determine:
- The types that will be allowed because they are above *const string*, meaning they can be cast to a *const string*.
- The types that will **not** be allowed because they are below *const string*, meaning they **cannot** be cast to a *const string*.

This code shows examples that work and don't work:
```js
//@version=4
study("alertcondition arguments")

// ————— These strings will not work.
// The rsi() value can only be known at runtime time and it is a "series",
// so "wrongMsgArg1" becomes a "series string".
wrongMsgArg1 = "RSI value is:" + tostring( rsi(close, 14))
// This does not work because although the result can be calculated at compile time,
// "tostring()" returns a "simple string" (a.k.a. "string"),
// and automatic casting rules do not allow for that type to be cast to "const string".
wrongMsgArg2 = "Enter at: " + tostring(100.3)
// This fails because the condition can only be evaluated at compile time,
// so the result of the ternary is a "series string".
wrongMsgArg3 = close > open ? "Long Entry" : "Short Entry"

// ————— These strings will work because:
// ————— 1. They can be evaluated at compile time,
// ————— 2. Their type is "literal string" or "const string".
// Test condition "false" is known at compile time and result of ternary is a "const string".
goodMsgArg1 = false ? "Long Entry" : "Short Entry"
// Both values in the expression are literal strings known at compile time. Result is "const string".
goodMsgArg2 = "AAA " + "BBB"

alertcondition(true, title="Id appearing in Create Alert db", message = goodMsgArg1)
```

**[Back to top](#table-of-contents)**



<br><br>
## EDITOR


### How can I access the Pine code of the built-in indicators?
From the Pine Editor, go to the *New* menu and select the built-in you want to work with. Note that some built-ins like the three Volume Profile and the Volume indicators are not written in Pine and their behavior cannot be reproduced in Pine.

### How can I make the console appear in the editor?
Use the CTRL-&#8997; + \` (grave accent) keyboard shortcut or right click on the script's name and choose *Show Console*.

### How can I convert a script from v3 to v4?
With the script open in the editor, choose the *Convert to v4* button at the upper right of the editor window, to the right of the *Save* button.


**[Back to top](#table-of-contents)**



<br><br>
## TECHNIQUES


### How do I save a value or state for later use?
Since v4 the `var` keyword provides a way to initialize variables on the first bar of the dataset only, rather than on every bar the script is run on, as was the case before. This has the very useful benefit of automatically taking care of the value's propagation throughout bars:
```js
//@version=4
study("Variable Initialization")

// Initialization at first bar (bar_index=0) only. Value is propagated across bars.
var initOnce = 0
initOnce := initOnce + 1
// Initialization at each bar. Value is not propagated across bars.
initOnEachBar1 = 0
initOnEachBar1 := initOnEachBar1 + 1
// Initialization at each bar. Value is not propagated across bars,
// so we must refer to the variable's previous value in the series,
// while allowing for the special case on first bar where there is no previous value.
initOnEachBar2 = 0
initOnEachBar2 := nz(initOnEachBar2[1]) + 1

plot(initOnce, "initOnce", color.blue, 10)
plot(initOnEachBar1, "initOnEachBar1", color.red)
plot(initOnEachBar2, "initOnEachBar2", color.orange, 3, transp = 0)
```

See [here](https://www.tradingview.com/pine-script-docs/en/v4/language/Expressions_declarations_and_statements.html#variable-declaration) for more information. This is another example by vitvlkv: [Holding a state in a variable](https://www.tradingview.com/script/llcoIPKG-Pine-Example-Holding-a-state-in-a-variable/).

### How to avoid repainting when using the `security()` function?
See the discussion published with the PineCoders indicator [How to avoid repainting when using security()](https://www.tradingview.com/script/cyPWY96u-How-to-avoid-repainting-when-using-security-PineCoders-FAQ/).

The easiest way is to use the following syntax for v4:
```js
security(syminfo.tickerid, "D", close[1], lookahead = barmerge.lookahead_on)
```
And this for v3:
```js
security(tickerid, "D", close[1], lookahead = barmerge.lookahead_on)
```

### How to avoid repainting when NOT using the `security()` function?
See the discussion published with the PineCoders indicator [How to avoid repainting when NOT using security()](https://www.tradingview.com/script/s8kWs84i-How-to-avoid-repainting-when-NOT-using-security/).

The general idea is to use the confirmed information from the last bar for calculations.

### How can I trigger a condition only when a number of bars have elapsed since the last condition occurred?
Use the [``barssince()``](https://www.tradingview.com/pine-script-reference/v4/#fun_barssince) function:
```js
//@version=4
study("", overlay = true)
len = input(3)
cond = close > open and close[1] > open[1]
trigger = cond and barssince(cond[1]) > len - 1
plotchar(cond)
plotchar(trigger, "", "O", color = color.red)
```

### How can my script identify what chart type is active?
Use everget's [Chart Type Identifier](https://www.tradingview.com/script/8xCRJkGR-RESEARCH-Chart-Type-Identifier/).

### How can I plot the chart's historical high and low?
Notice how we take advantage of the fact that script execution begins at the first bar of the dataset and executes once for each successive bar. By working this way we don't need a `for` loop to go inspect past bars, as our script is already running in a sort of giant loop taking it on each of the dataset's bars, from the oldest to the realtime bar. Scripts with calculations structured in the following way will execute much faster than ones using `for` loops:
```js
//@version=4
study("Plot history's high and low", "", true)
var hi = 0.
var lo = 10e20
hi := max(hi, high)
lo := min(lo, low)
plot(hi, trackprice = true)
plot(lo, trackprice = true)
```
Also note that we are using the `var` keyword to initialize variables only once on the first bar of the dataset. This results in the variable's value being automatically propagated throughout bars so we don't have to use the equivalent of what was necessary in v3 to fetch the value of the variable from the previous bar:
```js
//@version=3
study("Plot history's high and low", "", true)
hi = 0.
lo = 10e20
hi := max(nz(hi[1]), high)
lo := min(nz(lo[1]), low)
plot(hi, trackprice = true)
plot(lo, trackprice = true)
```

### How can I remember when the last time a condition occurred?
The [`barssince()`](https://www.tradingview.com/pine-script-reference/v4/#fun_barssince) built-in function is the simplest way of doing it, as is done in Method 1 in the following script. Method 2 shows an alternate way to achieve the same result as `barssince()`. In Method 2 we watch for the condition as the script is executing on each successive bar, initialize our distance to 0 when we encounter the condition, and until we encounter the condition again, add 1 to the distance at each bar.

In either case the resulting value can be used as an index with the`[]` [history-referecing operator](https://www.tradingview.com/pine-script-docs/en/v4/language/Operators.html#history-reference-operator).
```js
//@version=4
study("Track distance from condition", "", true)
// Plot the high/low from bar where condition occurred the last time.

// Conditions.
upBar = close > open
dnBar = close < open
up3Bars = dnBar and upBar[1] and upBar[2] and upBar[3]
dn3Bars = upBar and dnBar[1] and dnBar[2] and dnBar[3]

// Method 1, using "barssince()".
plot(high[barssince(up3Bars)], linewidth = 10, transp = 80)
plot(low[barssince(dn3Bars)], color = color.red, linewidth = 10, transp=80)

// Method 2, doing manually the equivalent of "barssince()".
var barsFromUp = 0
var barsFromDn = 0
barsFromUp := up3Bars ? 0 : barsFromUp + 1
barsFromDn := dn3Bars ? 0 : barsFromDn + 1
plot(high[barsFromUp])
plot(low[barsFromDn], color = color.red)
plotchar(barsFromUp, "barsFromUp", "", location.top)
plotchar(barsFromDn, "barsFromDn", "", location.top)
```

This script shows how to keep track of the number of bars since the last cross using the same two methods:
```js
//@version=4
study("Bars between crosses", "", true)

maS = sma(close,30)
maF = sma(close,5)
masCross = cross(maF, maS)

// ————— Count number of bars since last crossover: manually or using built-in function.
var barCount1 = 0
barCount1 := masCross ? 0 : barCount1 + 1
barCount2 = barssince(masCross)

// ————— Plots
label.new(bar_index, high + tr, "barCount1: " + tostring(barCount1) + "\nbarCOunt2: " + tostring(barCount2), xloc.bar_index, yloc.price, size = size.small)
plot(maF)
plot(maS, color = color.fuchsia)
```

### How can I track highs/lows for a specific timeframe?
This code shows how to do that without using `security()` calls, which slow down your script. The source used to calculate the highs/lows can be selected in the script's *Inputs*, as well as the period after which the high/low must be reset.
```js
//@version=4
//@author=LucF, for PineCoders
study("Periodic hi/lo", "", true)
showHi = input(true, "Show highs")
showLo = input(true, "Show lows")
srcHi = input(high, "Source for Highs")
srcLo = input(low, "Source for Lows")
period = input("D", "Period after which hi/lo is reset", input.resolution)

var hi = 10e-10
var lo = 10e10
// When a new period begins, reset hi/lo.
hi := change(time(period)) ? srcHi : max(srcHi, hi)
lo := change(time(period)) ? srcLo : min(srcLo, lo)

plot(showHi ? hi : na, "Highs", color.blue, 3, plot.style_circles)
plot(showLo ? lo : na, "Lows", color.fuchsia, 3, plot.style_circles)
```

### How can I track highs/lows for a specific period of time?
We use session information in the 2-parameter version of the [`time`](https://www.tradingview.com/pine-script-reference/v4/#fun_time) function to test if we are in the user-defined hours during which we must keep track of the highs/lows. A setting allows the user to choose if he wants levels not to plot outside houts. It's the default.
```js
//@version=4
//@author=LucF, for PineCoders
study("Session hi/lo", "", true)
noPlotOutside = input(true, "Don't plot outside of hours")
showHi = input(true, "Show highs")
showLo = input(true, "Show lows")
srcHi = input(high, "Source for Highs")
srcLo = input(low, "Source for Lows")
timeAllowed = input("1200-1500", "Allowed hours", input.session)

// Check to see if we are in allowed hours.
timeIsAllowed = time(timeframe.period, timeAllowed)
var hi = 10e-10
var lo = 10e10
if timeIsAllowed
    // We are entering allowed hours; reset hi/lo.
    if not timeIsAllowed[1]
        hi := srcHi
        lo := srcLo
    else
        // We are in allowed hours; track hi/lo.
        hi := max(srcHi, hi)
        lo := min(srcLo, lo)

plot(showHi and not(noPlotOutside and not timeIsAllowed)? hi : na, "Highs", color.blue, 3, plot.style_circles)
plot(showLo and not(noPlotOutside and not timeIsAllowed)? lo : na, "Lows", color.fuchsia, 3, plot.style_circles)
```
![.](https://www.tradingview.com/x/nxoCwdMs/ "Session Hi/Lo")

### How can I track highs/lows between specific intrabar hours?
We use the intrabar inspection technique explained [here](http://www.pinecoders.com/faq_and_code/#is-it-possible-to-use-security-on-lower-intervals-than-the-charts-current-interval) to inspect intrabars and save the high or low if the intrabar is whithin user-defined begin and end times.

```js
//@version=4
//@author=LucF, for PineCoders
study("Pre-market high/low", "", true)
begHour = input(7, "Beginning time (hour)")
begMinute = input(0, "Beginning time (minute)")
endHour = input(9, "End time (hour)")
endMinute = input(25, "End time (minute)")
// Lower TF we are inspecting. Cannot be in seconds and must be lower that chart's resolution.
insideRes = input("5", "Intrabar resolution used")

startMinute = (begHour * 60) + begMinute
finishMinute = (endHour * 60) + endMinute

f_highBetweenTime(_start, _finish) =>
    // Returns low between specific times.
    var float _return = 0.
    var _reset = true
    _minuteNow = (hour * 60) + minute
    if _minuteNow >= _start and _minuteNow <= _finish
        // We are inside period.
        if _reset
            // We are at first bar inside period.
            _return := high
            _reset := false
        else
            _return := max(_return, high)
    else
        // We are past period; enable reset for when we next enter period.
        _reset := true
    _return

f_lowBetweenTime(_start, _finish) =>
    // Returns low between specific times.
    var float _return = 10e10
    var _reset = true
    _minuteNow = (hour * 60) + minute
    if _minuteNow >= _start and _minuteNow <= _finish
        // We are inside period.
        if _reset
            // We are at first bar inside period.
            _return := low
            _reset := false
        else
            _return := min(_return, low)
    else
        // We are past period; enable reset for when we next enter period.
        _reset := true
    _return

highAtTime = security(syminfo.tickerid, insideRes, f_highBetweenTime(startMinute, finishMinute))
lowAtTime = security(syminfo.tickerid, insideRes, f_lowBetweenTime(startMinute, finishMinute))
plot(highAtTime, "High", color.green)
plot(lowAtTime, "Low", color.red)
```

### How can I count the occurrences of a condition in the last x bars?
The built-in [`sum()`](https://www.tradingview.com/pine-script-reference/v4/#fun_sum) function is the most efficient way to do it, but its length (the number of last bars in your sample) cannot be a series float or int. This script shows three different ways of achieving the count:

1. *Method 1* uses the `sum()` built-in.
1. *Method 2* uses a technique that is also efficient, but not as efficient as the built-in. It has the advantage of accepting a series float or int as a length.
1. *Method 3* also accepts a series float or int as a length, but is very inefficient because it uses a `for` loop to go back on past bars at every bar. Examining all *length* bars at every bar is unnecessary since all of them except the last bar have already been examined previously when the script first executed on them. This makes for slower code and will be detrimental to chart loading time.

*Method 2* is a very good example of the *Pine way* of doing calculations by taking advantage of series and a good understanding of the Pine runtime environment to code our scripts. While it is useful to count occurrences of a condition in the last x bars, it is also worth studying because the technique it uses will allow you to write much more efficient Pine code than one using a `for` loop when applied to other situations. There are situations when using a `for` loop is the only way to realize what we want, but in most cases they can be avoided. `for` loops are the only way to achieve **some** types of backward analysis when the criteria used are only known after the bars to analyze have elapsed.
```js
//@version=4
//@author=LucF, for PineCoders

// TimesInLast - PineCoders FAQ
//  v1.0, 2019.07.15 19:37 — Luc 

// This script illustrates 3 different ways of counting the number of occurrences when a condition occured in the last len bars.
// By using the script's Settings/Inputs you can choose between 4 types of length to use with the functions.
// If you look at results in the Data Window, you will see the impact of sending different types of length to each of the functions.

// Conclusions: 
//      - Unless your length is of series type, use Method 1.
//      - Use Method 2 if you need to be able to use a series int or series float length.
//      - Never use Method 3.
study("TimesInLast - PineCoders FAQ")

// Change this value when you want to use different lengths.
// Inputs cannot be change through Settings/Inputs; only the form-type.
deflen = 100

// ————— Allow different types to be specified as length value.
// This part is only there to show the impact of using different form-types of length with the 3 functions.
// In normal situation, we would just use the following: len = input(100, "Length")
LT1 = "1. input int", LT2 = "2. input float", LT3="3. series int", LT4="4. series float"
lt = input(LT1, "Type of 'length' argument to functions", options=[LT1, LT2, LT3, LT4])
len1 = input(deflen, LT1, type=input.integer, minval=deflen, maxval=deflen)
len2 = input(deflen, LT2, type=input.float, minval=deflen, maxval=deflen)
var len3 = 0
len3 := len3 == deflen ? len3 : len3 + 1
var len4 = 0.
len4 := len4 == deflen ? len4 : len4 + 1
// Choose proper form-type of length.
len = lt == LT1 ? len1 : lt == LT2 ? len2 : lt == LT3 ? len3 : lt == LT4 ? len4 : na

// Condition on which all counts are done.
condition = close > open

// ————— Method 1. This function uses Pine's built-in function but only accepts a simple int for the length.
f_ideal_TimesInLast(_cond, _len) =>  sum(_cond ? 1 : 0, _len)

// ————— Method 2. This function is equivalent to using sum() but works with a float and series value for _len.
f_verboseButEfficient_TimesInLast(_cond, _len) =>
    // For first _len bar we just add to cumulative count of occurrences.
    // After that we add count for current bar and make adjustment to count for the tail bar in our mini-series of length=_len.
    var _qtyBarsInCnt = 0
    var _cnt = 0
    if _cond
        // Add to count as per current bar's condition state.
        _cnt := _cnt + 1
    if _qtyBarsInCnt < _len
        // We have not counted the first _len bars yet; keep adding to checked bars count.
        _qtyBarsInCnt := _qtyBarsInCnt + 1
    else
        // We already have a _len bar total, so need to subtract last count at the tail of our _len length count.
        if _cond[_len]
            _cnt := _cnt - 1
    _qtyBarsInCnt == _len ? _cnt : na // Use this to return na until first _len bars have elapsed, as built-in "sum()" does.
    // _cnt // Use this when you want the running count even if full _len bars haven't been examined yet.

// ————— Method 3. Very inefficient way to go about the problem. Not recommended.
f_verboseAndINEFFICIENT_TimesInLast(_cond, _len) =>
    // At each bar we loop back _len-1 bars to re-count conditions that were already counted in previous calls, except for the current bar's condition.
    _cnt = 0
    for _i = 0 to _len - 1
        if na(_cond[_i])
            _cnt := na
        else
            if _cond[_i]
                _cnt := _cnt + 1
    _cnt

// ————— Plots
v1 = f_ideal_TimesInLast(condition, int(len))
v2 = f_verboseButEfficient_TimesInLast(condition, int(len))
v3 = f_verboseAndINEFFICIENT_TimesInLast(condition, int(len))
plot(v1, "1. f_ideal_TimesInLast", color.fuchsia)
plot(v2, "2. f_verboseButEfficient_TimesInLast", color.orange)
plot(v3, "3. f_verboseAndINEFFICIENT_TimesInLast")
// Plot red background on discrepancies between results.
bgcolor(v1 != v2 or v2 != v3 ? color.red : na, transp = 80)
```

### How can I implement and On/Off switch?
```js
//@version=4
study("On/Off condition", "", true)
upBar = close > open
// On/off conditions.
triggerOn = upBar and upBar[1] and upBar[2]
triggerOff = not upBar and not upBar[1]
// Switch state is implicitly saved across bars thanks to initialize-only-once keyword "var".
var onOffSwitch = false
// Turn the switch on when triggerOn is true. If it is already on,
// keep it on unless triggerOff occurs.
onOffSwitch := triggerOn or (onOffSwitch and not triggerOff)
bgcolor(onOffSwitch ? color.green : na)
plotchar(triggerOn, "triggerOn", "▲", location.belowbar, color.lime, 0, size = size.tiny, text = "On")
plotchar(triggerOff, "triggerOff", "▼", location.abovebar, color.red, 0, size = size.tiny, text = "Off")
```

### How can I allow transitions from condition A►B or B►A, but not A►A nor B►B
One way to do it is by using [`barssince()`](https://www.tradingview.com/pine-script-reference/v4/#fun_barssince). This way is more flexible and faster:
```js
//@version=4
//@author=LucF, for PineCoders
study("AB or BA", "", true)

// ————— Trigger conditions.
upBar = close > open
condATrigger = upBar and upBar[1]
condBTrigger = not upBar and not upBar[1]
// ————— Conditions. These variable will only be true/false on the bar where they occur.
condA = false
condB = false
// ————— State variable set to true when last triggered condition was A, and false when it was condition B.
// This variable's state is propagated troughout bars (because we use the "var" keyword to declare it).
var LastCondWasA = false

// ————— State transitions so that we allow A►B or B►A, but not A►A nor B►B.
if condATrigger and not LastCondWasA
    // The trigger for condA occurs and the last condition set was condB.
    condA := true
    LastCondWasA := true
else
    if condBTrigger and LastCondWasA
        // The trigger for condB occurs and the last condition set was condA.
        condB := true
        LastCondWasA := false

bgcolor(LastCondWasA ? color.green : na)
plotchar(condA, "condA", "▲", location.belowbar, color.lime, 30, size = size.tiny, text = "A")
plotchar(condB, "condB", "▼", location.abovebar, color.red, 30, size = size.tiny, text = "B")
// Note that we do not plot the marker for triggers when they are allowed to change states, since we then have our condA/B marker on the chart.
plotchar(condATrigger and not condA, "condATrigger", "•", location.belowbar, color.green, 0, size = size.tiny, text = "a")
plotchar(condBTrigger and not condB, "condBTrigger", "•", location.abovebar, color.maroon, 0, size = size.tiny, text = "b")
```

### How can I rescale an indicator from one scale to another?
The answer depends on whether you know the minimum/maximum possible values of the signal to be rescaled. If you don't know them, as is the case for volume where the maximum is unknown, then you will need to use a function that uses past history to determine the minimum/maximum values, as in the `normalize()` function here. While this is an imperfect solution since the minimum/maximum need to be discovered as your script progresses left to right through historical bars, it is better than techniques using `lowest()` and `highest()` over a fixed length, because it uses the minimum/maximum values for the complete set of elapsed bars rather than a subset of fixed length. The ideal solution would be to know in advance the minimum/maximum values for the whole series **prior** to beginning the normalization process, but this is currently not possible in Pine.

If you know the minimum/maximum values of the series, then you should use the `rescale()` function:
```js
//@version=4
//@author=LucF, for PineCoders
study("Normalizer")

// ————— When scale of signal to rescale is unknown.
// Min/Max of signal to rescale is determined by its historical low/high.
normalize(_src, _min, _max) => 
    // Normalizes series with unknown min/max using historical min/max.
    // _src: series to rescale.
    // _min: minimum value of rescaled series.
    // _max: maximum value of rescaled series.
    var _historicMin = 10e10
    var _historicMax = -10e10
    _historicMin := min(nz(_src, _historicMin), _historicMin)
    _historicMax := max(nz(_src, _historicMax), _historicMax)
    _min + (_max - _min) * (_src - _historicMin) / max(_historicMax - _historicMin, 10e-10)
plot(normalize(volume, -100, 100))

// ————— When scale of signal to rescale is known.
rescale(_src, _oldMin, _oldMax, _newMin, _newMax) =>
    // Rescales series with known min/max.
    // _src: series to rescale.
    // _oldMin: minimum value of series to rescale.
    // _oldMax: maximum value of series to rescale.
    // _newMin: minimum value of rescaled series.
    // _newMax: maximum value of rescaled series.
    _newMin + (_newMax - _newMin) * (_src - _oldMin) / max(_oldMax - _oldMin, 10e-10)
plot(rescale(rsi(close, 14), 0, 100, -100, 100), color = color.fuchsia)
```

### How can I monitor script run time?
Use the code from the PineCoders [Script Stopwatch](https://www.tradingview.com/script/rRmrkRDr-Script-Stopwatch-PineCoders-FAQ/). You will be able to time script execution so you can explore different scenarios when developing code and see for yourself which version performs the best.

### How can I save a value when an event occurs?
The key to this technique is declaring a variable using the `var` keyword. While there are other ways to accomplish our task in Pine, this is the simplest. When you declare a variable using the `var` keyword, the variable is initialized only once at bar_index zero, rather than on each bar. This has the effect of preserving the variable's value without the explicit re-assignement that was required in earlier versions of pine where you would see code like this:
```js
priceAtCross = 0.
priceAtCross := nz(priceAtCross[1])
```
This was required because the variable was reassigned the value `0.` at the beginning of each bar, so to remember its last value, it had to be *manually* reset to its last bar's value on each bar. This is now unnecessary with the `var` keyword and makes for cleaner code:
```
//@version=4
study("Save a value when an event occurs", "", true)
hiHi = highest(high, 5)[1]
var float priceAtCross = na
if crossover(close, hiHi)
    // When a cross occurs, save price. Since variable was declared with "var" keyword,
    // it will then preserve its value until the next reassignment occurs at the next cross.
    // Very important to use the ":=" operator here, otherwise we would be creating a second,
    // instance of the priceAtCross" variable local to the "if" block, which would disappear
    // once the "if" block was exited, and the global variable "priceAtCross"'s value would then not have changed.
    priceAtCross := close
plot(hiHi)
plot(priceAtCross, "Price At Cross", color.orange, 3, plot.style_circles)
```

### How can I count touches of a specific level?
This technique shows one way to count touches of a level that is known in advance (the median in this case). We keep a separate tally of up and down bar touches, and account for gaps across the median. Every time a touch occurs, we simply save a 1 value in a series. We can then use the [`sum()`](https://www.tradingview.com/pine-script-reference/v4/#fun_sum) function to count the number of ones in that series in the last `lookBackTouches` bars.

Note that the script can be used in overlay mode to show the median and touches on the chart, or in pane mode to show the counts. Change the setting of the `overlay` variable accordingly and re-add the indicator to the chart to implement the change.

```js
//@version=4
//@author=LucF, for PineCoders

// Median Touches
//  v1.0, 2020.01.02 13:01 — LucF

// Can work in overlay or pane mode and plots differently for each case.
overlay = true
study("Median Touches", "", overlay)
lookBackMedian = input(100)
lookBackTouches = input(50)
median = percentile_nearest_rank(close, lookBackMedian, 50)
// Don't count neutral touches when price doesn't move.
barUp = close > open
barDn = close < open
// Bar touches median.
medianTouch     = high    > median and low  < median
gapOverMedian   = high[1] < median and low  > median
gapUnderMedian  = low[1]  > median and high < median
// Record touches.
medianTouchUp = (medianTouch and barUp) or gapOverMedian  ? 1 : 0
medianTouchDn = (medianTouch and barDn) or gapUnderMedian ? 1 : 0
// Count touches.
touchesUp = sum(medianTouchUp, lookBackTouches)
touchesDn = sum(medianTouchDn, lookBackTouches)
// —————————— Plots
// ————— Both modes
// Markers
plotchar(medianTouchUp, "medianTouchUp", "▲", overlay ? location.belowbar : location.bottom, color.lime)
plotchar(medianTouchDn, "medianTouchDn", "▼", overlay ? location.abovebar : location.top, color.red)
// ————— Overlay mode
// Median for overlay mode.
plot(overlay ? median : na, "Median", color.orange)
// ————— Pane mode
// Base areas.
lineStyle = overlay ? plot.style_line : plot.style_columns
plot(not overlay ? touchesUp : na, "Touches Up", color.green, style = lineStyle)
plot(not overlay ? - touchesDn : na, "Touches Dn", color.maroon, style = lineStyle)
// Exceeding area.
minTouches = min(touchesUp, touchesDn)
minTouchesIsUp = touchesUp < touchesDn
p_basePlus = plot(not overlay ? minTouches : na, "Base Plus", #00000000)
p_hiPlus = plot(not overlay and not minTouchesIsUp ? touchesUp : na, "High Plus", #00000000)
fill(p_basePlus, p_hiPlus, color.lime, transp = 0)
p_baseMinus = plot(not overlay ? - minTouches : na, "Base Plus", #00000000)
p_loMinus = plot(not overlay and minTouchesIsUp ? - touchesDn : na, "Low Minus", #00000000)
fill(p_baseMinus, p_loMinus, color.red, transp = 0)
```
![.](https://www.tradingview.com/x/SJZzmMfN/ "Median touches")

**[Back to top](#table-of-contents)**




<br><br>
## DEBUGGING

### How can I examine the value of a string in my script?
This code will show a label containing the current values of the variables you wish to see. Non-string variables need to be converted to strings using `tostring()`. The label will show when price changes in the realtime bar, so the code needs to run on a live chart.
```js
//@version=4
study("f_print()", "", true)
f_print(_txt) => t = time + (time - time[1]) * 3, var _lbl = label.new(t, high, _txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large), label.set_xy(_lbl, t, high + 3 * tr)
f_print("Multiplier = " + tostring(timeframe.multiplier) + "\nPeriod = " + timeframe.period + "\nHigh = " + tostring(high))
```

![.](https://www.tradingview.com/x/BfsB2BqJ/ "f_print()")

### How can I plot numeric values so that they do not disrupt the indicator's scale?
The solution is to use the `plotchar()` function, but without actually printing a character, and using the fact that values plotted with `plotchar()` will appear both:
- in the Indicator's values (their display is controlled by the chart's *Settings/Status Line/Indicator Values* checkbox)
- in the Data Window (third icon down the list at the right of your TV window)

The reason for using the `location = location.top` parameter is that `plotchar()` uses `location.abovebar` as the default when the `location=` parameter is not specified, and this puts price into play in your indicator's scale, even if no character is actually plotted by `plotchar()`.

Note that you may use `plotchar()` to test variables of string type, but only by comparing them to a single string, as is done in the second `plotchar()` call in the following code:
```js
//@version=4
study("Printing values with plotchar()")
plotchar(bar_index, "Bar Index", "", location = location.top)
// This will be true (1) when chart is at 1min. Otherwise it will show false (0).
plotchar(timeframe.period == "1", "timeframe.period='1'", "", location = location.top)
```

![.](printing_values_with_plotchar.png "Printing values with plotchar()")

Note that:
- The indicator's scale is not affected by the `bar_index` value of `11215` being plotted.
- The value of `1` printed by the second call to `plotchar()`, indicating that we are on a 1 min chart.
- Values appear in both the indicator's values and the Data Window, even if nothing is plotted in the indicator's scale.

### How can I visualize many different states?
This code displays green or red squares corresponding to the two different states of four different conditions, and colors the background when they are either all true or all false:
```js
//@version=4
study("Debugging states with plotshape() and bgcolor()")
cond1 = close > open
cond2 = close > close[1]
cond3 = volume > volume[1]
cond4 = high - close < open - low
cond5 = cond1 and cond2 and cond3 and cond4
cond6 = not (cond1 or cond2 or cond3 or cond4)
plotshape(9, "cond1", shape.square, location.absolute, cond1 ? color.green : color.red, size = size.tiny)
plotshape(8, "cond2", shape.square, location.absolute, cond2 ? color.green : color.red, size = size.tiny)
plotshape(7, "cond3", shape.square, location.absolute, cond3 ? color.green : color.red, size = size.tiny)
plotshape(6, "cond4", shape.square, location.absolute, cond4 ? color.green : color.red, size = size.tiny)
bgcolor(cond5 ? color.green : cond6 ? color.red : na, title = "cond5/6")
```

![.](debugging_states_with_plotshape_and_bgcolor.png "Debugging states with plotshape() and bgcolor()")

You could also use `plot()` to achieve a somewhat similar result. Here we are plotting the condition number only when the condition is true:
```js
//@version=4
study("Debugging states with plot() and bgcolor()")
// ————— States
cond1 = close > open
cond2 = close > close[1]
cond3 = volume > volume[1]
cond4 = high - close < open - low
cond5 = cond1 and cond2 and cond3 and cond4
cond6 = not (cond1 or cond2 or cond3 or cond4)
plot(cond1 ? 1 : na, "cond1", linewidth = 4, style = plot.style_circles)
plot(cond2 ? 2 : na, "cond2", linewidth = 4, style = plot.style_circles)
plot(cond3 ? 3 : na, "cond3", linewidth = 4, style = plot.style_circles)
plot(cond4 ? 4 : na, "cond4", linewidth = 4, style = plot.style_circles)
bgcolor(cond5 ? color.green : cond6 ? color.red : na, title = "cond5/6")
```

![.](debugging_states_with_plot_and_bgcolor.png "Debugging states with plot() and bgcolor()")

### How can I visualize my script's conditions on the chart?
When building compound conditions that rely on the accuracy of multiple underlying conditions used as building blocks, you will usually  want to confirm your code is correctly identifying the underlying conditions. Here, markers identifying them are plotted at the top and bottom of the chart using `plotshape()`, while the compound conditions 5 an 6 are marked above and below bars using `plotshape()`, and one bar later using `plotchar()` and a Unicode character:
```js
//@version=4
study("Plotting markers with plotshape()", "", true)
cond1 = close > open
cond2 = close > close[2]
cond3 = volume > volume[1]
cond4 = high - close < open - low
cond5 = cond1 and cond2 and cond3 and cond4
cond6 = not (cond1 or cond2 or cond3 or cond4)
plotshape(cond1, "cond1", shape.circle, location.top, color.silver, text = "1", size = size.small)
plotshape(cond2, "cond2", shape.diamond, location.top, color.orange, text = "2", size = size.tiny)
plotshape(cond3, "cond3", shape.circle, location.bottom, color.fuchsia, text = "3", size = size.small)
plotshape(cond4, "cond4", shape.diamond, location.bottom, color.aqua, text = "4", size = size.tiny)
plotshape(cond5, "cond5", shape.triangleup, location.belowbar, color.green, 0, text = "cond5", size = size.tiny)
plotshape(cond6, "cond6", shape.triangledown, location.abovebar, color.maroon, 0, text = "cond6", size = size.tiny)
// Place these markers one bar late so they don't overprint the "plotshape()" triangles.
plotchar(cond5[1], "cond5", "⮝", location.belowbar, color.lime, 0, size = size.tiny)
plotchar(cond6[1], "cond6", "⮟", location.abovebar, color.red, 0, size = size.tiny)
```

![.](https://www.tradingview.com/x/BUkdl478/ "Plotting markers with plotshape()")

You will find lists of Unicode arrows [here](https://www.key-shortcut.com/en/writing-systems/35-symbols/arrows/) and [here](http://xahlee.info/comp/unicode_arrows.html). Because they are not all mapped in the MS Trebuchet font TV uses, not all characters will work with `plotchar()`. Some work as arguments to the `text=` parameter, but not as arguments to `char=`.


**[Back to top](#table-of-contents)**
