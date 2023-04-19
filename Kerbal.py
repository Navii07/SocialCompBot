import praw
import re

reddit = praw.Reddit(
    client_id='zRFmLVVtIrtotSAiwLQU0Q',
    client_secret='KQQgQEj87V7t4u4Ob9FYTscq1BdL6w',
    user_agent='Kerbal_Bot',
    username='Kerbal_Bot',
    password='pVzNkPER9JmFYAf'
)

subreddit = reddit.subreddit('neckbeardstestroom')

subscription_dict = {}
privacy_dict = {}

# Check comment stream for new (un)subscription requests
for comment in subreddit.stream.comments(skip_existing=True):
    # Add new keywords to user's subscription list
    if re.search("!sub", comment.body, re.IGNORECASE):
        # Keywords should be separated by commas
        # TODO: Handle lower/upper case keywords
        keywords = comment.body.replace("!sub ", "").split(", ")

        # Add keywords to user's subscription list
        # TODO: Should we limit the amount of subscriptions per user?
        if comment.author not in subscription_dict:
            subscription_dict[comment.author] = keywords
        else:
            for keyword in keywords:
                if keyword not in subscription_dict[comment.author]:
                    subscription_dict[comment.author].append(keyword)

        # Have the bot reply to the comment confirming subscription
        comment.reply("*Beep Boop* \n\nYou are now subscribed to the specified keywords!")
        print(subscription_dict)

    # Remove keywords from a user's subscription list
    elif re.search("!unsub", comment.body, re.IGNORECASE):
        # Keywords should be separated by commas
        keywords = comment.body.replace("!unsub ", "").split(", ")

        # Remove keywords from user's subscription list
        if comment.author in subscription_dict:
            for keyword in keywords:
                if keyword in subscription_dict[comment.author]:
                    subscription_dict[comment.author].remove(keyword)

        # Have the bot reply to the comment confirming subscription
        comment.reply("*Beep Boop* \n\nYou have unsubscribed from the specified keywords.")
        print(subscription_dict)


# TODO: Add option to silence bot for a post because a keyword might be repeated on many comments
# Check new posts and comments for keywords
for submission in subreddit.stream.submissions(skip_existing=True):
    for user in subscription_dict:
        # TODO: Do we want a {user:keywords} dictionary or a {keyword:users} dictionary?
        for keyword in subscription_dict[user]:
            if re.search(keyword, submission.title, re.IGNORECASE) and submission.author.name != user.name:
                # TODO: This might not work as the bot won't be able to DM users since it is a new account
                user.message(
                    subject="Your keyword \"" + keyword + "\" was mentioned!",
                    message="Your keyword was mentioned in a new post. Go check it out!\n\n" + submission.url
                )

for comment in subreddit.stream.comments(skip_existing=True):
    for user in subscription_dict:
        for keyword in subscription_dict[user]:
            if re.search(keyword, comment.body, re.IGNORECASE) and submission.author.name != user.name:
                user.message(
                    subject="Your keyword \"" + keyword + "\" was mentioned!",
                    message="Your keyword was mentioned in a new comment by " + comment.author.name
                            + ". Go check it out!\n\n" + comment.submission.url
                )
