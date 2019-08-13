[<img src="http://pinecoders.com/images/PineCodersLong.png">](http://pinecoders.com)

# FAQ & Code

This is a compendium of frequently asked questions on Pine. Answers often give code examples or link to the best sources on the subject.

### Table of Contents

- [Built-in variables](#built-in-variables)
- [Built-in functions](#built-in-functions)
- [Operators](#operators)
- [Plotting](#plotting)
- [Indicators (a.k.a. studies)](#indicators)
- [Strategies](#strategies)
- [Time and dates](#time-and-dates)
- [Other intervals (MTF)](#other-intervals-mtf)
- [Alerts](#alerts)
- [Techniques](#techniques)



<br><br>
## BUILT-IN VARIABLES


### What is the variable name for the current price? 
The `close` variable holds both the price at the close of historical bars and the current price when an **indicator** is running on the realtime bar. If the script is a **strategy** running on the realtime bar, by default it runs only at the bar's close. If the `calc_on_every_tick` parameter of the `strategy()` declaration statement is set to `true`, the strategy will behave as an indicator and run on every price change of the realtime bar.

To access the close of the previous bar's close in Pine, use `close[1]`. In Pine, brackets are used as the [history-referencing operator](https://www.tradingview.com/pine-script-docs/en/v4/language/Operators.html#history-reference-operator).

### What is the code for a green candle?
```
greenCandle = close > open
```
Once you have defined the `greenCandle` variable, if you wanted a boolean variable to be `true` when the last three candles were green ones, you could write:
```
threeGreenCandles = greenCandle and greenCandle[1] and greenCandle[2]
```
> Note that the variable name `3GreenCandles` would have caused a compilation error. It is not legal in Pine as it begins with a digit.

If you need to define up and down candles, then make sure one of those definitions allows for the case where the `open` and `close` are equal:
```
upCandle = close >= open
downCandle = close < open
```

**[Back to top](#table-of-contents)**



<br><br>
## BUILT-IN FUNCTIONS


### Why do I get an error message when using `highest()` or `lowest()`?
Most probably because you are trying to use a series instead of an integer as the second parameter (the length). Either use a [simple integer](https://www.tradingview.com/pine-script-docs/en/v4/language/Type_system.html#simple) or use the [RicardoSantos](https://www.tradingview.com/u/RicardoSantos/#published-scripts) replacements [here](https://www.tradingview.com/script/32ohT5SQ-Function-Highest-Lowest/). If you don't know Ricardo, take the time to look at his indicators while you're there. Ricardo is among the most prolific and ingenious Pinescripters out there.

**[Back to top](#table-of-contents)**



<br><br>
## OPERATORS


### What's the difference between `==`, `=` and `:=`?
`==` is a [comparison operator](https://www.tradingview.com/pine-script-docs/en/v4/language/Operators.html#comparison-operators) used to test for true/false conditions.<br>
`=` is used to [declare and initialize variables](https://www.tradingview.com/pine-script-docs/en/v4/language/Expressions_declarations_and_statements.html#variable-declaration).<br>
`:=` is used to [assign values to variables](https://www.tradingview.com/pine-script-docs/en/v4/language/Expressions_declarations_and_statements.html#variable-assignment) after initialization, transforming them into *mutable variables*.
```
//@version=3
study("")
a = 0
b = 1
plot(a == 0 ? 1 : 2)
plot(b == 0 ? 3 : 4, color = orange)
a := 2
plot(a == 0 ? 1 : 2, color = aqua)
```

**[Back to top](#table-of-contents)**



<br><br>
## PLOTTING


### Can I plot diagonals between two points on the chart?
Yes, using the [`line.new()`](https://www.tradingview.com/pine-script-reference/v4/#fun_line{dot}new) function available in v4.

### How do I plot a line using start/stop criteria?
You'll need to define your start and stop conditions and use logic to remember states and the level you want to plot.

Note the combination of plotting `na` and using the `style = plot.style_linebr` parameter to avoid a continuous line to be plotted, including inelegant joins when it changes levels.
```
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
// Determine if a line start/stop condition has occured.
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

### How do I plot a support or a trend line line?
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
The limit for plots is 64. Note than one plot statement can use up more than one allowed plot, depending on how it is structured.
The limit for `security()` calls is 40.
The limit for variables is 1000.
We do not know of a limit to the number of lines in a script. There is, however a limit of 50K compiled tokens, but they don't correspond to code lines.

### How can I use colors in my indicator plots?
See [Working with colours](https://kodify.net/tradingview/colours/) by Kodify.

### How do I make my indicator plot over the chart?
Use `overlay=true` in `strategy()` or `study()` declaration statement, e.g.,:
```
study("My Script", overlay = true)
```
If your indicator was already in a Pane before applying this change, you will need to use Add to Chart again for the change to become active.

### Can I use `plot()` calls in a `for` loop?
No, but you can use the v4 [`line.new()`](https://www.tradingview.com/pine-script-reference/v4/#fun_line{dot}new) function in `for` loops.

**[Back to top](#table-of-contents)**



<br><br>
## INDICATORS


### Can I create an indicator that plots like the built-in Volume or Volume Profile indicators?
No.

### How do I feed the output of one script to another script?
Use the following in your code:
```
ExternalIndicator = input(close, "External Indicator")
```
From the script's *Inputs* you will then be able to select a plot from another indicator if it present on your chart.
You can use only one such statement in your script. If you use more than one, the other indicator plots will not be visible from the *Inputs* dropdown.
You cannot use this technique in strategies.

### Can I write a script that plots like the built-in Volume Profile or Volume indicators?
No. TradingView uses special code for these that is not available to standard Pine scripts.

### How can I use one script's output as an input into another?
See how our [Signal for Backtesting-Trading Engine](https://www.tradingview.com/script/y4CvTwRo-Signal-for-Backtesting-Trading-Engine-PineCoders/) can be integrated as an input to our [Backtesting-Trading Engine](https://www.tradingview.com/script/dYqL95JB-Backtesting-Trading-Engine-PineCoders/).

### Is it possible to export indicator data to a file?
No. The only way for now is through screen scraping.

### Can my script place something on the chart when it is running from a pane?
The only thing that can be changed on the chart from within a pane is the color of the bars. See the [`barcolor()`](https://www.tradingview.com/pine-script-docs/en/v4/annotations/Barcoloring_a_series_with_barcolor.html) function.

### Can I merge 2 or more indicators into one?
Sure, but start by looking at the scale each one is using. If you're thinking of merging a moving average indicator designed to plot on top of candles and in relation to them, you are going to have problems if you also want to include and indicator showing volume bars in the same script because their values are not on the same scale.

Once you've made sure your scales will be compatible (or you have devised a way of normalizing/re-scaling them), it's a matter of gathering the code from all indicators into one script and removing any variable name collisions so each indicator's calculations retain their independence and integrity.

> Note that if the indicators you've merged are CPU intensive, you may run into runtime limitations when executing the compound script.

**[Back to top](#table-of-contents)**



<br><br>
## STRATEGIES


### How do I implement date range filtering in strategies?
```
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
```
EnterLong = GoLong and TradeDateIsAllowed()
```
> Note that with this code snippet, date filtering can be enabled/disabled using a checkbox. This way you don't have to reset dates when filtering is no longer needed; just uncheck the box.

### How do I write code for a signal with 2 conditions that occur at different times?
Backtest Rookies has a [blog post](https://backtest-rookies.com/2018/10/26/tradingview-opening-a-window/) on the subject.

### How can I save the entry price in a strategy?
See [How to Plot Entry Price](https://www.tradingview.com/script/bHTnipgY-HOWTO-Plot-Entry-Price/) by vitvlkv

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

**[Back to top](#table-of-contents)**



<br><br>
## OTHER INTERVALS (MTF)

**[Back to top](#table-of-contents)**



<br><br>
## ALERTS


### How do I make an alert available from my indicator?
Two steps are required:
1. Insert an `alertcondition()` call in an indicator script.
2. Create an alert from the TV Web user interface (ALT-A) and choose the script's alert condition.

See the User Manual page on [`alertcondition()`](https://www.tradingview.com/pine-script-docs/en/v4/annotations/Alert_conditions.html). Code to create an alert condition looks like:
```
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
```
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

alertcondition(true, title="Id appearing in Create Alert db", message = goodMsgArg1)```
```

**[Back to top](#table-of-contents)**



<br><br>
## TECHNIQUES


### How do I save a value or state for later use?
Since v4 there exists a simpler way to save variable value from bar to bar, using the `var` keyword when initializing variables. See [here](https://www.tradingview.com/pine-script-docs/en/v4/language/Expressions_declarations_and_statements.html#variable-declaration) for more information. When using earlier versions of Pine, the following articles will be more useful:

- Backtest Rookies has a [blog post](https://backtest-rookies.com/2018/11/23/tradingview-save-a-variable-store-a-value-for-later/) on the subject.
- Pine Example: [Holding a state in a variable](https://www.tradingview.com/script/llcoIPKG-Pine-Example-Holding-a-state-in-a-variable/) by vitvlkv.

### How do I calculate averages?
1. If you just want the average between two values, you can use `avg(val1, val2)` or `(val1 + val2)/2`. Note that the [`avg()`](https://www.tradingview.com/pine-script-reference/v4/#fun_avg) accepts up to 6 values.
1. To average the last x values in a series, you can use `sma(series, x)`.

### How can I calculate an average only when a certain condition is true?
[This script](https://www.tradingview.com/script/isSfahiX-Averages-PineCoders-FAQ/) shows how to calculate a conditional average using three different methods.

### How to avoid repainting when using the ``security()`` function?
See the discussion published with the PineCoders indicator [How to avoid repainting when using security()]().

The easiest way is to use the following syntax for v4:
```
security(syminfo.tickerid, “D”, close[1], lookahead = barmerge.lookahead_on)
```
And this for v3:
```
security(tickerid, “D”, close[1], lookahead = barmerge.lookahead_on)
```


**[Back to top](#table-of-contents)**

