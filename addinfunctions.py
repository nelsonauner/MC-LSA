#By Nelson Auner
#Date: October
#A collection of functions to assist Aniket's programs. 
#NEW: My own full-fledge programs, added to the bottom
#New; write 
#----------------------------------------------------------------------------------
import nltk 
import urllib
import csv
import re
from nltk.corpus import stopwords
import nltk
from nltk.corpus import stopwords
from scipy.linalg import svd
import collections
import string
import enchant
dicr = enchant.Dict("en_us")
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
#----------------------------------------------------------------------------------
#edit parameters here:
buzzwords = ["typed","artist","album","title","song"]
# practicesourcepath="C:\\Users\\nelson auner\\Dropbox\\HiphopFiles\\Python Script\\Counts Program\\SourcePath.txt"
# sourcepath="C:\\Users\\nauner\\Dropbox\\HiphopFiles\\Nelson\\QuickLSA\\sourcedoc.txt"
# testtext = open("C://cygwin//home//nelson auner//Pontikes//FinalData.OctNewKeepAndAnonymous/capsavem/my_cape/outtoget.cap.txt").read()
# testsource = "C://cygwin//home//nelson auner//Pontikes//FinalData.OctNewKeepAndAnonymous/capsavem/my_cape/outtoget.cap.txt"
smtesttext = '''
Artist: Sole
Album:  Hip-Hop Music for the Advanced Listener EP
Song:   Dear Elpee
Typed by: jason_ray@mindspring.com
  
[Sole]
Dear El-Pee,
How's your summer been? 
Mine's been fine
I heard you had a real good time at camp
Oh, yeah, I talked to Len, he said everythings cool
Oh, yo, I really liked "End To End Burner"
That little diss me thing on the internet was pretty funny
'''
#-----------------------------------------------------------------------------------------------------------------------------------------------
def spellandstem(word):
	return st.stem(word)


def listprint(openedfile,list):

	for i in list:
		openedfile.write(i+"\n")


def stemspelprac(rawn):
	spellcheck  = [0]*len(rawn)
	stem = [0]*len(rawn)
	for i in range(len(rawn)):
		if dicr.check(rawn[i]):
			spellcheck[i]=""
			stem[i] = st.stem(rawn[i])
		else:
			try: 
				spellcheck[i]=dicr.suggest(rawn[i])
				stem[i] = st.stem(spellcheck[i])
			except:
				spellcheck[i]="ERROR"
	return([spellcheck,stem])



def findverb(ss): 
	"""
	Takes a sentance-string, splits it apart, and uses nltk to search for a verb object, returning a boolean
	"""
	ss = ss.replace("chorus","") #This avoids our problem of "chorus" counting as a verb "VBZ"
	tags = nltk.pos_tag(nltk.Text(nltk.word_tokenize(ss.lower())))
	y = [x[1] for x in tags]
	for i in y:
		if i== 'VBD' or i == 'VBZ':
			return True
	return False



def stemmer10songs():
	#Finish up the lists of words that are surrounded by the following: {[*( --
	seperatorcharacter = "|"
	sourcelist = open("SourceswithArtist.csv","r")
	outfile = open("stem10songs.txt","w")
	count = 10
	wordz=[]
	for source in sourcelist: 
		print(source)
		if count <0:
			break
		count = count-1
		filename = source.split(",")[1][:-1]
		tempraw =customparse("C://cygwin//home//nelson auner//Pontikes//FinalData.OctNewKeepAndAnonymous//"+filename)
	 	wordz.extend(nltk.word_tokenize(tempraw))
	return(wordz)
#O = ["sweating","tripping","gunning","going"] 
	#HH.extend([i[0:-1] for i in O] )

def inchecker(z):
	res = []
	for i in z:
		if len(i) > 2 and i[-2:]=="in" and dicr.check(i) is False and dicr.check(i+"g") is True:
			res.append(i)
	return(res)




#def spellingtest():
def doforsources():
	#Finish up the lists of words that are surrounded by the following: {[*( --
	seperatorcharacter = "|"
	sourcelist = open("SourceswithArtist.csv","r")
	outfile = open("Jan17chorusNOVERB.txt","w")
	for source in sourcelist:
		filename = source.split(",")[1][:-1]
		temptext = customparse("C://cygwin//home//nelson auner//Pontikes//FinalData.OctNewKeepAndAnonymous//"+filename).split("\n")
		webfront = "http://lyrics.chicagobooth.edu/FinalData.OctNewKeepAndAnonymous/"
		pastline = ""
		for line in temptext:
			if line.lower().find("chorus")+1 and len(nltk.word_tokenize(line))  > 4 and not findverb(line): #because finding will return 1, no find returns -1, -1+1 = 0 evaluates to fals
				outfile.write(webfront+filename+seperatorcharacter+line+"\n")
				#else:
					#outfile.write(line+"\n")
	outfile.close()
	sourcelist.close()
	return()



