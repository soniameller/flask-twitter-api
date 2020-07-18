import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment(text):
  print('corpus length:', len(text))
  analyzer = SentimentIntensityAnalyzer()
  return analyzer.polarity_scores(text)
  
