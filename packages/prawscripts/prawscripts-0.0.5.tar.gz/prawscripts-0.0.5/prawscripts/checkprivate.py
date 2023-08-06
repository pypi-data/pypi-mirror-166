def checkprivate(instance):
    for subreddit in instance.redditor(str(instance.user.me())).moderated():
        if (subreddit.subreddit_type == 'private'):
            print (subreddit.display_name, " ", subreddit.subreddit_type)