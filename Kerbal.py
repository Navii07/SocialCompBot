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
private_users = []

# TODO: When there are no users subscribed to the specified keywords, change the bot message

# Check comment stream for new requests and mentions
for comment in subreddit.stream.comments(skip_existing=True):
    # Add new keywords to user's subscription list
    if re.search("!sub", comment.body, re.IGNORECASE):
        # Keywords should be separated by commas
        # TODO: Handle lower/upper case keywords
        keywords = comment.body.replace("!sub ", "").split(", ")

        # Add keywords to user's subscription list
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

    # TODO: Set default privacy to private instead of public
    # Make users private on request
    elif re.search("!privateme", comment.body, re.IGNORECASE):
        if comment.author not in private_users:
            private_users.append(comment.author)

        # Have the bot reply to the comment confirming privacy setting changed
        comment.reply("*Beep Boop* \n\nYour profile is now private.")
        print(private_users)

    # Make users public on request
    elif re.search("!publicme", comment.body, re.IGNORECASE):
        if comment.author in private_users:
            private_users.remove(comment.author)

        # Have the bot reply to the comment confirming privacy setting changed
        comment.reply("*Beep Boop* \n\nYour profile is now public.")
        print(private_users)

    # List users who have subscribed to a certain keyword
    elif re.search("!findusers", comment.body, re.IGNORECASE):
        keywords = comment.body.replace("!findusers ", "").split(", ")

        users_per_keyword = {}
        for keyword in keywords:
            users_per_keyword[keyword] = []
            for user in subscription_dict:
                if user not in private_users and keyword in subscription_dict[user]:
                    users_per_keyword[keyword].append(user.name)

        # Have the bot reply to the comment with usernames
        # TODO: Move this to DMs and make it cleaner
        comment.reply("*Beep Boop* \n\nThese are the users I found:\n\n" + str(users_per_keyword))
        print(private_users)

    else:
        for user in subscription_dict:
            for keyword in subscription_dict[user]:
                if re.search(keyword, comment.body, re.IGNORECASE) and comment.author.name != user.name and comment.author.name != "Kerbal_Bot":
                    # Have the bot reply to the comment with an alert
                    comment.reply("*Beep Boop* \n\nYour keyword \"" + keyword
                                  + "\" was mentioned in a new comment by " + comment.author.name
                                  + ". Go check it out!\n\n" + comment.submission.url)

                    # user.message(
                    #     subject="Your keyword \"" + keyword + "\" was mentioned!",
                    #     message="Your keyword was mentioned in a new comment by " + comment.author.name
                    #             + ". Go check it out!\n\n" + comment.submission.url
                    # )

# TODO: Move everything into the same loop/function
# TODO: Add option to silence bot for a post because a keyword might be repeated on many comments
# Check new posts and comments for keywords
for submission in subreddit.stream.submissions(skip_existing=True):
    for user in subscription_dict:
        # TODO: Switch to a {keyword:users} dictionary instead of a {user:keywords} dictionary
        for keyword in subscription_dict[user]:
            if re.search(keyword, submission.title, re.IGNORECASE) and submission.author.name != user.name:
                # Have the bot reply to the comment with an alert
                comment.reply("*Beep Boop* \n\nYour keyword \"" + keyword
                              + "\" was mentioned in a new post. Go check it out!\n\n" + submission.url)

                # # TODO: This might not work as the bot won't be able to DM users since it is a new account
                # user.message(
                #     subject="Your keyword \"" + keyword + "\" was mentioned!",
                #     message="Your keyword was mentioned in a new post. Go check it out!\n\n" + submission.url
                # )
