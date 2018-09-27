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

# Subreddt info
SUBREDDIT_NAMES = "" # String separated by "+"
FILLER = ""

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

def connect_to_database():
    try:
        db = dataset.connect('sqlite:///flairbot.db')
    except Exception:
        print("There was a problem connecting to the database.", Exception)
    print("Connected to the database.")
    return db

def main():
    # Authenticate with reddit and obtain the reddit instance
    redd = authenticate_reddit(CLIENT_ID, CLIENT_SECRET, USER_AGENT, USERNAME, PASSWORD)

    # Connect to the database
    database = connect_to_database()

    # Obtain reputation table
    rep_table = database['rep']

    # Obtain submission table
    sub_table = database['sub']

    print(rep_table.find_one(name="mike")['reputation'])

if __name__ == '__main__':
    main()
