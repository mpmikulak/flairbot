#!/usr/bin/python3

import praw
import dataset
import datetime

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

# Connect to the database and return a table
def obtain_database():
    # Connect to the database
    try:
        db = dataset.connect('sqlite:///rep.db')
    except Exception:
        print("There was a problem connecting to the database.")
    print("Connected to the database.")
    return db

# Obtain current value of poster reputation
def get_rep(table, poster):
    rep = table.find(name=poster)
    if rep is None:
        return 0
    return int(rep['rep'])


# Add reputation to the poster in the database
def add_rep(submission_table, reputation_table, comment):
    taken = submission_table.find(comment.submission.id)
    awardee = comment.submission.author.name
    if taken is None:
        reputation_table.insert(dict(name=awardee, rep = get_rep(reputation_table, awardee) + 1))
        submission_table.insert(dict(name=comment.submission.id, used=True))

def main():
    # Authenticate with Reddit and obtain a reddit instance
    reddit = authenticate()

    # Connect to the database
    db = obtain_database()

    # Obtain a reputation table in the database
    reputation_table = db['rep']

    # Obtain a submission tracker in the database
    submission_table = db['sub']

    # Manage the reddit instance   
    print("Beginning stream...")         
    for comment in reddit.subreddit(SUBREDDIT_NAME).stream.comments(skip_existing=True):
        print("{}: {}".format(comment.author.name, comment.body))
        if comment.body in KEYWORDS:
            poster = comment.submission.author.name
            add_rep(submission_table, reputation_table, comment)
            reddit.subreddit(SUBREDDIT_NAME).flair.set(poster, "{}{}".format(FILLER, get_rep(reputation_table, poster)))
            

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

if __name__ == "__main__":
    main()


