import bs4
import re
import requests


class CountViewsSTS:

	def __init__(self):
		self.name = []
		self.html_code = ""
		self.clips = []


	def entry_name(self, name):
		self.name = re.findall("([\w\']+)", name)
		for w in ['shaun', 'the', 'sheep']:
			if w.lower() in self.name:
				self.name.pop(self.name.index(w.lower()))


	def get_html_code(self):
		query = (
			'https://www.youtube.com/results?search_query=' +
			'+'.join(self.name + ['shaun', 'the', 'sheep'])
		)
		print('[+] Request query:', query)
		self.html_code = requests.get(query).text


	def get_list_detail_clips(self):
		self.get_html_code()
		soup = bs4.BeautifulSoup(self.html_code, 'html.parser')
		list_yt_content = soup.find_all('div', {'class': 'yt-lockup-content'})
		
		def pre_process(single_tag):
			try:
				return [
					single_tag.find('a').get_text(),
					re.findall('([\d\.]+)', single_tag.find_all('li')[-1].get_text())[0]
				]
			except IndexError:
				return None

		self.clips = list(map(pre_process, list_yt_content))




	def update_correct_episode(self):
		self.get_list_detail_clips()

		correct_list = [
			len([
				1 for name in self.name if name.lower() in single[0].lower()
			]) / len(self.name) > 0.5
			if single else False
			for single in self.clips
		]

		self.clips = [
			self.clips[i]
			for i in range(len(self.clips))
			if correct_list[i]
		]


	@property 
	def views(self):
		self.update_correct_episode()
		
		return sum([
			int(ele[1].replace('.', '')) for ele in self.clips
		])
