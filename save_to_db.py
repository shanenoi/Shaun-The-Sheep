from re import findall
from series_sts import ShaunTheSheep
from youtube_crawl_episode import CountViewsSTS

import sqlite3

DATA_BASE = "sts.db"
DATA_BASE_ARCHITECTURE = """
	episodes INT,
	title VARCHAR(255),
	director VARCHAR(746),
	writter VARCHAR(746),
	storyboard VARCHAR(746),
	airdate VARCHAR(255),
	summary TEXT,
	followers INT
"""


def check_table(cursor, table_name):
	try:
		cursor.execute(
			f'CREATE TABLE {table_name} ({DATA_BASE_ARCHITECTURE})'
		)
	except sqlite3.OperationalError:
		print(f'[+] {table_name} table was created!')


def ss1_process(single, counter):
	episodes = single.find('th', {'scope': 'row'})
	title = findall(
		'"([^"]+)"',
		single.find('td', {'class': 'summary'}).get_text()
	)[0]
	director, writter, storyboard, original_airdate = single.find_all('td', {'style': 'text-align:center'})[1:]
	counter.entry_name(title)
	summary = single.find_next_sibling('tr', {'class': 'expand-child'}).get_text()
	followers = counter.views

	if followers == 0:
		print(f'[X] {title} has {followers} views????')
		if input("[!] Do you want to try again? (y|n) ") == 'y':
			ss1_process(single, counter)
		else:
			print("[.] I don't think nobody follow this episode!")

	return (
		int(episodes.get_text()),
		title,
		director.get_text(),
		writter.get_text(),
		storyboard.get_text(),
		original_airdate.get_text(),
		summary,
		followers
	)


def remaining_ss_process(single, counter):
	episodes = single.find('th', {'scope': 'row'})
	title = findall(
		'"([^"]+)"',
		single.find('td', {'class': 'summary'}).get_text()
	)[0]
	original_airdate = single.find_all('td', {'style': 'text-align:center'})[-1]
	counter.entry_name(title)
	summary = single.find_next_sibling('tr', {'class': 'expand-child'}).get_text()
	followers = counter.views

	if followers == 0:
		print(f'[X] {title} has {followers} views????')
		if input("[!] Do you want to try again? (y|n) ") == 'y':
			remaining_ss_process(single, counter)
		else:
			print("[.] I don't think nobody follow this episode!")

	return (
		int(episodes.get_text()),
		title,
		"",
		"",
		"",
		original_airdate.get_text(),
		summary,
		followers
	)


def contact_db_with(table_ss, process, sql, cursor, counter):
	table_name = '_'.join(findall(
		'([^() ]+)',
		table_ss[0].get_text().replace('[edit]', '')
	))
	check_table(cursor, table_name)
	values = [process(i, counter) for i in table_ss[1].find_all('tr', {'class': 'vevent'})]
	for value in values:
		cursor.execute(
			f"INSERT INTO {table_name} " +
			"VALUES (?,?,?,?,?,?,?,?)",
			value
		)
	print(f'[+] {table_name} Done!')
	sql.commit()


def main():
	sts = ShaunTheSheep()
	list_table = sts.parse()
	counter = CountViewsSTS()

	with sqlite3.connect(DATA_BASE) as sql:
		cursor = sql.cursor()
		list_table = list(list_table)

		print('[*] Series 1 ...')
		contact_db_with(list_table[0], ss1_process, sql, cursor, counter)

		print('[*] Series 2 ...')
		contact_db_with(list_table[1], remaining_ss_process, sql, cursor, counter)
		
		print('[*] Series 3 ...')
		contact_db_with(list_table[2], remaining_ss_process, sql, cursor, counter)
		
		print('[*] Series 4 ...')
		contact_db_with(list_table[3], remaining_ss_process, sql, cursor, counter)
		
		print('[*] Series 5 ...')
		contact_db_with(list_table[4], remaining_ss_process, sql, cursor, counter)
		
		print('[*] Shaun the Sheep 3D ...')
		contact_db_with(list_table[5], remaining_ss_process, sql, cursor, counter)
		
		print('[*] Shaun The Sheep Championsheeps')
		contact_db_with(list_table[6], remaining_ss_process, sql, cursor, counter)


if __name__ == '__main__':
	main()
