import logging
import textwrap
import wikipedia
from requests.exceptions import ConnectionError
from ..utils.utils import playOnYoutube, googleSearchFor
from .mixins.speechMixin import SpeechMixin
from .mixins.asyncStdVoiceResponseMixin import AsyncStdVoiceResponseMixin


class Searcher(SpeechMixin, AsyncStdVoiceResponseMixin):
	logger = logging.getLogger(__name__)
	def __init__(self, 
				config, 
				speechEngine = None,
				soundEngine = None):
		SpeechMixin.__init__(self, speechEngine)
		AsyncStdVoiceResponseMixin.__init__(self, config, soundEngine)

	def google(self, searchStatement):
		self.acknowledge()
		googleSearchFor(searchStatement)
		Searcher.logger.info(f"Google searching for {searchStatement}")
		

	def youtube(self, searchStatement):
		self.acknowledge()
		playOnYoutube(searchStatement)
		Searcher.logger.info(f"Youtube searching for {searchStatement}")

	def wiki(self, searchStatement):
		self.acknowledge()
		Searcher.logger.info(f"Wiki searching for {searchStatement}")
		
		try:
			info = wikipedia.summary(searchStatement, 2)
			Searcher.logger.info(f"Wiki search results: {info}")
			paragraphed = textwrap.fill(info.strip(), width=80)
			print(textwrap.indent(paragraphed, prefix="\t"))
			self.say(info)

		except wikipedia.DisambiguationError:
			Searcher.logger.exception("Wikipedia DisambiguationError: >1 possible searches")
			self.say("Sorry, there were quite many possible searches. \
				Please be more specific in your search terms")
				
		except wikipedia.exceptions.PageError:
			Searcher.logger.exception(f"{searchStatement} not found on wikipedia")
			self.say(f"Sorry, there are no matching searches for {searchStatement}")

		except ConnectionError:
			Searcher.logger.exception(f"Unable to connect to wikipedia")
			self.apologise(True)
			self.tryLater()

        