def doforsources():
	#Finish up the lists of words that are surrounded by the following: {[*( --
	seperatorcharacter = "|"
	sourcelist = open("SourceswithArtist.csv","r")
	outfile = open("Jan16chorus.txt","w")
	for source in sourcelist:
		filename = source.split(",")[1][:-1]
		temptext = customparse("C://cygwin//home//nelson auner//Pontikes//FinalData.OctNewKeepAndAnonymous//"+filename).split("\n")
		webfront = "http://lyrics.chicagobooth.edu/FinalData.OctNewKeepAndAnonymous/"
		pastline = ""
		for line in temptext:
			if line.lower().find("chorus")+1 and len(nltk.word_tokenize(line))  > 4 : #because finding will return 1, no find returns -1, -1+1 = 0 evaluates to fals
				outfile.write(webfront+filename+seperatorcharacter+line+"\n")
				#else:
					#outfile.write(line+"\n")
	outfile.close()
	sourcelist.close()
	return()



		# for i in rebrackets:
		# 	bracktsoutfile.write(i+"\n")

		# for i in replus:
		# 	plusoutfile.write(i+"\n")
		# for i in reastirix:
		# 	astirixoutfile.write(i+"\n")






def dosomethingforfiles(sourcelist,outputstring):
	sourcelist = open("SourceswithArtist.csv","r")
	outterfile = open(outputstring,"w")
	for i in sourcelist:
		file = open(i,"r")
		#DO THING HERE
		lines = file.readlines()
		for tb in lines:
			tb  =re.sub(r'\[[^)]*\]', '', tb) #This nukes everything within [ ]
			tb  =re.sub(r'\([^)]*\)', '', tb) #This nukes everything within ( )
			tb  =re.sub(r'\{[^)]*\}', '', tb) #This nukes everything within { }
			tb  =re.sub(r'\*[^)]*\]', '', tb) #This nukes everything within * *
			if tb.find("*")!=-1:
				outfile.write(i[70:len(i)]) #cut of my OS path
				outfile.write("\n"+tb)
				outterfile.write(tb)
	outfile.close()
	outterfile.close()
	return()

def quicklistwrite(filename,listofstrings):
	out = open(filename,"w")
	for word in listofstrings:
		out.write(word+"\n")
	out.close()


def deleteifrepeatchar(replimit,textlist):
	res = []
	for word in textlist:
		for i in range(len(word)-5):
			if not all([word[i+1:i+7]!=word[i]*6 for i in range(len(word)-7)]):
				break
			res.append(word)
			break
	return(res)





def deletefromlines(filein,fileout,deleteif):
	filein = open(filein,"r")
	text = filein.read()
	list = text.split("\n")
	list = [name for name in list if not((name.find(delete))+1)]
	outfile = open(fileout,"w")
	for i in list:
		outfile.write(i+"\n")
	outfile.close()
	filein.close()
	return()




def csvprintline(ls,delim):
	res = ""
	for i in ls:
		res = res+str(i)+delim
	res = res[0:-1]+"\n"
	return(res)

def lscleaner(cleanme,lremove):
	res = []
	for c in cleanme:
		for l in lremove:
			c = c.replace(l,"")
		res = res+[c]
	return(res)



def printtocsv(sfn,lls): #StringofFileName & ListofListS
	print("Entering print phase with file "+sfn)
	out = open(sfn+".csv","w")
	print(len(lls))
	for line in lls:
		for entry in line:
			out.write(str(entry)+"|")
		out.write("\n")
		print(line[0])
	out.close()

def csw(stopwords,filename):
	#Given the existing stopword list and a file of new stopwords, return combines 
	listofwords = [x.strip() for x in open(filename)]
	stopwords.extend(listofwords) 
	return(stopwords)

def nelsonlinewrite(lws,filename,openstyle):
	file = open(filename,openstyle)
	for word in lws:
		file.write(word+"|")
	file.write("\n")
	file.close()

def loadsources(path):
	""" 	
	given the path for a text file containing sources, returns the sources (file location) as a list
	"""
	sources = []
	sourcefile = open(path, 'r')
	for line in sourcefile:
		line =line.replace("\n","")
		sources.append(line)
 	#Use my local copy, folder hierarchy should be the same. 
 	sources = [w.replace('E:/University of Chicago Hip Hop Lyrics Project','C:\\cygwin\\home\\nelson auner\\Pontikes') for w in sources]
 	sources = [w.replace('/','\\') for w in sources]
 	sourcefile.close()
 	return(sources)

