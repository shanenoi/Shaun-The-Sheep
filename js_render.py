from datetime	import datetime as dt
from html 		import unescape
from re 		import findall
from save_to_db import DATA_BASE

import random
import sqlite3

TEMPLATE = "template.js"
TABLES = [
	['Series_1_2007', 'Series 1 (2007)', '2007'],
	['Series_2_2009–2010', 'Series 2 (2009–2010)', '2009–2010'],
	['Series_3_2012–2013', 'Series 3 (2012–2013)', '2012–2013'],
	['Series_4_2014', 'Series 4 (2014)', '2014'],
	['Series_5_2016', 'Series 5 (2016)', '2016'],
	['Shaun_The_Sheep_Championsheeps_2012', 'Shaun The Sheep Championsheeps 2012', '2012'],
	['Shaun_the_Sheep_3D_2012', 'Shaun the Sheep 3D 2012', '2012']
]
CHARTCOLORS = [
	'rgb(255, 99, 132)',
	'rgb(255, 159, 64)',
	'rgb(255, 205, 86)',
	'rgb(75, 192, 192)',
	'rgb(54, 162, 235)',
	'rgb(153, 102, 255)',
	'rgb(201, 203, 207)'
]
TYPE_DATA = {
	"type": 'line',
	"tableName": "",
	"labels": [],
	"data": [],
	"title": [],
	"director": [],
	"writter": [],
	"storyBoard": [],
	"airdate": [],
	"Xlabel": "",
	"Ylabel": "",
	"color": ""
}


def split_time(ss):
	for ele in ss:
		ele = list(ele)
		try:
			ele[5] = findall('(.+)\([^()]+\)', ele[5])[0].replace('\xa0', " ")
		except IndexError:
			pass
		ele[6] = ele[6].strip()
		yield ele


def prepair_data():
	with sqlite3.connect(DATA_BASE) as sql:
		cursor = sql.cursor()

		for table in TABLES:
			cursor.execute(
				f"""SELECT * FROM `{table[0]}` GROUP BY title ORDER BY episodes;"""
			)
			ss = cursor.fetchall()
			yield list(split_time(ss))


def html_writter(data):
	tl_html = open(TEMPLATE).read()
	with open("js.js", "w") as f:
		f.write(tl_html.replace("[@1@]", str(data)))


def main():
	temp = TYPE_DATA
	o_data = list(prepair_data())
	data = []
	for i in range(len(o_data)):
		temp = TYPE_DATA
		temp["tableName"] = TABLES[i][1]
		temp["labels"] = [ele[0] for ele in o_data[i]]
		temp["data"] = [ele[-1] for ele in o_data[i]]
		temp["title"] = [ele[1] for ele in o_data[i]]
		temp["director"] = [ele[2] for ele in o_data[i]]
		temp["writter"] = [ele[3] for ele in o_data[i]]
		temp["storyBoard"] = [ele[4] for ele in o_data[i]]
		temp["airdate"] = [ele[5] for ele in o_data[i]]
		temp["Xlabel"] = "Episodes"
		temp["Ylabel"] = "Followers"
		temp["color"] = random.choice(CHARTCOLORS)
		data.append(str(temp))

	temp = TYPE_DATA
	temp["type"] = "bar"
	temp["tableName"] = "Compare Series"
	temp["labels"] = [table[1] for table in TABLES]
	temp["data"] = [sum([i[-1] for i in series]) for series in o_data]
	temp["title"] = temp['labels']
	temp["airdate"] = [table[-1] for table in TABLES]
	temp["Xlabel"] = "Series"
	temp["Ylabel"] = "Followers"
	temp["color"] = random.choice(CHARTCOLORS)
	data.append(str(temp))

	html_writter(data)


if __name__ == '__main__':
	main()