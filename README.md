# Project Ajax: An A.I general assistant
---

## Installation instructions
1. Install Python 3.6 from the [official Python downloads website](https://www.python.org/downloads/) on your machine
2. Install `pipenv` by running `pip install pipenv`
3. Open up command line in the directory on this project.
4. Run `pipenv install`

### Running it
5. `python ajax.py <config-file-name>`

## Some of the voice commands
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


## Misc
### Resources:
- [Speech Recognition Recognizer documentation](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst)
- [PyAudio whl file repository for WINDOWS](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- [Python caching tool](https://towardsdatascience.com/how-to-speed-up-your-python-code-with-caching-c1ea979d0276)
- [Rasa Python API](http://35.196.60.7/docs/nlu/0.14.5/python/)
- [How to fix - Python 3.6 contains broken python 2 concurrent futures packages](https://stackoverflow.com/questions/54338270/syntax-error-after-installing-futures-package-in-my-virtualenv)
	- Downgrade setuptools to 45.2.0
- [How to build an event system implementing Observer pattern](https://dev.to/kuba_szw/build-your-own-event-system-in-python-5hk6)
- [How to read an uncompressed epub file](https://stackoverflow.com/questions/1388467/reading-epub-format)
- 4 principles of config mgmt
	- Static
	- Use literals not string keys
	- Define them close to where they are used
	- Early validation
- [Indepth python logging tutorial](https://coderzcolumn.com/tutorials/python/logging-simple-guide-to-log-events-in-python)
- [Arduino WIFI ESP8266](https://www.youtube.com/watch?v=Q6NBnPfPhWE)

### Improvements
---
#### Primary
I have enough information to implement these fixes:


#### Secondary
Still need do research to implement them
- [ ] Make sound features more OS independent(file system, config and playsound function)
	- Sound libraries are OS dependent
	- Current sound features are injected into receivers using mixin interfaces. **Each** sound mixin depends on a `SoundEngine` which is solely responsible for playing sound. Sound mixins are solely responsible for using the `SoundEngine`.
	- Can implement sound features for both windows and OS by modifying the `SoundEngine` class to adapt to the current OS.
	- Need a library that can play sound asynchronously for linux.
	- Modify or extend the SoundEngine class into different versions for different OSes.
- [ ] Adjust for ambient noise only when needed. Incorporate with user analytics. Only when needed := Fail to twice in a row := Kena default command twice in a row


#### IOT phase
- Test code on Linux system. See if feasible and make it OS independent


### Shelved
---
#### Improvements

- [ ] If computer is playing audio && wake word is heard, lower computer volume temporarily
	- will make it more windows OS oriented tho
- [ ] Sort the music into genres


#### Add-ons
##### Voice assistant
- Maybe incorporate [exrex](https://github.com/asciimoo/exrex) - A reverse Regex generator

- User analytics
	- To adjust the timeout, phrase timeout, etc


### Notes
- Pocketsphinx is not supported beyond python 3.6. The python version was downgraded to support pocketsphinx so as to enable offline transcription.
- [rasa init fails with import error "composition view" remedy](https://stackoverflow.com/questions/70506164/importerror-cannot-import-name-compositionview-from-sanic-views-when-i-trie)
- Should not move the project if it has an existing virtualenv living in the system. Otherwise need to reset the virtualenv by deleting and re-creating it from the Pipfile
- Pyaudio requires a different dependency on raspberry pi, which in turn depends on portaudio. [Install portaudio 1st.](https://raspberrypi.stackexchange.com/questions/75031/cannot-install-pyaudio)

	
	