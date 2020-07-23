# IMPORTS
# ------ Flask ------
import flask
from flask import request, jsonify

# ------ Logic ------
import scraping 
import sentimentAnalysis 
import textAnalysis
# import predict



app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/tweets/', methods=['GET'])
def tweets():
    # Check if QUERY was provided as part of the URL.
    # If QUERY is provided, assign it to a variable.
    # If no QUERY is provided, display an error in the browser.

    if 'query' in request.args:
        searchQuery = str(request.args['query'])
        maxTweets = 500
        lang = ''
        stop_words_lang = ''
        
        if 'maxTweets' in request.args:
            maxTweets = int(request.args['maxTweets'])
        if 'lang' in request.args:
            lang = str(request.args['lang'])

        df = scraping.tweets_to_df(searchQuery,maxTweets,language=lang,geocode=[])
        df = scraping.get_full_text(df) 
        top = scraping.get_top_tweets(df,5)
        text= scraping.df_to_clean_text(df)
        sentiment = sentimentAnalysis.sentiment(text)

        if lang == 'en':
            stop_words_lang = 'english'
        elif lang == 'es':
            stop_words_lang = 'spanish'
        elif lang == 'pt':
            stop_words_lang = 'portuguese'
        
        print('LANGUAGE:',lang,"STOP:", stop_words_lang, "MAX:",maxTweets )

        wordFreq = textAnalysis.word_freq(text,searchQuery,stop_words_lang)

    else:
      # TODO -don't know if this works
        return jsonify({"Error: No query field provided. Please specify a query."})


    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify({'top_tweets':top, 'sentiment': sentiment,'word_freq':wordFreq})

# ---- PREDICTION ROUTER -----

@app.route('/api/tweets/sentiment', methods=['POST'])
def predict():

    tweet = list(request.form.to_dict().keys())[0]
    sentiment = sentimentAnalysis.sentiment(tweet)

    return jsonify(sentiment)



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
