# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:29:34 2022

@author: Pablo
"""

import pandas as pd
import PyPDF2
import nltk
from nltk import word_tokenize
from collections import Counter


# Remove all the text after the keyword 'delim'
def ref_remover(s, delim):
    return s.partition(delim)[0]

# Download tagger
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

# Configure stopwords 
nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
#print(stopwords)

# Custom stopwords
new_stopwords = ['ieee']

# Extend the stopwords
stopwords.extend(new_stopwords)

# Configure characters
special_characters = ['!','#','$','%', '&','@','[',']',' ',']','_', '.', ',', '(', ')', ':', ';', '“', '”', '-', '|']

# Open the PDF File using a File Object by Parsing
filename ='3.pdf' 

pdfFileObj = open(filename,'rb')               
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   
#Reads the number of pages in the PDF
num_pages = pdfReader.numPages                 

#Reads through all the pages
count = 0
text = ""
     
# Extract text from pdfs                                                       
while count < num_pages:                       
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()

# Remove everything after REFERENCES
#text = ref_remover(text, "REFERENCES")

with open('raw_tex.txt', 'w', encoding="utf-8") as f:
    f.write(text)


# Keep only nouns
text_tokens = word_tokenize(text)
tags = nltk.pos_tag(text_tokens, tagset = "universal")
nouns = [word for word,pos in tags if (pos == 'NOUN')]
back_to_tokens = word_tokenize(' '.join(nouns))

# Remove stop words
filtered_sentence_raw = [w for w in back_to_tokens if not w.lower() in stopwords]
filtered_sentence_raw = [w for w in filtered_sentence_raw if not w.lower() in special_characters]
filtered_sentence = ' '.join(filtered_sentence_raw)
#print(filtered_sentence)


with open('filtered_tex.txt', 'w', encoding="utf-8") as f:
    f.write(filtered_sentence)

# Separates out the keywords from the text and count
counts = Counter(filtered_sentence_raw)
#print(counts)


# Create a dataframe of the keywords for easier processing using pandas package and prevents duplicates
df = pd.DataFrame.from_records(list(dict(counts).items()), columns=['keywords','number_of_occurences'])
#display(df)


# Sort the words in the order of weights
df = df.sort_values('number_of_occurences',ascending=False)

# Print the dataframe
print(df.head(20))

# Stores the data in excel file
#writer = pd.ExcelWriter('keywords_extracted.xlsx', engine='xlsxwriter')
#df.to_excel(writer, sheet_name='Sheet1')
#writer.save()

# Save the most important features in an array
feature_words = df.head(3)['keywords'].to_numpy()
#print(feature_words)

# Convert to string
features_string = ','.join(feature_words)
#print(features_string)







