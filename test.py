# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
import json

final_stopWords = []
temp_file = open('stopwords.txt', 'r')
final_stopWords = [line.rstrip('\n') for line in temp_file]


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
    returnList = []
    if query in final_stopWords:        #if the query is not good enough to be searched,return -1
        return(json.dumps(returnList))
    keywordList = YouTubeTranscriptApi.get_transcript(videoID)
    for i in keywordList:
        phrase = i['text']
        if query.lower() in phrase.lower():
            temp = {"timestamp": str(i['start']) + 's',
                    "phrase": i['text']}
            returnList.append(temp)
    # fullString = '{ "results": [ '
    # for i in range(len(returnList)):
    #     if i == len(returnList)-1:
    #         fullString += '{ \"timestamps": \"' + str(returnList[i]['start']) + 's\", \"phrase\": \"' + returnList[i]['text'] + '\" } '
    #     else:
    #         fullString += '{ \"timestamps\": \"' + str(returnList[i]['start']) + 's\", \"phrase\": \"' + returnList[i]['text'] + '\" }, '
    # fullString += '] }'

    return (json.dumps(returnList))

# driver function
if __name__ == '__main__':

	app.run(host='0.0.0.0', port='5000', threaded=True, debug = True)
