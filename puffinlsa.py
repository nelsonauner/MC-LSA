#-------------------------------------------------------------------
#By Nelson Auner - October 2012
#Adapted, and greatly modified, from http://www.puffinwarellc.com/lsa.py
#
# Instructions
#
#
#
# TODO: better parsing (in nelsonfunctions)
# Eliminate words that only appear in one (or two or three) text file. 
#
#


from pylab import *
from numpy import zeros
from scipy.linalg import svd
#following needed for TFIDF
from math import log
from numpy import *
from nelsonfunctions import *
import time


#---------------------------------------------------------
threshold = 784  # # of docs is 1567 #How many times must a word be mentioned for it to be included
#---------------------------------------------------------


class LSA(object):
    def __init__(self, filestem,sourcedoc,noartist=0): 
        self.noartist=noartist
        self.sourcedoc = sourcedoc #the document that has the list of sources
        self.filestem = filestem
        self.stopwords = csw(nltk.corpus.stopwords.words('english'),"newstopwords.txt")
        self.wdict = {} #This will map word -> docs
        self.IDandSources = {}   #What is this, bozo: 
        self.BagLength =  {}  #Dictionary of artistID (string) and how many words in their bag (integer)
        self.dcount = -1 #and goes down        
        self.minthreshold = 1  #A word has to appear in more than 'threshold' documents to be included
        self.maxthreshold = 784
		
		
	# def loadFromOneFile(self):
		# """load from sourcedoc directly. Must be organized " [ID] | [BAGOWORDS] " where [ID] is identifier and [BAGOWORDS] is words to be identified"""
		# contents = open(self.sourcedoc,'r')
		# for s in sourcefile:
			# splitsource = s.split("|")
			# self.IDandSources
				
			
		
    def loadsources(self):
        """ Using self.sourcedoc, finds or creates and ID for each source in the doc, and adds it to the IDandSources dictionary for later parsing
		If noartist = 0, then each line of sourcedoc should have a file location. If noartist = 1, then each line of sourcedoc should be [ID] , [FILE_LOCATION] """
        print("loading sources!")
        sourcefile = open(self.sourcedoc,'r')
        for s in sourcefile.read().splitlines():
            #print(s)
            splitsource = s.split(",")
            if self.noartist == 1:
                tempID = str(self.dcount)
                song = splitsource[1]
                self.dcount += -1
            elif len(splitsource)==1: #If there is no artistID, use dcount
                tempID = str(self.dcount)
                song = splitsource[1]
                self.dcount += -1
            elif len(splitsource)==2:  #If there is an artistID
                tempID = splitsource[0]
                song = splitsource[1]
			#This is perfomed each time
            if tempID in self.IDandSources:
                self.IDandSources[tempID].append(song)
            else:
                self.IDandSources[tempID] = [song]

    def parseAllSources(self):
        """Go through self.IDandSources and parse each document! """
        stem = self.filestem
        for ID, songsources in self.IDandSources.items():
            for source in songsources:
            	words = nltk.word_tokenize(customparse(stem+"\\"+source)) #add the local file stem back to the short file stem
                #words is a list of words
                for w in words:
                    w = spellandstem(w)   #correct spelling and stem it? 
                    if w in self.stopwords:
                        continue
                    elif w in self.wdict:
                        self.wdict[w].append(ID)   
                        #self.docdic[self.dcount].append(w)
                    else:
                        self.wdict[w] = [ID]
						
    def completematrix(self):
    	self.countwdict = self.wdict
    	l = len(self.sources)
    	#self.cm = zeros((len(self.wdict.keys()),len(self.sources)),dtype=numpy.int8)
    	for key in self.countwdict.keys():
    		self.countwdict[key] = listcompressor(list=self.wdict[key],length=l)

    def printcountcsv(self,title,filename):
        print("Printing the countwdict to "+filename)
        out = open(filename+".csv","w")
        l = len(self.sources)
        sourcestoprint = lscleaner(self.sources,[".txt","C:\cygwin\home\nelson auner\Pontikes\FinalData.OctNewKeepAndAnonymous"])
        out.write(csvprintline([title]+sourcestoprint,delim="|"))
        for key in self.wdict.keys():
            #print([key]+(listcompressor(self.wdict[key],l)))
            out.write(csvprintline([key]+(listcompressor(self.wdict[key],l)),delim="|"))
        
    def incrementBagLength(ID,length): #ID is string, length is scalar
        if ID in self.BagLength:
                self.BagLength[ID]+=length   #new size of Bag of words is previous size + size of new document
        else:
            self.BagLength[ID] =length

    def build(self):
        self.keys = [k for k in self.wdict.keys() if (self.maxthreshold  > len(set(self.wdict[k])) > self.minthreshold)]
        self.keys.sort()
        keylen = len(self.keys)
        #self.vectors = [self.makeVector(tokens) for tokens in self.keys] <--- why did you remove this??
        self.A = zeros((len(self.keys), len(self.IDandSources.keys())),dtype="int")
        for i, k in enumerate(self.keys):
            print("Key "+str(i)+"/"+str(keylen))
            for id in self.wdict[k]:
                self.A[i,self.IDandSources.keys().index(id)] += 1

    def storenorms(self):
        self.norms = [norm(self.A[:,i]) for i in range(0,len(self.A[1,])) ]

    def TFIDFPrint(self):
        """Print each word's TDIF power"""
        limit = 400
        counter = 1
        outpath = open("WordTFIDFnew.txt","w")
        outpath.write("Token|TF|DF|IDF\n")
        numberofdocs=len(self.IDandSources.keys())
        for word, docs in self.wdict.items():
            df = len(set(docs))
            # if df <= self.threshold:
            #     continue
            #skip a word if it does not meet threshold
            tf = len(docs)
            idf = math.log((numberofdocs)/df) #this won't work with artists...
            outpath.write(word+"|"+str(tf)+"|"+str(df)+"|"+str(idf)+"\n")
        outpath.close()
        return()

    def tfidfTransform(self,):
		""" Fromhttp://blog.josephwilk.net/projects/latent-semantic-analysis-in-python.html
		With a document-term matrix: matrix[x][y]
		tf[x][y] = frequency of term y in document x / frequency of all terms in document x
		idf[x][y] = log( abs(total number of documents in corpus) / abs(number of documents with term y)  )
		Note: This is not the only way to calculate tf*idf

		Requires self.vectors to be initialized! """
		numWords = len(self.keys) # rows = words
		NumDocs = len(self.IDandSources.keys())
		for  word in xrange(numWords):
			NumDocsWithTerm = float(len(set(self.wdict.keys()[word])))
			idf = log(NumDocs/ NumDocsWithTerm)  #NumDocs does not need to be called as float() explicitely
			for doc in xrange(NumDocs):
				self.vectors[doc][word] *= idf #multiply the existing term frequency by the idf. 
				#termDocumentOccurences = len(self.wdict[self.wdict.keys()[col]])  #cols represent the number of documents, stupid!
				#termFrequency = self.vectors[row][col]/float(wordTotal)
				#inverseDocumentFrequency = log(abs(cols/float(termDocumentOccurences)))
					
					
    def newbuild(self,howmany = -1):
		""" Create the vector space for the new documents strings"""
		if howmany == -1:
			howmany = len(self.IDandSources.keys())
		self.keys = [k for k in self.wdict.keys() if (self.maxthreshold > len(set(self.wdict[k])) > self.minthreshold)]
		self.keys.sort()
		#To conserve memory, create list vector by vector. Vectors can be mapped to the original doc by self.sources[/vector#/]
		self.vectors = []
		for sonum in range(0,howmany): #Or put another number here!
			artistID = self.IDandSources.keys()[sonum]
			self.vectors.append(self.makeVector(artistID))

    def makeVector(self, ID):
        #use tfidf?     
        vector = [0] * len(self.keys)
        for i in range(0,len(self.keys)):
            word = self.keys[i]
            for num in self.wdict[word]:
                if num == str(ID):
                    vector[i]+=1
		if sum(vector) == 0:
			print("Warning: sum of vector == 0 for ID "+str(ID))
        return(vector)

    def cosine(self,v1,v2):
        """related documents j and q are in the concept space by comparing vectors:
            cosine = (v1 * v2) / (||v1|| ||v2||) """
        #print(dot(v1,v2))
        #print(norm(v1))
        #print(norm(v2))
        #print(dot(v1,v2)/(norm(v1)*norm(v2)))
		nv1 = norm(v1)
		nv2 = norm(v2)
		if (nv1 == 0 or nv2 ==0):
			print("warning: zero denominator. Returning 0")
			return 0.0
        return float(dot(v2,v1)/(nv1*nv2))

    def __getTermDocumentOccurances(self,col):
        termDocumentOccurences=0
        rows = self.keys
        cols = len(self.IDandSources.keys())
        for n in xrange(rows):
            if self.vectors[n][col]>0:
                termDocumentOccurences+=1
        return termDocumentOccurences
		
    def calc(self):
        self.U, self.S, self.Vt = svd(self.A)
    def printA(self):
        print 'Here is the count matrix'
        print self.A
    def printSVD(self):
        print 'Here are the singular values'
        print self.S
        print 'Here are the first 3 columns of the U matrix'
        print -1*self.U[:, 0:3]
        print 'Here are the first 3 rows of the Vt matrix'
        print -1*self.Vt[0:3, :]

    def compareartists(self,ID1,ID2):
        return(mylsa.cosine(mylsa.makeVector(ID1),mylsa.makeVector(ID2)))

	def newmag(self):
		outfile = open("QuickLSA_RESULTS.csv","w")
		numdocs = len(self.IDandSources.keys())
		for i in range(numdocs):
			firstID = self.IDandSources.keys()[i]
			for j in range(numdocs-i):
				otherID = self.IDandSources.keys()[i+j]
				print("comparing "+str(firstID)+" with "+str(otherID))
				outfile.write(str(firstID)+","+str(otherID)+","+str(self.cosine(self.vectors[i],self.vectors[i+j]))+"\n") #formula for cosine: <A,B. / ||A|| ||B||
		outfile.close()
		return

    def makeartistgraph(self):
   		outfile = open("QuickLSA_RESULTS.csv","w")
		numdocs = len(self.IDandSources.keys())
		for i in range(numdocs):
			firstID = self.IDandSources.keys()[i]
			for j in range(numdocs-i):
				otherID = self.IDandSources.keys()[i+j]
				outfile.write(str(firstID)+","+str(otherID)+","+str(self.cosine(self.vectors[i],self.vectors[i+j]))+"\n") #formula for cosine: <A,B. / ||A|| ||B||
		outfile.close()
		return
	

    def makekeys(self):
        self.keys = [k for k in mylsa.wdict.keys() if len(set(mylsa.wdict[k])) > 1]

    # def makeartistgraph(self):
    #     #for each artist pairing...
    #     #return the cosine vector
    #     outfile = open("artistcosine.txt","w")
    #     #create the top axis. 
    #     for artistid in IDandSources.keys():
    #         outfile.write(str(artistid)+"|")
    #     outfile.write("\n")
    #     for firstID in IDandSources.keys():
    #         for otherID in IDandSources.keys()[firstID:-1]:
    #             v1 = makeVector(firstID)
    #             print(str(self.cosine(v1,makeVector(otherID)))+"|")
    #         print("\n")
