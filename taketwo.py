#!/usr/bin/python3

import praw
import dataset
import datetime

# OAuth credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = ''
USERNAME = '' # Required to be in edit mode
PASSWORD = '' # Required to be in edit mode

# Subreddt info
SUBREDDIT_NAMES = "" # String separated by "+" eg. "funny+all"
KEYWORDS = ("+1") # Strings separated by a comma eg. ("+1", "up yours")
FILLER = ""

# Returns an authorized instance of reddit
def authenticate_reddit(client_id, client_secret, user_agent, username, password):
    try:
        reddit = praw.Reddit(client_id=client_id,
                                client_secret=client_secret,
                                user_agent=user_agent,
                                username=username,
                                password=password)
    except Exception:
        print(Exception)

    if reddit.read_only:
        print("Authenticated as read only mode.")
    else:
        print("Authenticated as edit mode.")
    return reddit

# Returns the initialized database
def connect_to_database():
    try:
        db = dataset.connect('sqlite:///flairbot.db')
    except Exception:
        print("There was a problem connecting to the database.", Exception)
    print("Connected to the database.")
    return db

# Verifies whether a submission has been used to award reputation. Returns boolean.
def not_taken(submission_id, submission_table):
    taken = submission_table.find_one(submission_id)
    if taken is None:
        return True
    return False

# Finds and returns the value of reputation an individual has
def get_reputation(awardee, reputation_table):
    return reputation_table.find_one(name=awardee)['reputation']

# Modifies the database by adding one to a users reputation
def add_reputation(awardee, reputation_table):
    rep = get_reputation(awardee, reputation_table)
    if rep is None:
        reputation_table.insert(dict(name=awardee, reputation=1))
    else:
        reputation_table.update(dict(name=awardee, reputation=rep+1), ['name'])

# Inserts the submission into the table so it can't be used again
def make_taken(submission_id, sub_table):
    sub_table.insert(dict(submission_id=submission_id, taken=True))

def main():
    # Authenticate with reddit and obtain the reddit instance
    reddit = authenticate_reddit(CLIENT_ID, CLIENT_SECRET, USER_AGENT, USERNAME, PASSWORD)

    # Connect to the database
    database = connect_to_database()

    # Obtain reputation table
    rep_table = database['rep']

    # Obtain submission table
    sub_table = database['sub']

    for comment in reddit.subreddit(SUBREDDIT_NAMES).stream.comments(skip_existing=True):
        if comment in KEYWORDS:
            submission_id = comment.submission.id
            if not_taken(submission_id, sub_table):
                awardee = comment.submission.author.name # Aquire the awardee's name
                add_reputation(awardee, rep_table) # Add a reputation point to the database for that user
                make_taken(submission_id, sub_table) # Add the submission to the database as taken

                subreddit = reddit.subreddit(comment.subreddit.display_name)
                new_rep = get_reputation(rep_table, awardee)
                
                subreddit.flair.set(awardee, "{}{}".format(FILLER, new_rep)) # Apply the flair
                subreddit.reply("Congradulations, your new reputation is now {}".format(new_rep)) # Reply to the OP informing them of their new status
                print("{}'s reputation updated to {}".format(awardee, new_rep)) # Console output

if __name__ == '__main__':
    main()
