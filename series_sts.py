import bs4
import re
import requests


class ShaunTheSheep:

	def __init__(self):
		self.source_data = "https://en.wikipedia.org/wiki/List_of_Shaun_the_Sheep_episodes"


	def __get_html_code(self):
		return requests.get(self.source_data).text


	def parse(self):
		soup = bs4.BeautifulSoup(
			self.__get_html_code(),
			'html.parser'
		)
		for ele in soup.find_all('table', {'class': 'wikitable plainrowheaders'}):
			yield [ele.find_previous_sibling('h3'), ele]
