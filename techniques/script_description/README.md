<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-147975914-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-147975914-1');
</script>

[<img src="https://www.pinecoders.com/images/PineCodersLong.png">](https://www.pinecoders.com/)

# How PineCoders Write and Format Their Script Descriptions

### Table of Contents

- [Introduction](#introduction)
- [Our Building Blocks](#our-building-blocks)
- [A Description, Step by Step](#a-description-step-by-step)
- [Tips](#tips)


<br><br>
## Introduction
This document explains how we write and format our script descriptions for publication on TradingView. We aim for our descriptions to **provide the most useful and legible information enabling users of our scripts to understand and use them advantageously**.

In order to achieve this, we:
- Order the content vertically by decreasing relevance to the understanding of our script.
- Aim to achieve maximal legibility while using minimal graphic/typographic attributes.
- Write the first sentence or two extra carefully, as they will be visible in the script's widget, which users will see before opening our script's page. We want that first sentence or two to adequately summarize our script.

<br><br>
## Our Building Blocks

### Markup
The following markup is available in script descriptions. You can access all these tags except the Pine code block tags from the list of icons at the top of the "Publish script" or "Edit script" window:

[<img src="TagIcons.png">](https://www.pinecoders.com/techniques/script_description/TagIcons.png)

#### Bold and Italics
```
This text will produce [i]italics[/i], [b]bold[/b] and [b][i]bold italics[/i][/b].
```
and will look like this:

[<img src="BoldItalics.png">](https://www.pinecoders.com/techniques/script_description/BoldItalics.png)

We try to use bold and italics sparingly. We use bold to mark emphasis and italics to name elements of our indicators that we refer to in its inputs or documentation.

#### URLs
Two types of URLs can be included. General URLs look like:
```
The PineCoders account's [url=https://www.tradingview.com/u/PineCoders/#published-scripts]Scripts page[/url].
```
and yield:

[<img src="GeneralLink.png">](https://www.pinecoders.com/techniques/script_description/GeneralLink.png)

When you want to link to a TradingView publication such as a script or idea, or a chart snapshot created use:
```
Link to a script publication: [chart]https://www.tradingview.com/script/Wvcqygsx-MTF-Oscillator-Framework-PineCoders/[/chart]
```
to obtain:

[<img src="LinkToPublication.png">](https://www.pinecoders.com/techniques/script_description/LinkToPublication.png)

Note that this type of tag is not required; raw links to TV publications or snapshots will be interpreted the same way, so that:
```
Link to a script publication: https://www.tradingview.com/script/Wvcqygsx-MTF-Oscillator-Framework-PineCoders/
```
will yield the same output.

#### Symbols
You can link to a symbol which readers may click on to bring up a generic chart:
```
Link to a symbol: `[symbol="NASDAQ:AAPL"]NASDAQ:AAPL[/symbol]`  
```
which will look like this:

[<img src="LinkToASymbol.png">](https://www.pinecoders.com/techniques/script_description/LinkToASymbol.png)

#### Pine Code Blocks
You can include Pine code in monospace blocks by using:
```
Pine code:[pine]//@version=4
study("")
plot(close)[/pine]
```
to yield:

[<img src="PineTags.png">](https://www.pinecoders.com/techniques/script_description/PineTags.png)

Notes:
- There is no inline equivalent for a monospace tag.
- Some character combinations in Pine code will be interpreted and garbled in the parser's output. Be sure to test the output of your code blocks in private descriptions before publishing them by copyying the published result and trying to compile it in the Pine Editor.

#### Bulleted Lists

Lists are tagged like this:
```
List:
[list]
[*]Item 1
[*]Item 2
[/list]
```
and look like this:

[<img src="Lists.png">](https://www.pinecoders.com/techniques/script_description/Lists.png)

We don't like the smaller point size used for list items and prefer to build our own lists, as we explain in our example description.


### Special Characters

We use a few different [Unicode space characters](http://jkorpela.fi/chars/spaces.html) to indent and align our text:
- Em space, U+2003 ( )
- En Space, U+2002 ( )
- Thin space, U+2009 ( ) 

and:
- Full block, U+2588 (█)
- Bullet, U+2022 (•)
- Em dash, U+2014 (—)


<br><br>
## A Description, Step by Step
We will now build an example description step by step. We begin with our "Overview" section:
```
█ [b]OVERVIEW[/b]

We begin our descriptions with an "Overview" section, keeping in mind that these first sentences will appear in the [i]widget[/i] of the published script. The [i]widget[/i] is the small thumbnail representing your script in the Scripts stream or in your user profile's "Scripts" tab. When users click on your script's [i]widget[/i], they open your script's [i]page[/i].


```
The above text will look like this in your script's page:

[<img src="Overview.png">](https://www.pinecoders.com/techniques/script_description/Overview.png)

and like this in your script's widget:

[<img src="ScriptWidget.png">](https://www.pinecoders.com/techniques/script_description/ScriptWidget.png)

Note:
- We prefix section titles with a full block and an Em space: (█ ).
- We use all caps for the title and the bold attribute.
- We follow section titles with an empty line.
- We end sections with two empty lines to provide visual separation between sections. This entails that we never use two empty lines within sections.









This is an example of a marked up description which you can use as is in an actual TradingView script publication. Copy/paste it in a private script publication's description to play around with it.


<br><br>
## Tips

### Multilingual Descriptions
When writing multilingual descriptions, House rules require that you begin with English. To indicate to readers of another locale that another language is available, it is good practice to mention this in the very first line of your description. If a French description was available after the English, you could use:

```
[Une description en français suit l'anglais.]
```
which says "A French description follows the English one."

### Tags in Comments
Note that the only tags interpreted in comments posted on TradingView publications are links to TV publications and chart snapshots, and Pine code block tags. As in descriptions, links to TV publications and snapshots do not require using `[chart]...[/chart]` tags; you can simply paste the link in the comment, which will render as an image.

### AutoHotkey Macros
We use these AutoHotkey macros to help us with tags:

```
; ————— TV markup tags.
!b::SendInput [b]               ; bold open (ALT-B).
!+b::SendInput [/b]             ; bold close (SHIFT-ALT-B).
!i::SendInput [i]               ; itals open (ALT-I).
!+i::SendInput [/i]             ; itals close (SHIFT-ALT-I).
!l::SendInput [list]            ; list open (ALT-L).
!+l::SendInput [/list]          ; list close (SHIFT-ALT-L).
^!+l::SendInput [*]             ; list item (CTRL-SHIFT-ALT-L).
^#!Right::SendInput [pine]      ; Pine open tag (CTRL-WIN-ALT-RightArrow).
^#!Left::SendInput [/pine]      ; Pine close tag (CTRL-WIN-ALT-LeftArrow).
```
