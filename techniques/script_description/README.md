//@version=5
indicator("Smoothed VWAP Range", overlay=true)

// 输入参数
length = input.int(200, title="Length")
bandMultiplier = input.float(2.0, title="Band Multiplier")
showBands = input.bool(true, title="Show Bands")
showClose = input.bool(true, title="Show Close Line")
showHLArea = input.bool(true, title="Show High-Low Area")

// 计算成交量和VWAP
vol = volume
volSma = ta.sma(vol, length)

srcVolSmaClose = ta.sma(close * vol, length)
srcVolSmaHigh = ta.sma(high * vol, length)
srcVolSmaLow = ta.sma(low * vol, length)

vwapHighClose = srcVolSmaClose / volSma
vwapHighHigh = srcVolSmaHigh / volSma
vwapHighLow = srcVolSmaLow / volSma

// 控制显示高低区域 (云图)
hline = showHLArea ? vwapHighHigh : na
lline = showHLArea ? vwapHighLow : na

plot(hline, color=color.new(color.blue, 0), title="VWAP High", linewidth=1)
plot(lline, color=color.new(color.blue, 0), title="VWAP Low", linewidth=1)

fill(hline, lline, color=color.new(color.blue, 90), title="HL Area")

// 控制显示收盘线
plot(showClose ? vwapHighClose : na, color=color.white, title="VWAP Close Line", linewidth=2)

// 计算并显示VWAP标准差带
if (showBands) 
    srcSrcVolSmaClose = ta.sma(vol * math.pow(close, 2), length)
    srcSrcVolSmaHigh = ta.sma(vol * math.pow(high, 2), length)
    srcSrcVolSmaLow = ta.sma(vol * math.pow(low, 2), length)

    stDevHighClose = math.sqrt(srcSrcVolSmaClose / volSma - math.pow(vwapHighClose, 2))
    stDevHighHigh = math.sqrt(srcSrcVolSmaHigh / volSma - math.pow(vwapHighHigh, 2))
    stDevHighLow = math.sqrt(srcSrcVolSmaLow / volSma - math.pow(vwapHighLow, 2))

    upperBandClose = vwapHighClose + stDevHighClose * bandMultiplier
    lowerBandClose = vwapHighClose - stDevHighClose * bandMultiplier

    upperBandHigh = vwapHighHigh + stDevHighHigh * bandMultiplier
    lowerBandHigh = vwapHighHigh - stDevHighHigh * bandMultiplier

    upperBandLow = vwapHighLow + stDevHighLow * bandMultiplier
    lowerBandLow = vwapHighLow - stDevHighLow * bandMultiplier

    plot(upperBandClose, color=color.new(color.red, 0), title="Upper Band (Close)", linewidth=1)
    plot(lowerBandClose, color=color.new(color.red, 0), title="Lower Band (Close)", linewidth=1)

    plot(upperBandHigh, color=color.new(color.green, 0), title="Upper Band (High)", linewidth=1)
    plot(lowerBandHigh, color=color.new(color.green, 0), title="Lower Band (High)", linewidth=1)

    plot(upperBandLow, color=color.new(color.yellow, 0), title="Upper Band (Low)", linewidth=1)
    plot(lowerBandLow, color=color.new(color.yellow, 0), title="Lower Band (Low)", linewidth=1)
