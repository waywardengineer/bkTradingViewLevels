This script reads levels from "bklevels.txt" and creates a Pinescript for TradingView. The levels are drawn for one day in the chart. The date for a given group  of levels is read from the line above it. 
Format is:

{Year}-{month}-{day1}~

{ticker1} : {price1},{label1};{price2},{label2},...

{ticker2} : {price1},{label1};{price2},{label2},...

{Year}-{month}-{day2}~

{ticker1} : {price1},{label1};{price2},{label2},...

{ticker2} : {price1},{label1};{price2},{label2},...

See "bklevels.txt" in this repo for an example

Requirements: Python3.x

Usage: Update "bklevels.txt" up in the same folder as the Python script. Run the "makePineScript.py", and it should create or update "levels.pine" in the same folder. Install "levels.pine" into Tradingview

Issues/improvements:
- Will add multiple coloring
- Will make remapping of tickers (like "ES" to "ES1!" more generalized and less kludgy
- Right now, if a ticker is in the group for one date and not in the group for another date, things are gonna get weird. Make sure all dates have the same set of tickers for now(order doesn't matter)
