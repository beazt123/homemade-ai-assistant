# Project Ajax: An A.I general assistant
---

## Installation instructions
1. Install Python 3.6 from the [official Python downloads website](https://www.python.org/downloads/) on your machine
2. Install `pipenv` by running `pip install pipenv`
3. Open up command line in the directory on this project.
4. Run `pipenv install`

### Running it
5. `python ajax.py`

## Waking up the assistant
To get the A.I assistant to listen to you, you must wake it up from its dormant state. 

You can say one of the mainstream activation words I.e. *"Ok Google", "Alexa", "Hey Siri"* or even your favourite *"Jarvis"*! (I'm sorry. "Friday" doesn't work here) Alternatively, choose any word you like from below:
- grapefruit
- terminator
- grasshopper
- hey google
- bumblebee
- pico clock
- americano
- computer
- picovoice
- blueberry
- porcupine

## Voice commands
### "*\<google/youtube/wiki\> \<item\>*"
Opens up a web browser and searches for \<item\> in the respective platform. For wiki, will print a summary in the command prompt and read it out.

### "*play [some] music*"
Words in the square brackets are optional. It will search for music on your computer and shuffle play.

### "*time [me the] time*"
Self explanatory

### "*news*"
Reads you 5 articles from Straits times. Prints them on the command prompt.

### "*time [me a] joke*"
Tells you a programming related joke. Only programming nerds can understand.

### "*shutdown computer/system*"
Self explanatory. Make sure you've ready saved your work.

### "*[Can I talk to] a male/female assistant?*"
Words in the square brackets are optional. On the contrary, words not in the square brackets are compulsory. The default is female.


## Misc
### Resources:
- [Speech Recognition Recognizer documentation](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst)
- [PyAudio whl file repository](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)



### Improvements
- Create offline and online modes, use the offline transcriber
	- If offline, use cache for results. Create an interface
	- Enable offline transcription
- make it more OS independent(file system and playsound function)
- If computer is playing audio && wake word is heard, lower computer volume temporarily
- Store preferences, settings and system settings
	- Preferences
		- News articles
		- Spotify credentials
- Use NLP cosine similarity calculations to link command to underlying action

### Add-ons
#### Voice assistant
- Introduce caching of content downloaded from online. I.e. pyjokes. So that they can still run offline
- Maybe incorporate [exrex](https://github.com/asciimoo/exrex) - A reverse Regex generator
- Spotify API: use input() if not credentials not found in cache/config
- Introduce states using smach
- Dictionary function



#### CMD tool
- Add file search function to CMD general tool assistant


### Notes
- Pocketsphinx is not supported beyond python 3.6. The python version was downgraded to support pocketsphinx so as to enable offline transcription.

#### Config mgmt
- 4 principles of config mgmt
	- Static
	- Use literals not string keys
	- Define them close to where they are used
	- Early validation
	

## Workflows
- Google/Wiki/Youtube: <platform-name> <search statement>
- News: say "Give me the latest news"
- Offline Music: play some music
- Time/Quick Programming Joke/Change AI gender
- Terminate programme
- Shutdown computer


### Special(Custom) Interfaces
- What's/Who's <thing>: Performs Wiki search
- Play <video> on Youtube: Play 1st vidoe that comes up in youtube search results in a default web browser.
- 