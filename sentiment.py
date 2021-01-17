from google.cloud import language_v1

def analyze_sentiment(text_content):
    # Imports the Google Cloud client library
    from google.cloud import language_v1
    print("Running sentinment analysis...")
    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    print("Sentiment (positivity, intensity): {}, {}".format(sentiment.score, sentiment.magnitude))
    return [sentiment.score, sentiment.magnitude]
