# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
import json

import sys
import re
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from youtube_transcript_api import YouTubeTranscriptApi

final_stopWords = []
temp_file = open('stopwords.txt', 'r')
final_stopWords = [line.rstrip('\n') for line in temp_file]

def getListFromDict(dict):
    dictlist= []
    for x in dict:
        dictlist.append(x['text'])
    return dictlist

def getFullPhrase(query, dictList):
    listOfPhrases = []
    for phrase in dictList:
        if query.lower() in phrase.lower().split(" "):
            idx = dictList.index(phrase)
            if idx == 0:
                listOfPhrases.append(dictList[idx] + " " + dictList[idx+1])
            elif idx == len(dictList)-1:
                listOfPhrases.append(dictList[idx-1] + " " + dictList[idx])
            else:
                listOfPhrases.append(dictList[idx-1] + " " + dictList[idx] + " " + dictList[idx+1])
           # listOfPhrases.append(dictList[idx])
    return listOfPhrases

def totalKeywordscore(a,b,c):
    numerator = 0
    denominator = 0
    for i in range(len(a)):
        numerator += (a[i]*b[i]*c[i])
        denominator += (b[i]*a[i])

    positive = 0.0
    negative = 0.0
    neutral = 0.0

    for i in range(len(a)):
        if float(c[i]) > 0.01:
            # print("positve",c[i])
            positive += a[i]
        elif float(c[i]) < -0.01:
            # print("negative",type(c[i]))
            negative += a[i]
        else:
            # print("neutral here",c[i])
            neutral += a[i]

    pos = positive/(positive+neutral+negative)
    neu = neutral/(positive+neutral+negative)
    neg = negative/(positive+neutral+negative)

    return numerator/denominator,pos,neg,neu


def sample_analyze_entity_sentiment(text_content,query):
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    client = language_v1.LanguageServiceClient()
    response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    salience = []
    score = []
    magnitude = []

    for entity in response.entities:
        if query.lower() in re.sub(r'[^\w\s]','',entity.name).lower().split(" "):
            # print(u"\n\nRepresentative name for the entity: {}".format(text_content))
            # print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
            # print(u"Salience score: {}".format(entity.salience))
            salience.append(entity.salience)
            sentiment = entity.sentiment
            # print(u"Entity sentiment score: {}".format(sentiment.score))
            # print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
            score.append(sentiment.score)
            magnitude.append(sentiment.magnitude)

    #         for metadata_name, metadata_value in entity.metadata.items():
    #             print(u"{} = {}".format(metadata_name, metadata_value))

    #         for mention in entity.mentions:
    #             print(u"Mention text: {}".format(mention.text.content))
    #             # Get the mention type, e.g. PROPER for proper noun
    #             print(
    #                 u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
    #             )

    # print(u"Language of the text: {}".format(response.language))
    return salience,magnitude,score


def merge(keywordList):
    returnList = ""
    for i in keywordList:
        # print(i["text"])
        returnList += " " + i["text"]
    # print(returnList)
    return returnList





# creating a Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])

# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/<query>/<videoID>', methods = ['GET'])
def getJSON(videoID, query):
    items = dict()
    if query in final_stopWords:        #if the query is not good enough to be searched,return -1
        return(json.dumps(items))
    phrases = getFullPhrase(query, getListFromDict(YouTubeTranscriptApi.get_transcript(videoID)))
    print((phrases))
    a = []
    b = []
    c = []

    if len(phrases)==0:             #if the keyword not found in any phrases
        return(json.dumps(items))

    for x in phrases:
        l,m,n = sample_analyze_entity_sentiment(x,query)
        print(l,m,n)
        if len(l) > 0:
            a.append(l[0])
            b.append(m[0])
            c.append(n[0])

    total2,p,n,nu = totalKeywordscore(a,b,c)
    print(total2)
    temp = {"score": str(total2),"positive" : str(p),"negative": str(n), "neutral" : str(nu)}
    # fullString = '{ "results": [ '
    # for i in range(len(returnList)):
    #     if i == len(returnList)-1:
    #         fullString += '{ \"timestamps": \"' + str(returnList[i]['start']) + 's\", \"phrase\": \"' + returnList[i]['text'] + '\" } '
    #     else:
    #         fullString += '{ \"timestamps\": \"' + str(returnList[i]['start']) + 's\", \"phrase\": \"' + returnList[i]['text'] + '\" }, '
    # fullString += '] }'

    return (json.dumps(temp))

# driver function
if __name__ == '__main__':

	app.run(host='0.0.0.0', port='5001', threaded=True, debug = True)
