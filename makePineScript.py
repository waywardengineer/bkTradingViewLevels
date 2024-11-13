scriptTemplate = '''//
// Test
// @version=5
//
indicator("BKlevels", overlay = true, max_bars_back = 1000, max_labels_count = 500, max_lines_count = 500)

dayLineLength = 1000 * 60 * 60 * 23
labelOffset = 1000 * 60 * 60 * 10 

{declarations}
{tickers}
'''

tickerTemplate = '''
if (syminfo.ticker == "{ticker}")
	{levels}'''

levelTemplate = '''
	var label {labelReference} = na
	line.new(x1 = {dateReference}, y1 = {level}, x2 = {dateReference} + dayLineLength, y2 = {level}, color = {color}, width = 1, style = line.style_solid, xloc = xloc.bar_time)
	{labelReference} := label.new({dateReference} + labelOffset, {level}, "{levelName}", style=label.style_label_center, color=color.black, textcolor=color.white, xloc = xloc.bar_time)'''
	
dateTemplate = '''
{dateReference} = timestamp("{y}-{m}-{d}")'''

#take a line as read from the input file, parse it and return data. 
#example of returned data structure: ("SPY", {"595" : "1st Put Vol", "600" : "HvolC, Upper PDVR"})
def processLine(line): 
	segments = line.split(" : ")
	ticker = segments[0]
	levelTxts = segments[1].split(";")
	levels = {}
	for levelTxt in levelTxts:
		parts = levelTxt.split(",")
		level = str(parts[0])
		label = parts[1].strip()
		if level not in levels:
			levels[level] = label
		else:
			newTxt = levels[level] + ", " + label
			levels[level] = newTxt
	if ticker == 'ES':
		ticker = 'ES1!'
	return ticker, levels

dates = []
declarationsPs = []
tickers = {}
tickersPs = []
dateRefs = []
labelIndex = 0


f = open("bkLevels.txt", "r")
for line in f:
	if len(line) > 1:
		if line[-2] == '~':
			dates.append(line[:-2].split('-'))
		else:
			ticker, levels = processLine(line)
			if ticker not in tickers:
				tickers[ticker] = []
			tickers[ticker].append(levels)
f.close()

for index, date in enumerate(dates):
	dateRef = "D" + str(index)
	declarationsPs.append(dateTemplate.format(dateReference = dateRef, y = date[0], m = date[1], d = date[2]))
	dateRefs.append(dateRef)
	

for ticker, datesLevels in tickers.items():
	levelsPs = []
	for dateIndex, levels in enumerate(datesLevels):
		for level, label in levels.items():
			levelsPs.append(levelTemplate.format(
				labelReference = "label" + str(labelIndex),
				dateReference = dateRefs[dateIndex],
				level = level,
				levelName = label,
				color = "#ffccff"
			))
			labelIndex += 1
	tickersPs.append(tickerTemplate.format(
		ticker = ticker,
		levels = "\n".join(levelsPs)
	))			
psout = scriptTemplate.format(
	declarations = "\n".join(declarationsPs),
	tickers = "\n".join(tickersPs),
)

f = open("levels.pine", "w")
f.write(psout)
f.close()