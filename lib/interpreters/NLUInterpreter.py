import os
import logging
from lib.interpreters.interpreter import Interpreter
from lib.interpreters.RasaInterpreter import RasaInterpreter
from lib.commands import DefaultCommand
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import tflearn
import tensorflow
import yaml
import pickle


class NLUInterpreter(Interpreter):
	logger = logging.getLogger(__name__)
	model = None
	words = None

	def __init__(self, config, soundEngine, mic):
		Interpreter.__init__(self, config, soundEngine, mic)
		NLUInterpreter.prepareModel()

	@classmethod
	def prepareModel(cls):
		try:
			with open(os.path.join("lib", "interpreters", "data.pickle"), "rb") as f:
				words, labels, training, output = pickle.load(f)
		except ValueError:
			raise RuntimeError("data.pickle not found")

		tensorflow.compat.v1.reset_default_graph()

		net = tflearn.input_data(shape=[None, len(training[0])])
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
		net = tflearn.regression(net)

		model = tflearn.DNN(net)

		try:
			model.load(os.path.join("lib", "interpreters", "model.tflearn"))
		except ValueError:
			raise RuntimeError("Model not found")

		NLUInterpreter.model = model
		NLUInterpreter.words = words
		NLUInterpreter.labels = labels


	@staticmethod
	def bag_of_words(s, words):
		bag = [0 for _ in range(len(words))]

		s_words = nltk.word_tokenize(s)
		s_words = [stemmer.stem(word.lower()) for word in s_words]

		for se in s_words:
			for i, w in enumerate(words):
				if w == se:
					bag[i] = 1
				
		return np.array(bag)

	@classmethod
	def process(cls, command):
		if command == Interpreter.FAILED_TOKEN:
			cls.logger.warn("Failed to interpret command. Reverting to default command")
			return DefaultCommand.__name__, None
		results = NLUInterpreter.model.predict([NLUInterpreter.bag_of_words(command, NLUInterpreter.words)])
		results_index = np.argmax(results)
		intent = NLUInterpreter.labels[results_index]

		if RasaInterpreter.isIOTcmd(intent):
			return RasaInterpreter.processIOTcmd(intent)
		else:
			event = RasaInterpreter.mapIntentToEvent(intent)
			data = None

			cls.logger.info(f"Event, data: {event}, {data}")
			return event, data



if __name__ == "__main__":
	with open(r"D:\Desktop\External Commitments\Projects\Google Home\rasa-nlu\data\nlu.yml", 'r') as stream:
		data = yaml.safe_load(stream)   

	try:
		with open("data.pickle", "rb") as f:
			words, labels, training, output = pickle.load(f)
	except:
		words = []
		labels = []
		docs_x = []
		docs_y = []

		for intent in data["nlu"]:
			if intent['intent'] == "define_word" or  intent['intent'] == "wiki_search" or  intent['intent'] == "google_search" or  intent['intent'] == "youtube_search": 
				continue
			for pattern in intent["examples"]:
				wrds = nltk.word_tokenize(pattern.strip("- ").strip("\n"))
				words.extend(wrds)
				docs_x.append(wrds)
				docs_y.append(intent["intent"])

			if intent["intent"] not in labels:
				labels.append(intent["intent"])

		words = [stemmer.stem(w.lower()) for w in words if w != "?"]
		words = sorted(list(set(words)))

		labels = sorted(labels)

		training = []
		output = []

		out_empty = [0 for _ in range(len(labels))]

		for x, doc in enumerate(docs_x):
			bag = []

			wrds = [stemmer.stem(w.lower()) for w in doc]

			for w in words:
				if w in wrds:
					bag.append(1)
				else:
					bag.append(0)

			output_row = out_empty[:]
			output_row[labels.index(docs_y[x])] = 1

			training.append(bag)
			output.append(output_row)


		training = numpy.array(training)
		output = numpy.array(output)

		with open("data.pickle", "wb") as f:
			pickle.dump((words, labels, training, output), f)
			
	tensorflow.compat.v1.reset_default_graph()

	net = tflearn.input_data(shape=[None, len(training[0])])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
	net = tflearn.regression(net)

	model = tflearn.DNN(net)

	try:
		model.load("model.tflearn")
	except ValueError:
		model = tflearn.DNN(net)
		model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
		model.save("model.tflearn")


	def bag_of_words(s, words):
		bag = [0 for _ in range(len(words))]

		s_words = nltk.word_tokenize(s)
		s_words = [stemmer.stem(word.lower()) for word in s_words]

		for se in s_words:
			for i, w in enumerate(words):
				if w == se:
					bag[i] = 1
				
		return numpy.array(bag)


	def chat():
		print("Start talking with the bot (type quit to stop)!")
		while True:
			inp = input("You: ")
			if inp.lower() == "quit":
				break

			results = model.predict([bag_of_words(inp, words)])
			results_index = numpy.argmax(results)
			tag = labels[results_index]
			print(tag)

			for tg in data["nlu"]:
				if tg['intent'] == tag:
					print(tg['intent'])

			# print(random.choice(responses))

	chat()