# -*- coding: utf-8 -*-
"""XC410-Summarization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yC_7EtKV8RvKrVGIEWOZ1deJpgj-jgGq
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install pdfreader
!pip install PyPDF2
#PDFreader doccumentation
#https://pdfreader.readthedocs.io/en/latest/tutorial.html

from PyPDF2 import PdfReader
from pdfreader import PDFDocument, SimplePDFViewer
from google.colab import drive
import pandas as pd
drive.mount('/content/drive')

from PyPDF2 import PdfReader

def PDFread(y):
# creating a pdf reader object
  reader = PdfReader(y)
  total = ""
  for x in range(len(reader.pages)):
    page = reader.pages[x]
    text = page.extract_text()
    total += text

  return total

from google.colab import drive
from PyPDF2 import PdfReader
import pandas as pd
import glob

# Mount Google Drive
drive.mount('/content/drive')

# Set the path to the directory containing the PDF files
path = "/content/drive/Shareddrives/Warrants/Warrants/Warrants_OCR"

# Create an empty dataframe to store the extracted text
df = pd.DataFrame(columns=["Filename", "Text"])
i = 0
# Iterate over the PDF files in the directory and extract text from each file
for file in glob.glob(path + "/*.pdf"):
  i+=1
  print(i)
  try:
        # Read the PDF file using PyPDF2
      text = PDFread(file)
        
        # Append the extracted text to the dataframe as a new row
      df = pd.concat([df, pd.DataFrame({"Filename": [file], "Text": [text]})], ignore_index=True)
  except Exception as e:
      print(f"Error processing file {file}: {e}")

# Save the dataframe to a CSV file
df.to_csv("extracted_text.csv", index=False)

df

import numpy as np
 df["Summary"] = np.nan

!pip install torch==1.8.0
!pip install transformers==3.4.0
!pip install sentencepiece

df

pip install --upgrade transformers

from google.colab import files

df.to_csv('df.csv')
files.download('df.csv')

import torch
import json
import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

def summary(text):
  model = T5ForConditionalGeneration.from_pretrained('t5-small')
  tokenizer = T5Tokenizer.from_pretrained('t5-small', model_max_length=30000)
  device = torch.device('cpu')


  preprocess_text = text.strip().replace("\n","")
  t5_prepared_Text = "summarize: "+preprocess_text


  tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)


  # summmarize 
  summary_ids = model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=30,
                                    max_length=100,
                                    early_stopping=True)

  output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

import pandas as pd
i = 0
# Apply the summary function to each row of the dataframe and store the result in a new column called "Summary"
for index, row in df.iterrows():
    i+=1
    print(i)
    df.at[index, 'Summary'] = summary(row['Text'])

df

# LOOKING FOR WHAT THEY ARE SEARCHING FOR IN THE WARRENT
from transformers import pipeline
from datasets import load_dataset

dataset = load_dataset("multi_news")
def trans(text):
  classifier = pipeline("summarization")
  classifier(text)
## [{ "summary_text": " Paris is the capital and most populous city of France..." }]