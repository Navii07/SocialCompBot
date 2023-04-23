import re
import praw
import time

reddit = praw.Reddit(
    client_id='zRFmLVVtIrtotSAiwLQU0Q',
    client_secret='KQQgQEj87V7t4u4Ob9FYTscq1BdL6w',
    user_agent='Kerbal_Bot',
    username='Kerbal_Bot',
    password='pVzNkPER9JmFYAf'
)

subreddit = reddit.subreddit('neckbeardstestroom')

subscription_dict = {}
silence_dict = {}
public_users = []

# TODO: When multiple keywords are used in the same comment or title please only respond once


def checkComments():

    print("checking comments...")

    try:

        # Check comment stream for new requests and mentions
        for comment in subreddit.stream.comments(skip_existing=True, pause_after=3):

            # Add new keywords to user's subscription list
            b=time.perf_counter()
            if re.search("!sub", comment.body, re.IGNORECASE):
                # Keywords should be separated by commas
                keywords = comment.body.replace("!sub ", "").split(", ")
                print("!sub used")
                # Force all keywords to lower case
                keywords = [k.lower() for k in keywords]
                print(keywords)
                # Add keywords to user's subscription list
                for keyword in keywords:
                    if keyword not in subscription_dict:
                        subscription_dict[keyword] = str(comment.author)
                    else:
                        subscription_dict[keyword].append(str(comment.author))
                print(keywords)
                print(subscription_dict)
                
                # Have the bot reply to the comment confirming subscription
                # Creates a string that has all keywords separated by commas
                # Then prints full message with keywords
                keywords_string = ""
                for keyword in keywords:
                    keywords_string = keywords_string + ", " + keyword
                keywords_string = keywords_string.split(",")[1:]
                keywords_string = ", ".join(keywords_string)
                comment.reply("*Beep Boop* \n\nYou are now subscribed to keyword(s)" + keywords_string)
                # print(subscription_dict)

            # Remove keywords from a user's subscription list
            elif re.search("!unsub", comment.body, re.IGNORECASE):
                # Keywords should be separated by commas
                keywords = comment.body.replace("!unsub ", "").split(", ")

                # Force all keywords to lower case
                keywords = [k.lower() for k in keywords]

                # Remove keywords from user's subscription list
                for keyword in keywords:
                    if str(comment.author) in subscription_dict[keyword]:
                        subscription_dict[keyword].remove(str(comment.author))

                # Have the bot reply to the comment confirming unsubscription
                # Creates a string that has all keywords separated by commas
                # Then prints full message with keywords
                keywords_string = ""
                for keyword in keywords:
                    keywords_string = keywords_string + ", " + keyword
                keywords_string = keywords_string.split(",")[1:]
                keywords_string = ", ".join(keywords_string)
                comment.reply("*Beep Boop* \n\nYou are now unsubscribed from keyword(s)" + keywords_string)
                # print(subscription_dict)

            # Make users public on request
            elif re.search("!publicme", comment.body, re.IGNORECASE):
                if str(comment.author) not in public_users:
                    public_users.append(str(comment.author))

                # Have the bot reply to the comment confirming privacy setting changed
                comment.reply("*Beep Boop* \n\nYour profile is now public.")
                # print(public_users)

            # Make users private on request
            elif re.search("!privateme", comment.body, re.IGNORECASE):
                if str(comment.author) in public_users:
                    public_users.remove(str(comment.author))

                # Have the bot reply to the comment confirming privacy setting changed
                comment.reply("*Beep Boop* \n\nYour profile is now private.")
                # print(public_users)

            # List users who have subscribed to a certain keyword
            elif re.search("!findusers", comment.body, re.IGNORECASE):
                keywords = comment.body.replace("!findusers ", "").split(", ")

                # Force all keywords to lower case
                keywords = [k.lower() for k in keywords]

                users_per_keyword = {}
                for keyword in keywords:
                    users_per_keyword[keyword] = []
                    if keyword in subscription_dict:
                        if str(user) in public_users and str(user.name) in subscription_dict[keyword]:
                            users_per_keyword[keyword].append(str(user.name))

                # Have the bot reply to the comment with usernames
                # TODO: Move this to DMs and make it cleaner
                if str(users_per_keyword) != '[]':
                    comment.reply("*Beep Boop* \n\nThese are the users I found:\n\n" + str(users_per_keyword))
                else:
                    comment.reply("*Beep Boop* \n\nI found no users!")
                # print(public_users)
            elif re.search("!silence", comment.body, re.IGNORECASE):
                # Keywords should be separated by commas
                a = time.perf_counter()
                keywords = comment.body.replace("!sub ", "").split(", ")

                # Force all keywords to lower case
                keywords = [k.lower() for k in keywords]

                # Add keywords to user's subscription list
                if str(comment.author) not in silence_dict:
                    silence_dict[str(comment.author)] = keywords
                else:
                    for keyword in keywords:
                        if keyword not in silence_dict[str(comment.author)]:
                            silence_dict[str(comment.author)].append(keyword)

                # Have the bot reply to the comment confirming subscription
                # Creates a string that has all keywords separated by commas
                # Then prints full message with keywords
                keywords_string = ""
                for keyword in keywords:
                    keywords_string = keywords_string + ", " + keyword
                keywords_string = keywords_string.split(",")[1:]
                keywords_string = ", ".join(keywords_string)
                comment.reply("*Beep Boop* \n\nThe following keywords have been silenced for 24 hours: " + keywords_string)
                # print(subscription_dict)
            elif b-a >=86400:
                silence_dict.clear()
            else:
                for keyword in subscription_dict:
                    for user in subscription_dict[keyword]:
                        # comment.author.name != user.name and
                        if user not in silence_dict:
                            if re.search(keyword, comment.body, re.IGNORECASE) and comment.author.name != "Kerbal_Bot" and keyword not in silence_dict[user]:
                                # Have the bot reply to the comment with an alert
                                users_per_keyword = {}
                                users_per_keyword[keyword] = []
                                if user in public_users and user in subscription_dict[keyword]:
                                    users_per_keyword[keyword].append(user.name)
                                comment.reply("*Beep Boop* " + "Hi, " + str(users_per_keyword) + "!" + "\n\nYour keyword \"" + keyword
                                            + "\" was mentioned in a new comment by " + comment.author.name
                                            + ". Go check it out!\n\n" + comment.submission.url)
                            # print(public_users)
                                # user.message(
                                #     subject="Your keyword \"" + keyword + "\" was mentioned!",
                                #     message="Your keyword was mentioned in a new comment by " + comment.author.name
                                #             + ". Go check it out!\n\n" + comment.submission.url
                                # )
    except Exception as e:
        print("")

