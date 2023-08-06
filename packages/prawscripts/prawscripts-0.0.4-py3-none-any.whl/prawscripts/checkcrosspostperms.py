def checkcrosspostperms(instance):
    """
    Simple script that checks subs that doesn't allow crossposts

    Parameters
    ----------
    instance : PRAW Reddit Object
        The name of the PRAW instance
    """
    for subreddit in instance.redditor(str(instance.user.me())).moderated():
        try:
            if not instance.subreddit(subreddit.display_name).mod.settings()['allow_post_crossposts']:
                print(f'{subreddit.display_name} \n')
        except:
            continue