#-------------------------- END OF LSA OBJECT DECLARATION -----------------------------------------------------------------#	
	
def constructor():
    """Initiate building an myLSA document"""
    #Construct a myLSA by loading all the sources from the sources var
    #ignorchars not used?
    mylsa = LSA(filestem = "C:\\Users\\nauner\\Dropbox\\HiphopFiles\\Nelson\\QuickLSA",
        sourcedoc ="C:\\Users\\nauner\\Dropbox\\HiphopFiles\\Nelson\\QuickLSA\\sourcedoc.txt",
        noartist=0)
    print("unpackingsources")
    mylsa.loadsources()
    print("unpacked. now creating word dic")
    start = time.clock()
    #modify to use a sourcelist, not whole string
    mylsa.parseAllSources()
    end = time.clock()
    print("done in "+str(end-start)+" seconds, I think")
    return(mylsa)



def printthatstuff():
        mylsa = LSA(filestem = "C:\\cygwin\\home\\nelson auner\\Pontikes\\FinalData.OctNewKeepAndAnonymous",
        sourcedoc ="C:\\Users\\nelson auner\\Dropbox\\HiphopFiles\\Python Script\\SourceswithArtist.csv",
        noartist=1)
        mylsa.loadsources()
        return(mylsa)


print("constructing")
mylsa = constructor()
print("constructed. building")
mylsa.newbuild()
mylsa.tfidfTransform()
mylsa.makeartistgraph()



#-------------RANDOM CODE BELOW-------------------------------------------------------------------
def printkeys():
    outprint = open("wordlistnov.txt","w")
    for i in mylsa.keys:
        outprint.write(i+"\n")
    outprint.close()

#create the diagnostic plots:

def plotting():
    y = [0,0,0]
    y[0] = [0]*1000
    y[1]= [0]*1000
    y[2] = [0]*1000


    for t in [[0,1],[1,5],[2,100]]:
        mylsa.threshold = t[1]+1
        mylsa.build()
        mylsa.newbuild(1000)
        print(len(mylsa.keys))
        for i in range(1,1000):
            y[t[0]][i]=sum(mylsa.vectors[i])
        y[t[0]].sort()

    #now plot all of these 
    plot(y[0],label="threshold = 1" )
    plot(y[1],label="threshold = 2" )
    plot(y[2],label="threshold = 3" )
    legend(loc="upper left")
    show()
#debugging stuff
#hi = where(mylsa.A )