# TODO: Add option to silence bot for a post because a keyword might be repeated on many comments


def checkSubmissions():

    print("checking submissions...")
    try:
        # Check new posts and comments for keywords
        for submission in subreddit.new(limit=10):

            for keyword in subscription_dict:
                # TODO: Switch to a {keyword:users} dictionary instead of a {user:keywords} dictionary
                # print("checking user")
                for user in subscription_dict[keyword]:
                    # print("checking keyword")
                    # and submission.author.name != user.name
                    if user not in silence_dict:
                        if re.search(keyword, submission.title, re.IGNORECASE) and keyword not in silence_dict[user]:
                            # Have the bot reply to the comment with an alert
                            users_per_keyword = {}
                            users_per_keyword[keyword] = []
                            if user in public_users and user in subscription_dict[keyword]:
                                users_per_keyword[keyword].append(user.name)
                            reply_string = "*Beep Boop* " + "Hi, " + str(users_per_keyword) + "!" + "\n\nYour keyword " + keyword + " was mentioned in a new comment by " + comment.author.name + ". Go check it out!\n\n" + comment.submission.url
                            already_said = False

                            # For loop to make sure no comment is repeated for submissions
                            for comment in submission.comments:
                                if comment.body == reply_string:
                                    already_said = True
                                    break

                            if not already_said:
                                submission.reply(reply_string)

                        # print(public_users)

                            # # TODO: This might not work as the bot won't be able to DM users since it is a new account
                            # user.message(
                            #     subject="Your keyword \"" + keyword + "\" was mentioned!",
                            #     message="Your keyword was mentioned in a new post. Go check it out!\n\n" + submission.url
                        # )
    except Exception as e:
        print(f"Error in checkSubmissions(): {e}")
        print(traceback.format_exc())


while True:
    checkComments()
    checkSubmissions()
