import time
import random
from instabot import Bot

comments_list = [
    "Great post!",
    "Nice shot!",
    "Love it!",
    "Awesome!",
    "Keep it up!",
    "Amazing!",
    "Fantastic!",
]

# Load Instagram account credentials from a file
def load_accounts(filename):
    accounts = []
    with open(filename, 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            accounts.append((username, password))
    return accounts

# Function to validate a direct link to a post
def validate_direct_link(link):
    return link.startswith("https://www.instagram.com/p/")

# Function to validate a username
def validate_username(username):
    return len(username) >= 4

# Function to validate post content
def validate_post_content(content):
    return bool(content.strip())

# Function to ask the user whether to like a post
def ask_to_like_post():
    while True:
        like_post = input("Do you want to like this post? (yes/no): ").strip().lower()
        if like_post in ["yes", "no"]:
            return like_post == "yes"
        else:
            print("Please enter 'yes' or 'no'.")

# Function to post an image to your Instagram story
def post_image_to_story(bot, image_path):
    try:
        bot.upload_story_photo(image_path)
    except Exception as e:
        print(f"An error occurred while posting to the story: {str(e)}")

# Function to ask the user whether to follow the user
def ask_to_follow_user():
    while True:
        follow_user = input("Do you want to follow this user? (yes/no): ").strip().lower()
        if follow_user in ["yes", "no"]:
            return follow_user == "yes"
        else:
            print("Please enter 'yes' or 'no'.")

# Function to perform Instagram actions
def perform_actions(username, password):
    # Create an Instabot instance
    bot = Bot()

    try:
        # Login to the Instagram account
        bot.login(username=username, password=password)

        # Prompt user for input
        direct_link = input("Enter a direct link to a post: ")
        if not validate_direct_link(direct_link):
            print("Invalid direct link. Please provide a valid Instagram post link.")
            return

        # Fetch the media ID from the direct link
        media_id = bot.get_media_id_from_link(direct_link)
        if not media_id:
            print("Invalid post link. Please make sure the link is correct.")
            return

        # Convert media_id to a string
        media_id_str = str(media_id)

        # Display US shoe size based on user input
        shoe_size = input("Enter your shoe size (US): ")
        if shoe_size.isdigit():
            comment = f"US {shoe_size}"
            bot.comment(media_id_str, comment)

        # Ask the user if they want to like the post
        if ask_to_like_post():
            bot.like(media_id_str)

        # Ask the user if they want to follow the user
        if ask_to_follow_user():
            # Get the post's owner username
            post_info = bot.get_media_info(media_id_str)
            if post_info and 'user' in post_info[0]:
                owner_username = post_info[0]['user']['username']
                bot.follow(owner_username)

            # Ask the user if they want to post an image to their story
            post_to_story = input("Do you want to post an image to your story? (yes/no): ").strip().lower()
            if post_to_story == "yes":
                image_path = input("Enter the path to the image you want to post: ").strip()
                post_image_to_story(bot, image_path)

    except Exception as e:
        print(f"An error occurred for account {username}: {str(e)}")

    finally:
        # Logout from the Instagram account
        bot.logout()

# Main program
if __name__ == "__main__":
    # Load Instagram accounts
    accounts = load_accounts("path to your txt file")

    # Iterate through accounts and perform actions for each account
    for username, password in accounts:
        # Perform actions for the current account
        perform_actions(username, password)

        # Random delay for commenting
        random_comment_delay = random.randint(60, 3600)  # Random delay between 1 minute and 1 hour
        time.sleep(random_comment_delay)
