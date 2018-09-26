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
SUBREDDIT_NAME = 'funny'

# Keywords that will increase reputation
KEYWORDS = ('+1')

# Filler text that will appear with the reputation number
FILLER = 'Reputation:'

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
        print("There was a problem connecting to the database.", Exception)
    print("Connected to the database.")
    return db

# Obtain current value of poster reputation
def get_rep(table, poster):
    rep = table.find(name=poster)
    if rep is None:
        return 0
    return int(table[poster])


# Add reputation to the poster in the database
def add_rep(submission_table, reputation_table, comment):
    submission_id = comment.submission.id
    taken = submission_table.find(submission_id)
    awardee = comment.submission.author.name
    if taken is None:
        reputation_table.insert(dict(name=awardee, rep=get_rep(reputation_table, awardee) + 1))
        submission_table.insert(dict(name=submission_id, used=True))

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
        
        if comment.body in KEYWORDS:
            print("Matching comment: {}: {}: {}".format(comment.author.name, comment.body, comment.submission.id))
            poster = comment.submission.author.name
            add_rep(submission_table, reputation_table, comment)
            reddit.subreddit(SUBREDDIT_NAME).flair.set(poster, "{}{}".format(FILLER, get_rep(reputation_table, poster)))
            print("{}'s reputation updated to {}".format(poster, get_rep(reputation_table, poster)))
            
if __name__ == "__main__":
    main()


