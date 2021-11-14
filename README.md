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

### "*Define [Word]*"
Reads you a dictionary definition of the word. Works offline and online.

### "*Play [some] music*"
Words in the square brackets are optional. It will search for music on your computer and shuffle play.

### "*Tell [me the] time*"
Self explanatory

### "*news*"
Reads you 5 articles from Straits times. Prints them on the command prompt.

### "*weather*"
Reads you the weather conditions for the next 12 hrs in 3 hr increments.

### "*Tell [me a] joke*"
Tells you a programming related joke. Only programming nerds can understand.

### "*Shutdown computer/system*"
Self explanatory. Make sure you've ready saved your work.

### "*[Can I talk to] a male/female assistant?*"
Words in the square brackets are optional. On the contrary, words not in the square brackets are compulsory. The default is female.


## Misc
### Resources:
- [Speech Recognition Recognizer documentation](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst)
- [PyAudio whl file repository](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- [Python caching tool](https://towardsdatascience.com/how-to-speed-up-your-python-code-with-caching-c1ea979d0276)
- [Rasa Python API](http://35.196.60.7/docs/nlu/0.14.5/python/)
- [How to fix - Python 3.6 contains broken python 2 concurrent futures packages](https://stackoverflow.com/questions/54338270/syntax-error-after-installing-futures-package-in-my-virtualenv)
	- Downgrade setuptools to 45.2.0
- [How to build an event system implementing Observer pattern](https://dev.to/kuba_szw/build-your-own-event-system-in-python-5hk6)

### Improvements
#### Current phase
- Write an articlePrinter class using Builder design pattern
- Singleton for config
- Replace config with dependency injected config: A config object in top level object. Passed into every object it is composed of.
	- Each object implements FilterConfig interface where it chooses only appropriate config. No longer hard coded object methods.
	- Pass config object to receivers in the main methods
	- [*] Use config to choose what receivers to instantiate
- Implement Command interface
- Have a voice Receiver object which is called by other Receivers

#### IOT phase
- Test code on Linux system. See if feasible and make it OS independent
- Implement Publisher interface with only /local topic enabled
- Create MQTT related class which implements Publisher.

### Shelved
#### Improvements
- make it more OS independent(file system and playsound function)
- If computer is playing audio && wake word is heard, lower computer volume temporarily(will make it more windows OS oriented)
- Store preferences, settings and system settings
	- Preferences
		- News articles
		- Spotify credentials
		- wait time and phrase time limit
		- AI talking speed
- Use NLP cosine similarity calculations to link command to underlying action
- Adjust for ambient noise only when needed
- Sort the music into genres
- Get the engine to refresh the new userPreferences unto the current settings. User preference not updating.


#### Add-ons
##### Voice assistant
- Maybe incorporate [exrex](https://github.com/asciimoo/exrex) - A reverse Regex generator

- Introduce states using smach
- Pafy library for youtube
- User analytics
	- To adjust the timeout, phrase timeout, etc

##### CMD tool
- Add file search function to CMD general tool assistant


### Notes
- Pocketsphinx is not supported beyond python 3.6. The python version was downgraded to support pocketsphinx so as to enable offline transcription.
- Spotify API: use input() if not credentials not found in cache/config
	- Shelved: Auth needed and only premium users get to stream content
	
	
#### Config mgmt
- 4 principles of config mgmt
	- Static
	- Use literals not string keys
	- Define them close to where they are used
	- Early validation