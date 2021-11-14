import logging
import textwrap
import wikipedia

from ..utils.utils import playOnYoutube, googleSearchFor
from .speechMixin import SpeechMixin


class Searcher(SpeechMixin):
	def __init__(self, config, speechEngine):
		SpeechMixin.__init__(self, config, speechEngine)

	def google(self, searchStatement):
		googleSearchFor(searchStatement)

	def youtube(self, searchStatement):
		playOnYoutube(searchStatement)

	def wiki(self, searchStatement):
		try:
			info = wikipedia.summary(searchStatement, 2)

			self.say(info)

			paragraphed = textwrap.fill(info.strip(), width=80)
			print(textwrap.indent(paragraphed, prefix="\t"))

		except wikipedia.DisambiguationError:
			logging.error("Wikipedia DisambiguationError: >1 possible searches")
			self.say("Sorry, there were quite many possible searches. \
				Mind if you be more specific in your search terms? Thanks!")
				
		except wikipedia.exceptions.PageError:
			logging.error("Not found")
			self.say(f"Sorry, there are no matching searches for {searchStatement}")

        
