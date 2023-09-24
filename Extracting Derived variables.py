import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import os
import syllables
import pandas as pd

os.chdir(r'C:\Users\Satvinder Singh\Documents\Intrnshala_Assignment\Textual_Analysis')

path = r"text_Files\after"
path2 = r"text_Files"


with open(r"MasterDictionary\positive-words.txt") as f:
    positiveWords = word_tokenize(f.read())

with open(r"MasterDictionary\negative-words.txt") as f:
    negativeWords = word_tokenize(f.read())


def personal_pronoun_count(text):
    pronoun_count = re.compile(r'\b(I|we|ours|my|mine|(?-i:us))\b', re.I)
    pronouns = pronoun_count.findall(text)
    return len(pronouns)


def Average_Word_Length(text):
    c = 0
    words = text.split()
    for word in words:
        c += len(word)
    try:
        return round(c/len(words), 2)

    except:
        return 0


def syllables_count(token):
    l = []
    for i in token:
        l.append(syllables.estimate(i))
    try:
        return round((sum(l)/len(l)), 2)
    except:
        return 0


def Sentence_analysis(complex_word, total_words, number_of_sentences, SA):
    try:
        Average_Sentence_Length = round(total_words / number_of_sentences, 2)
        Percentage_of_Complex_words = round(complex_word / total_words, 2)
        Fog_Index = round(0.4 * (Average_Sentence_Length +
                          Percentage_of_Complex_words), 2)
        SA['AVG SENTENCE LENGTH'].append(Average_Sentence_Length)
        SA['PERCENTAGE OF COMPLEX WORDS'].append(Percentage_of_Complex_words)
        SA['FOG INDEX'].append(Fog_Index)
    except ZeroDivisionError as e:
        SA['AVG SENTENCE LENGTH'].append(0)
        SA['PERCENTAGE OF COMPLEX WORDS'].append(0)
        SA['FOG INDEX'].append(0)
    return SA


positive_counts = []
negative_counts = []
file_p = []
word_avg_length = []
complex_word_list = []
polarity = []
subjectivity = []
url_ids = []

SA = {'AVG SENTENCE LENGTH': [],
      'PERCENTAGE OF COMPLEX WORDS': [], 'FOG INDEX': []}
avg_w_len = []
Average_Number_of_Words_Per_Sentence = SA['AVG SENTENCE LENGTH']
pronouns = []
syllables_count_Per_Word = []
total_words_count = []


for file in os.listdir(path):
    file_path = f"{path}\{file}"
    file_p.append(file)
    f = open(file_path, errors='ignore')
    text = f.read()
    res = re.sub(r'[^\w\s]', '', text)
    p = 0
    n = 0
    complex_word = 0
    sylb_count = 0

    token = word_tokenize(res)
    total_words = len(token)
    total_words_count.append(total_words)

    sen = sent_tokenize(text)
    number_of_sentences = len(sen)

    for i in token:
        if i.lower() in positiveWords:
            p += 1
        elif i.lower() in negativeWords:
            n += 1

    for i in token:
        if syllables.estimate(i) > 2:
            complex_word += 1
    complex_word_list.append(complex_word)

    c = 0
    for i in token:
        c += len(i)

    polarity.append((round((p - n) / ((p + n) + 0.000001), 2)))
    subjectivity.append(round((p + n)/((total_words) + 0.000001), 2))
    positive_counts.append(p)
    negative_counts.append(n)
    syllables_count(token)
    url_ids.append(file.split('.txt')[0])

    score = {'url_id': url_ids, 'POSITIVE SCORE': positive_counts, 'NEGATIVE SCORE': negative_counts,
             'POLARITY SCORE': polarity, 'SUBJECTIVITY SCORE': subjectivity}
    SA = Sentence_analysis(
        complex_word, total_words, number_of_sentences, SA)
    avg_w_len.append(Average_Word_Length(text))
    pronouns.append(personal_pronoun_count(text))
    syllables_count_Per_Word.append(syllables_count(token))
    try:
        word_avg_length.append(round(c/len(token)))
    except:
        word_avg_length.append(0)

score.update(SA)
score.update({"AVG NUMBER OF WORDS PER SENTENCE": Average_Number_of_Words_Per_Sentence,
                  'COMPLEX WORD COUNT': complex_word_list,
                  'WORD COUNT': total_words_count,
                  'SYLLABLE PER WORD': syllables_count_Per_Word,
                  'PERSONAL PRONOUNS': pronouns,
                  'AVG WORD LENGTH': word_avg_length})
df1 = pd.DataFrame(score)
print(df1)
df1.to_excel('Final_output.xlsx')
