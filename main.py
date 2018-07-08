import json
import sys
import requests
import api_keys as ak
from requests_oauthlib import OAuth1Session

def authenticate():
    toauth = OAuth1Session(ak.AP, ak.APS, ak.AT, ak.ATS)
    return toauth

def tl():
    uri = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    toauth = authenticate()
    params = {}
    req = toauth.get(uri, params = params)
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:
            print('== ', tweet['user']['name'],' (' , tweet['created_at'] , ')')
            print(tweet['text'])
            print('retweets : ', tweet['retweet_count'])
            print('------------------')
    else:
        print ("Error: %d" % req.status_code)
    # print("called tl")
    return

def post():
    uri = "https://api.twitter.com/1.1/statuses/update.json"
    toauth = authenticate()
    params = {}
    content = input("> ")
    params['status'] = content
    req = toauth.post(uri, params)
    if req.status_code == 200:
        print("== Sucessfully tweeted ==")
        print(content)
    else:
        print ("Error: %d" % req.status_code)
    # print("called post")
    return

def help():
    print("Usage: twit-cli [command] [options]")
    print("-----------------------------------")
    print("[command list]")
    print("  tl : show twitter timeline")
    print("post : tweet new post on timeline")
    print("[options]")
    print("currently no options")

def main():
    commands = {"tl": tl, "post": post , "help": help}
    argv = sys.argv
    argc = len(argv)
    if argc < 2:
        help()
        return
    if argv[1] in commands:
        commands[argv[1]]()
    else:
        print("Unknown command :", argv[1])
        help()

if __name__ == '__main__':
    main()
