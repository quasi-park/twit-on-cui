import json
import sys
import requests
import api_keys as ak
from requests_oauthlib import OAuth1Session

def authenticate():
    toauth = OAuth1Session(ak.AP, ak.APS, ak.AT, ak.ATS)
    return toauth

def is_number(s):
    try:
        int(s)
        return True
    except ValueaError:
        return False

def retweet(action, timeline, toauth):
    uri = 'https://api.twitter.com/1.1/statuses/retweet/'
    for target in action[1:]:
        if(is_number(target)):
            tgt = int(target) - 1
        else:
            print(tgt, 'is an invalid input')
            continue

        if tgt> len(timeline):
            print(target, ' is bigger than retrived timeline')
        else:
            uri2 = uri + timeline[tgt]['id_str'] + '.json'
            req = toauth.post(uri2, params = {'id': timeline[tgt]['id_str']})
            if req.status_code == 200:
                print("== retweeted ==")
            else:
                print("== !!Could not retweet!! ==")
            print(timeline[tgt]['text'])
    return

def unretweet(action, timeline, toauth):
    uri = 'https://api.twitter.com/1.1/statuses/unretweet/'
    for target in action[1:]:
        if(is_number(target)):
            tgt = int(target) - 1
        else:
            print(tgt, 'is an invalid input')
            continue
        if tgt> len(timeline):
            print(target, ' is bigger than retrived timeline')
        else:
            uri2 = uri + timeline[tgt]['id_str'] + '.json'
            req = toauth.post(uri2, params = {'id': timeline[tgt]['id_str']})
            if req.status_code == 200:
                print("== unretweeted ==")
            else:
                print("== !!Could not unretweet!! ==")
            print('== ', timeline[tgt]['user']['name'],' (' , timeline[tgt]['created_at'] , ')')
            print(timeline[tgt]['text'])
            print('-------------------')
    return

def favorite(action, timeline, toauth):
    uri = 'https://api.twitter.com/1.1/favorites/create.json'
    for target in action[1:]:
        if(is_number(target)):
            tgt = int(target) - 1
        else:
            print(tgt, 'is an invalid input')
            continue

        if tgt> len(timeline):
            print(target, ' is bigger than retrived timeline')
        else:
            req = toauth.post(uri, params = {'id': timeline[tgt]['id_str']})
            if req.status_code == 200:
                print("== favorited ==")
            else:
                print("== !!Could not favorite!! ==")
            print(timeline[tgt]['text'])
    return

def unfavorite(action, timeline, toauth):
    uri = 'https://api.twitter.com/1.1/favorites/destroy.json'
    for target in action[1:]:
        if(is_number(target)):
            tgt = int(target) - 1
        else:
            print(tgt, 'is an invalid input')
            continue
        if tgt> len(timeline):
            print(target, ' is bigger than retrived timeline')
        else:
            req = toauth.post(uri, params = {'id': timeline[tgt]['id_str']})
            if req.status_code == 200:
                print("== unfavorited ==")
            else:
                print("== !!Could not unfavorite!! ==")
            print('== ', timeline[tgt]['user']['name'],' (' , timeline[tgt]['created_at'] , ')')
            print(timeline[tgt]['text'])
            print('-------------------')
    return

def tl():
    action_list = {'retweet':retweet, 'rt': retweet, 'unretweet':unretweet, 'urt': unretweet, 'favorite': favorite, 'unfavorite': unfavorite}
    uri = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    toauth = authenticate()
    params = {}
    req = toauth.get(uri, params = params)
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for i, tweet in enumerate(timeline, 1):
            print(i, '== ', tweet['user']['name'],' (' , tweet['created_at'] , ')')
            print(tweet['text'])
            print('retweets : ', tweet['retweet_count'], '[', 'v' if tweet['retweeted'] else ' ', ']')
            print('favorites: ', tweet['favorite_count'], '[','v' if tweet['favorited'] else ' ', ']')
            print('------------------')
        while True:
            action = input("actions(q to exit) >")
            action = action.split(' ')
            if action[0] == 'quit' or action[0] == 'q':
                return
            else:
                if action[0] in action_list:
                    action_list[action[0]](action, timeline, toauth)
                else:
                    print("Action does not exist")
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
    commands = {"tl": tl, "timeline": tl, "post": post, "help": help}
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
