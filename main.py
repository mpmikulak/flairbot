#!/usr/bin/python3

import praw
import dataset

# OAuth credentials
CLIENT_ID = 'u2s7QyS8qkpmAA'
CLIENT_SECRET = 'c1R5P5TRhNrx_6ZQG1cJK2NfB_s'
USER_AGENT = 'flairbot'
USERNAME = '' # Required to be in edit mode
PASSWORD = '' # Required to be in edit mode

# SubReddit info
SUBREDDIT_NAME = 'ClashRoyaleTrade'

# Keywords that will increase reputation
KEYWORDS = ('+1')

# Filler text that will appear with the reputation number
FILLER = 'Reputation'

# Authentication function
def authenticate():
    print("Authenticating...")
    try:
        reddit = praw.Reddit(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            user_agent=USER_AGENT,
                            username=USERNAME,
                            password=PASSWORD)
    except Exception:
        print("There was a problem: ", Exception)
    if reddit.read_only:
        print("User is read only.")         
    else:
        print("User is in edit mode.")
    return reddit

def main():
    # Authenticate with Reddit and obtain a reddit instance
    reddit = authenticate()

    # Connect to the database
    try:
        db = dataset.connect('sqlite:///rep.db')
    except Exception:
        print("There was a problem connecting to the database.")
    table = db['rep']
    
    # Manage the reddit instance            
    for comment in reddit.subreddit(SUBREDDIT_NAME).stream.comments():
        if comment.body in KEYWORDS:

if __name__ == "__main__":
    main()

# def getRep(username):
#   rep = table.find(name=username)
#   if rep is None:
#     return 0
#   return int(rep['rep'])

# def addRep(username, amount=1):
#   table.insert(dict(name=username, rep = getRep() + 1))


# for comment in reddit.subreddit('ClashRoyaleTrade').stream.comments():
#     if comment.body in ("+rep", "+1"):
#       op = comment.submission.author
#       reddit.subreddit('ClashRoyaleTrade').flair.set(op, getRep(op))
#       comment.reply("{}'s rep has been updated".format(op))


