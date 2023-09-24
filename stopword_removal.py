import pathlib
import os
from nltk.tokenize import word_tokenize
import nltk



os.chdir(r'C:\Users\Satvinder Singh\Documents\Intrnshala_Assignment\Textual_Analysis\StopWords')

filenames = ['StopWords_Auditor.txt', 'StopWords_Currencies.txt','StopWords_DatesandNumbers.txt','StopWords_Generic.txt','StopWords_GenericLong.txt','StopWords_Geographic.txt','StopWords_Names.txt']
with open('all_stop_words.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)


with open('all_stop_words.txt', 'r') as file:
    StopWordList = set(word_tokenize(file.read()))

os.chdir(r'C:\Users\Satvinder Singh\Documents\Intrnshala_Assignment\Textual_Analysis')
loop_dir = r'text_Files'
save_dir = r'text_Files\after'
cleaned = []

for txt in os.listdir(loop_dir):
	print(txt)
	file = open(loop_dir+'\\' + '.txt', errors='ignore')
	save_file = open(save_dir+'\\' + txt, 'w')
	text = file.read().lower()

	# Apply the stoplist to the text
	cleaned = [word for word in text.split() if word not in StopWordList]

	save_file.writelines(["%s\n" % item  for item in cleaned])

