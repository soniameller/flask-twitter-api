# IMPORTS
# ------ Flask ------
import flask
from flask import request, jsonify

# ------ Logic ------
import scraping 
import sentimentAnalysis 
import textAnalysis



app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/tweets/', methods=['GET'])
def tweets():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.

    if 'query' in request.args:
        searchQuery = str(request.args['query'])
        maxTweets = 500
        lang = ''
        if 'maxTweets' in request.args:
            maxTweets = int(request.args['maxTweets'])
        if 'lang' in request.args:
            lang = str(request.args['lang'])

        df = scraping.tweets_to_df(searchQuery,maxTweets,language=lang,geocode=[])
        df = scraping.get_full_text(df)
        top = scraping.get_top_tweets(df,5)
        text= scraping.df_to_clean_text(df)
        sentiment = sentimentAnalysis.sentiment(text)
        wordFreq = textAnalysis.word_freq(text)

    else:
      # pass
        return "Error: No id field provided. Please specify an id."


    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify({'top_tweets':top, 'sentiment': sentiment,'word_freq':wordFreq})


@app.route('/api/top-tweets/', methods=['GET'])
def api_tweets():

    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.

    if 'query' in request.args:
        searchQuery = str(request.args['query'])
        maxTweets = 500
        lang = ''
        if 'maxTweets' in request.args:
            maxTweets = int(request.args['maxTweets'])
        if 'lang' in request.args:
            lang = str(request.args['lang'])

        df = scraping.tweets_to_df(searchQuery,maxTweets,language=lang,geocode=[])
        df = scraping.get_full_text(df)
        result = scraping.get_top_tweets(df,5)


    else:
      # pass
        return "Error: No id field provided. Please specify an id."


    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify({'tweets':result})

app.run()
