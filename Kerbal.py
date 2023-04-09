import praw

reddit = praw.Reddit(client_id='kQalmPPoSPu9T4PwHrlyuw', client_secret='KtDxAZakapW1EZv3NTUCsDjRJVZojQ',
                     user_agent='manavvats')
subreddit_name = 'neckbeardstestroom'

command_phrase = "!subto"

subreddit = reddit.subreddit(subreddit_name)


def send_direct_message(user, subject, message):
    reddit.redditor(user).message(subject, message)

print(subreddit.stream.comments)
for comment in subreddit.stream.comments(skip_existing=True):
    print(command_phrase in comment.body)
    if command_phrase in comment.body:
        input_keywords = comment.body.replace(command_phrase, "").strip()
        all_keywords = input_keywords.split(",")
        first_word = all_keywords[0]
        keyword = first_word
        print(keyword)
    for submission in subreddit.new(limit=10):
        # if keyword.lower() in submission.title.lower():
        if submission.title.lower().find(keyword.lower()) != -1:
            print("The word " + keyword + " was used in the title of the post:")
            print(submission.title)
            # send_direct_message(submission.author.name, "[insert message here]")
        # if keyword.lower() in submission.selftext.lower():
        if submission.selftext.lower().find(keyword.lower()) != -1:
            print("The word " + keyword + " was used in the body of the post:")
            print(submission.selftext)
            # send_direct_message(submission.author.name, "[insert message here]")
        # submission.comments.replace_more(limit=None)
        # for comment in submission.comments.list():
    # if keyword.lower() in comment.body.lower():
    if comment.body.lower().find(keyword.lower()) != -1:
        print("The word " + keyword + " was used in a comment:")
        print(comment.body)
        # send_direct_message(comment.author.name, "[insert message here]")
