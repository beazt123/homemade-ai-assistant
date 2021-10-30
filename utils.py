import webbrowser as web
import requests


def playOnYoutube(topic: str):
	"""Play a YouTube Video"""


	url = "https://www.youtube.com/results?q=" + topic
	count = 0
	cont = requests.get(url)
	data = cont.content
	data = str(data)
	lst = data.split('"')
	for i in lst:
		count += 1
		if i == "WEB_PAGE_TYPE_WATCH":
			break
		if lst[count - 5] == "/results":
			raise Exception("No Video Found for this Topic!")

	web.open("https://www.youtube.com" + lst[count - 5])
	
	
def googleSearchFor(topic: str) -> None:
	"""Searches About the Topic on Google"""

	link = "https://www.google.com/search?q={}".format(topic)
	web.open(link)