def getmodmailcount(instance):
    """
    Script gets modmail count across multiple subreddits under the assumption there are mail perms on all subreddits

    Parameters
    ----------
    instance : PRAW Reddit Object
        The name of the PRAW instance
    """
    for subreddit in instance.redditor(str(instance.user.me())).moderated():
      x=0
      for convo in instance.subreddit(subreddit.display_name).modemail.conversations(limit=1000):
          x=x+1
      if x>0:
          print(subreddit.display_name, x)