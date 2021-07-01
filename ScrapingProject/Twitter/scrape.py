import requests
import json
import csv

ENV = 'https://api.twitter.com/2/tweets/search/all'
auth_token = 'AAAAAAAAAAAAAAAAAAAAAFkYQQEAAAAAn9wUvR%2BCWpx%2FNb%2FAy4v4FwpHgPk%3D7R5XvHce20cfKnJ4gr0UfvjlcG3LnsRhDxa5dIeDVGfSpOqCMe'
data = './ScrapingProject/Twitter/data_de.csv'
samplesize = 10 # amount of requests for testing

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

with open(data, 'r') as csvfile:
    datareader = csv.DictReader(csvfile)
    i=0
    for row in datareader:
        file_number = row['file_number']
        payload = {
            'query' : file_number,
            'max_results' : '10',
            'expansions' : 'author_id',
            'tweet.fields' : 'created_at,lang,conversation_id',
            'user.fields' : 'created_at,entities'
        }
        response = requests.get(ENV, params=payload, auth=BearerAuth(auth_token))

        print(file_number)
        print(response.text)
        i += 1
        if (i == samplesize):
            break






#print(response.text)