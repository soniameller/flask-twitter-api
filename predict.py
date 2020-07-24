from keras.models import load_model
import time
import numpy as np
import heapq
import pickle

model = load_model('models/todes_model.h5')

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

chars = load_obj('chars')
indices_char = load_obj('indices_char')
char_indices = load_obj('char_indices')

SEQUENCE_LENGTH = 80
MAX_TWITTER_CHARS = 280

def prepare_input(text):
    x = np.zeros((1, SEQUENCE_LENGTH, len(chars)))
    for t, char in enumerate(text):
        x[0, t, char_indices[char]] = 1.
    return x

def temperatureSample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def sample(preds, top_n=3):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds)
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)

    return heapq.nlargest(top_n, range(len(preds)), preds.take)

def predict_completion(text):
    original_text = text
    completion = ''
    while True:
        x = prepare_input(text)
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, top_n=1)[0]
        next_char = indices_char[next_index]
        text = text[1:] + next_char
        completion += next_char
        if len(original_text + completion) + 2 > len(original_text) and next_char == ' ':
            return completion

def predict_completions(text, n=3): 
    x = prepare_input(text)
    preds = model.predict(x, verbose=0)[0]
    next_indices = sample(preds, n)
    return [indices_char[idx] + predict_completion(text[1:] + indices_char[idx]) for idx in next_indices]

timestr = time.strftime("%Y%m%d-%H%M%S")
def genSentence(text, words = 2):
    textOG = text
    text = text.lower()
    while len(text) < SEQUENCE_LENGTH:
        text = ' ' + text
    text = text[-SEQUENCE_LENGTH:]
    for i in range(words):
        text = text[-SEQUENCE_LENGTH:]
        pred = predict_completions(text, 1)[0]
        text = text + pred
        textOG = textOG + pred
        #print(text)
        pass
    return textOG

def getTweet(text, tweet_length):
    test_txt = genSentence(text, 1)

    while len(test_txt)<=tweet_length:
        test_txt = genSentence(test_txt, 1)
    return test_txt
