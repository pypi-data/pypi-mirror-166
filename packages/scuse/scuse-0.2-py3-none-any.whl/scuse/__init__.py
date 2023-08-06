
import requests
from bs4 import *

class scuse:

	def wordf(self,wordfc):

		sel = "https://www.google.com/search?q="+wordfc
		get = requests.get(sel)

		code = BeautifulSoup(get.content, 'html.parser')
		scw  = code.h3.text

		return scw


