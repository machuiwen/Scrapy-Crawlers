import scrapy
import os

RESULT_PATH=os.path.join(os.getcwd(), 'results')
if not os.path.isdir(RESULT_PATH):
	os.makedirs(RESULT_PATH)
os.chdir(RESULT_PATH)

class DigimonModelSpider(scrapy.Spider):
	"""
	This spider is used to crawl 3D models from www.models-resource.com
	"""
	name = "digimon_model"

	hostname = 'https://www.models-resource.com'
	start_urls = [
		'https://www.models-resource.com/pc_computer/digimonmasters/',
		'https://www.models-resource.com/psp/digimonadventure/',
		'https://www.models-resource.com/custom_edited/digimoncustoms/',
		'https://www.models-resource.com/mobile/digimonlinkz/'
	]

	def parse(self, response):
		model_links = response.css('div.updatesheeticons a::attr(href)').extract()
		model_links = [self.hostname + l for l in model_links]
		for model_page in model_links:
			yield scrapy.Request(model_page, callback=self.parse_model_page)

	def parse_model_page(self, response):
		game_name = response.url.split('/')[-4]
		model_name = response.css('tr.rowheader div::text').extract_first()
		download_link = response.css('tr.rowfooter a::attr(href)').extract_first()
		download_link = self.hostname + download_link
		os.system("wget '%s' -O '%s-%s.zip'" % (download_link, game_name, model_name))
