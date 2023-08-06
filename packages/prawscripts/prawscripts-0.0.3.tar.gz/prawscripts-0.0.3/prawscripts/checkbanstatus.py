def checkbanstatus(instance, username):
    """
    Simple script that checks if someone is banned from any of your subs

    Parameters
    ----------
    instance : PRAW Reddit Object
        The name of your PRAW instance
    username : str
        The name of the Redditor in question
    """
    for subreddit in instance.redditor(str(instance.user.me())).moderated():
        try:
            if any(instance.subreddit(subreddit.display_name).banned(redditor=username)):
                print(subreddit.display_name)
        except:
            continue