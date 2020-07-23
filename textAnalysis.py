import nltk  
from collections import OrderedDict

def word_freq(text,query,language):
    corpus = nltk.sent_tokenize(text)
    wordfreq = {}

    for sentence in corpus:
        
        tokens = nltk.word_tokenize(sentence)
        
        stop_words = set(nltk.corpus.stopwords.words(language))   
        filtered_sentence = [w for w in tokens if not w in stop_words]
        
        for token in filtered_sentence:
            if token not in query.split():
                if token not in wordfreq.keys():
                    wordfreq[token] = 1
                else:
                    wordfreq[token] += 1

    d_descending = OrderedDict(sorted(wordfreq.items(), key=lambda kv: kv[1], reverse=True))
    word_list = list(d_descending.items())
    word_list
    return [{'text':word[0], 'value':word[1]} for word in word_list]