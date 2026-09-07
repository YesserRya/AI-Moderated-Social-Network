#from base64 import encode
from tensorflow import keras
import json
import string




model = keras.models.load_model("Best10.h5")

with open("dictionary.txt", "r") as f:
    word_index = eval(f.read())
    
    
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])



def review_encode(s):
	encoded = [1]

	for word in s:
		if word.lower() in word_index:
			encoded.append(word_index[word.lower()])
		else:
			encoded.append(2)

	return encoded


def clean(s):
    new_string = s.translate(str.maketrans('', '', string.punctuation))
    return new_string

def getPrediction():

    with open("text.txt", encoding="utf-8") as f:
        for line in f.readlines():
            print(line, "type of line", type(line))
            nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"","").strip().split(" ")
            encode = review_encode(nline)
            encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post", maxlen=250)
            predict = model.predict(encode)
            print(predict)
            print(line)
            print(encode)
            print(predict[0][0])
            return predict[0][0]
getPrediction() 

