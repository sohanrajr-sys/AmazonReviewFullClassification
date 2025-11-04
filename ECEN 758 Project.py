#ECEN 758 Project Group 7


#***********************************data download******************************

import os, tarfile, pandas as pd, gdown
from pathlib import Path

#find the users downloads folder
downloads_folder = Path.home() / "Downloads"

#creates our project folder for storing data that we have to download
ROOT = downloads_folder / "Amazon Data"
os.makedirs(ROOT, exist_ok=True)
print("Dataset will be stored at:", ROOT)

#Download the official AmazonReviewFull tar.gz from Google Drive
url_id = "0Bz8a_Dbh9QhbZVhsUnRWRDhETzA"   #same ID torchtext uses
tar_path = os.path.join(ROOT, "amazon_review_full_csv.tar.gz") #checks if zip file is there
if not os.path.exists(tar_path): # if file not there then it will begin to download file to the root directory
    print("Downloading dataset tar…")
    gdown.download(id=url_id, output=tar_path, quiet=False, resume=True)

#Extract zip file if needed, skipped if already done
extract_dir = os.path.join(ROOT, "amazon_review_full_csv")
train_csv = os.path.join(extract_dir, "train.csv")
test_csv  = os.path.join(extract_dir, "test.csv")
if not os.path.exists(train_csv):
    print("Extracting tar…")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=ROOT)

#confirms both files are in folder to user
train_path = os.path.join(ROOT, "amazon_review_full_csv", "train.csv")
test_path = os.path.join(ROOT, "amazon_review_full_csv", "test.csv")
print("Train file exists:", os.path.exists(train_path))
print("Test file exists:", os.path.exists(test_path))

#Count lines in each file 
with open(train_path, "r", encoding="utf-8") as f:
    n_lines = sum(1 for _ in f)
print("Train.csv lines:", n_lines)

with open(test_path, "r", encoding="utf-8") as f:
    n_lines = sum(1 for _ in f)
print("Test.csv lines:", n_lines)




#******************************Data cleansing****************************************

import re

#Ask the user how many rows to load for train/val
try:
    num_rows = int(input("Enter how many rows you want to load from Train.csv(max 3000000): "))
except ValueError:
    print("Invalid input. Defaulting to 50000 rows")
    num_rows = 50000

#Ask the user how many rows to load for test
try:
    test_rows = int(input("Enter how many rows to load from test.csv (max 650000): "))
except ValueError:
    print("Invalid input. Defaulting to 10000 rows")
    test_rows = 10000


#Load that many rows
cols = ["label", "title", "review"]
df = pd.read_csv(train_csv, header=None, names=cols, nrows=num_rows)
test_df = pd.read_csv(test_csv, header=None, names=cols, nrows=test_rows)
print(f"Loaded {len(df)} rows from train.csv")
print(f"Loaded {len(test_df)} rows from test.csv")

#Combine title + review into one text column
df["text"] = df["title"].fillna("") + " " + df["review"].fillna("")
test_df["text"] = test_df["title"].fillna("") + " " + test_df["review"].fillna("")

#Convert everything to lowercase
df["text"] = df["text"].str.lower()
test_df["text"] = test_df["text"].str.lower()

#Remove punctuation but keep letters, numbers, and space
df["text"] = df["text"].apply(lambda x: re.sub(r"[^a-z0-9\s]", "", x))
test_df["text"] = test_df["text"].apply(lambda x: re.sub(r"[^a-z0-9\s]", "", x))
label_test = test_df["label"].to_numpy()







#***************************Splitting train data to train/Validation**********************************

import numpy as np
from sklearn.model_selection import train_test_split
print("\nTrain/Validation Split:")

#Keep labels as 1–5
df["label"] = df["label"].astype(int)
label_full = df["label"].to_numpy() 

# Make a validation split from the train dataframe
try:
    val_frac = float(input("Enter validation fraction(0-1): "))
    if not (0 < val_frac < 1):
        raise ValueError
except ValueError:
    print("Invalid input, defaulting to 0.2")
    val_frac = 0.2

data_train_text, data_val_text, label_train, label_val = train_test_split(
    df["text"].values, label_full, test_size=val_frac, random_state=42, stratify=label_full)
print(f"Train texts: {len(data_train_text)} | Val texts: {len(data_val_text)}")
print(f"Label range: {min(label_full)}–{max(label_full)}")




#*************************************Tokenizing data*****************************************

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
print(f"\nTokenizing and padding:")

#Ask user for vocab size, how many unique words to keep 
try:
    vocab_size = int(input("Enter vocab size (e.g. 10000): "))
except ValueError:
    print("Invalid input. Defaulting to 10000.")
    vocab_size = 10000

#Ask user for maxlen, how long each review should be after padding
try:
    maxlen = int(input("Enter max sequence length (e.g. 200): "))
except ValueError:
    print("Invalid input. Defaulting to 200.")
    maxlen = 200


#Fit tokenizer on TRAIN DATA ONLY since its now allowed to have val or test data in here
tokenizer = Tokenizer(num_words=vocab_size, oov_token="(OOV)")
tokenizer.fit_on_texts(data_train_text)

#Convert text to numeric sequences
seq_train = tokenizer.texts_to_sequences(data_train_text)
seq_val   = tokenizer.texts_to_sequences(data_val_text)
seq_test  = tokenizer.texts_to_sequences(test_df["text"].values)

#Pad/cut sequences to fixed length
data_train = pad_sequences(seq_train, maxlen=maxlen, padding="post", truncating="post")
data_val   = pad_sequences(seq_val,   maxlen=maxlen, padding="post", truncating="post")
data_test  = pad_sequences(seq_test,  maxlen=maxlen, padding="post", truncating="post")

print(f"\nData Sizes(rows, sequence length):  data_train: {data_train.shape}, data_val: {data_val.shape}, data_test: {data_test.shape}")
print(f"\nLabel Sizes(rows):  label_train: {label_train.shape}, label_val: {label_val.shape}, label_test: {label_test.shape}")
print("Label ranges -> train:", label_train.min(), "-", label_train.max(), "| val:", label_val.min(), "-", label_val.max(),
    "| test:", label_test.min(), "-", label_test.max())





#***************************************Exploratory Data Analysis***************************