def removesonginfo(text,nlines,buzzwords):
	""" Removes any line in the first nlines of the file that contain a buzzword """
	text = text.split("\n")
	for line in text[0:nlines]:
		for word in buzzwords:
			#print("line being searched:"+line)
			match = re.search(word, line, re.IGNORECASE)
			if match:
				#print("MATCH FOUND")
				try:
					text.remove(line)
				except ValueError: #ignore since line has already been removed
					pass
	return(text)

def removebrackets(textlist):
	for tb in textlist: #for each line
		tb  =re.sub(r'\[.*?\]', '', tb) #This nukes everything within [ ]
		tb  =re.sub(r'\(.*?\)', '', tb) #This nukes everything within ( )
		tb  =re.sub(r'\{.*?\}', '', tb) #This nukes everything within { }
		tb  =re.sub(r'\*.*?\*', '', tb) #This nukes everything within * *


def customparse(filelocation):
	''' 
	Helper function for puffinLSA
	takes in the name of a text file
	and returns the blob of text, but edited a bit
	'''
	file = open(filelocation,"r") 
	tb = file.read()
	file.close()

	#print(tb)
	#buzzwords = ["typed","artist:","album:","title:","song:","\n","\t"]
	#tb = removesonginfo(tb,15,buzzwords)
	#tb = "\n".join(tb) #since removesonginfo returns a list of strings
	tb = tb.lower() #convert put back into one string, to all lower case
	#tb = tb.translate(string.maketrans("",""), string.punctuation) #remove ending puctuation
	#tb = tb.replace("\n"," ")
	tb  =re.sub(r'\[.*?\]', '', tb) #This nukes everything within [ ]
	tb  =re.sub(r'\(.*?\)', '', tb) #This nukes everything within ( )
	tb  =re.sub(r'\{.*?\}', '', tb) #This nukes everything within { }
	tb  =re.sub(r'\*.*?\*', '', tb) #This nukes everything within * *
	punctuation = re.compile(r'[.?!,*\":;]')  #This nukes all punctuation and numbers
   	tb = punctuation.sub("", tb)
	#No need to take out stopwords yet - this is handled by the parser itself -- maybe
	#print(tb)
	#tb.split(" ")   #note that this doens't acually do anything....
	#print(tb)
	return(tb)

def spellchecker(word):
	#check if in english dictionary
	if dicr.check(word):
		return word
	else:
		 return dicr.suggest(word)

#def stemmer(word):

def printcolcsv(filename,listofcols):
	outfile = open(filename,"w")
	for i in range(len(listofcols[1])):
		outfile.write()



def uniquelist(sourcelist):
	ul = []
	for source in sourcelist:
		wordlist = parsesource(source)
		ul.extend(wordlist)
	return(ul)


#now we have a list of words. 
#we want to create a large file with 

def conductcount(sourcelist,unilist):
	'''
	Given a list of sources (local path) and list of total unique words, creates a matrix, opens each text file and increments for each time a word is found. 
	'''
	matrix = [[0 for j in range(len(sourcelist))] for i in range(len(unilist))]
	#Iterate over numbers to make indexing to matrix easier!
	for x in range(len(sourcelist)):
		rawlist = parsesource(sourcelist[x])
		for word in rawlist:
			y = unilist.index(word)
			matrix[y][x]+=1
	return(matrix)

def matrixprint(sourcelist,unilist,matrix):
	'''
	Given the list of sources, unique "words", and the matrix of counts (rows: words, columns: songs), prints to a csv file 
	'''
	for i in range(len(matrix)):
		matrix[i].insert(0,unilist[i])
	sourcelist.insert(0,"Nelson Auner")
	matrix.insert(0,sourcelist) #Insert the sourcelist row at the top
	printtocsv("TRACK-WORD-RESULTS",matrix)
	return(matrix)



def listcompressor(list,length):
	rl = [0] * length
	for i in list:
		rl[i] = rl[i]+1
	return(rl)

def go(): 
	'''
	Load a list of sources, clean and then take all unique words to assemble a total list of unique words, then re-read all text files and count word occurences. Stopwords should be declared as global var
	'''

	#load sources
	sourcelist = loadsources(sourcepath)[1:5]
	#print(psourcelist)
	unilist = uniquelist(sourcelist)
	#Creates matrix from list of unique words and source list. 
	matrix = conductcount(sourcelist,unilist)
	x = matrixprint(sourcelist,unilist,matrix)
	print("huzzah")
	return(x)


def debugger():
	stopwords = csw(nltk.corpus.stopwords.words('english'),"newstopwords.txt")
	sourcelist = loadsources(sourcepath)[1]
	unilist = uniquelist([sourcelist])
	results = unilist #parsesource(sourcelist)[1]
	return(results)


#----------------------------------------------------------------------------------------------------------------------------
#stopwords = csw(nltk.corpus.stopwords.words('english'),"newstopwords.txt")
