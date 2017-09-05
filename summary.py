import os
import nltk
import shutil
import numpy as np

nDoc = 0 #temp 0



class doc(object):
	
	''' 
	
	docname - name of doc, summary file will have the same name
	wordFreq - word with it's freq in the doc
	wordWeight [0,1] - equals to  1 - (noOfDoc that has this word / total No of Doc)
	summary - summary of this doc
	weightThreshold - mean + (2 * std)
	
	'''


	def __init__ (self,docName):
		
		self.docName = docName
		self.wordFreq = dict() # contains word with their frequency
		self.wordWeight = dict() # contains word and it's weight, from [0,1]
		self.effectiveFreq = dict() 
		self.thresholdEffectiveFreq = 0
		self.summary = str()

		# calculate word frequency
		file = open(docName, "r")

		for line in file:
			line = line[0:-1] #remove newline char from the end
			
			wordsList = nltk.word_tokenize(line) #split words
			# count wordFrequency and update wordFreq dictionary
			for word in wordsList:
				if word.lower() not in self.wordFreq:
					self.wordFreq[word.lower()] = 1
				else:
					self.wordFreq[word.lower()] += 1

		file.close()



	# calculate weight threshold
	def calThresholdEffectiveFreq (self):

		for word,frequency in self.wordFreq.items():
			self.effectiveFreq[word] = frequency * self.wordWeight[word]

		# cal mean of weight of all the word in the doc
		effectiveFreqMean = np.mean( list(self.effectiveFreq.values()) )
		
		# cal std of weight of all the word in the doc
		effectiveFreqStd = np.std( list(self.effectiveFreq.values()) )
		
		# cal weightThreshold of weight of all the word in the doc
		self.thresholdEffectiveFreq = effectiveFreqMean + 2 * effectiveFreqStd





def calculate_word_weight(document_list,word):

	global nDoc
	word_occurrence = 0      #number of documents which contains this word

	for document in document_list:
		if word in document.wordFreq:
			word_occurrence = word_occurrence+1
	return (1 - (word_occurrence / nDoc))



#if summary folder exist then delete it
if os.path.exists("summary"):
	shutil.rmtree('summary')

# get list of all files in the folder
docNameList = os.listdir()
docNameList.remove(__file__) #remove python file name
nDoc = len(docNameList)


# creating list of all doc objects
# when doc object is created it's word frequency is counted
docList = []
for docName in docNameList:
	docList.append( doc(docName) )




global_word_dict = {}   #contains words whose weight is calculated




# calculating word weight
for doc in docList:
    for word in doc.wordFreq:
        if word in global_word_dict:
            doc.wordWeight[word] = global_word_dict[word]
        else:
            doc.wordWeight[word] = calculate_word_weight(docList,word)
            global_word_dict[word] = doc.wordWeight[word]


for doc in docList:
    doc.calThresholdEffectiveFreq()

    #if effective value >= thershold effective freq then add it into summary
    for word,effectiveFreq in doc.effectiveFreq.items():
        if effectiveFreq >= doc.thresholdEffectiveFreq:
            doc.summary += word + "\n"




# creating a summary folder
os.makedirs("summary")
os.chdir("summary")

# putting all summary in file with the same name as Doc name
for doc in docList:
	tmpFile = open(doc.docName,"w")
	tmpFile.write( doc.summary )
	tmpFile.close()