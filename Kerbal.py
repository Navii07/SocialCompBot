import praw

reddit = praw.Reddit(client_id='kQalmPPoSPu9T4PwHrlyuw', client_secret='KtDxAZakapW1EZv3NTUCsDjRJVZojQ', user_agent='manavvats')
subreddit_name = 'CompSocial'
subreddit = reddit.subreddit(subreddit_name)

keyword = 'recent'

def send_direct_message(user, subject, message):
    reddit.redditor(user).message(subject, message)
    userList = "socialcomputer", "manavvats", "mission_balance2721"

for submission in subreddit.new(limit=10):
    if keyword in submission.title.lower():
        print("The word 'people' was used in the title of the post:")
        print(submission.title)
        # send_direct_message(submission.author.name, "[insert message here]")
    if keyword in submission.selftext.lower():
        print("The word 'people' was used in the body of the post:")
        print(submission.selftext)
        # send_direct_message(submission.author.name, "[insert message here]")
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if keyword in comment.body.lower():
            print("The word 'people' was used in a comment:")
            print(comment.body)
            # send_direct_message(comment.author.name, "[insert message here]")