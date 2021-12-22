import os
import datetime
import requests
import shutil
from arguments import *
from authenticate import *


# Returns a list of submissions from the accounts saved posts
def get_saved(num, me):
    print("Retrieving saved submissions...\n")
    postlist = []
    for post in me.saved(limit=num):
        if isinstance(post, praw.models.reddit.comment.Comment):
            continue
        else:
            postlist.append(post)
    return postlist


# Returns the date the supplied post was created in human-readable format
def get_date(post):
    post_date = post.created
    return datetime.datetime.fromtimestamp(post_date)


# Tests if the post is an image
def is_image(post):
    file_extension = post.url.split(".")[-1]
    image_formats = ("jpg", "jpeg", "png", "gif", "bmp")
    if file_extension in image_formats:
        return True
    else:
        return False


# Saves image from {post}.url to file {filename}
def save_image(post, filename):
    image = requests.get(post.url, stream=True)
    if image.status_code == 200:
        image.raw.decode_content = True
        with open(f"{filename}", "wb") as f:
            shutil.copyfileobj(image.raw, f)


# Saves the body of {post} to a .txt file {filename}
def save_text(post, filename):
    outfile = open(filename, "a")
    outfile.write(str(get_date(post)).split(" ")[0])
    outfile.write("\n")
    outfile.write(f"By u/{post.author} in r/{post.subreddit.display_name}")
    outfile.write("\n")
    outfile.write(post.url)
    outfile.write("\n" * 2)
    outfile.write(post.selftext)
    outfile.write("\n" * 3)
    outfile.close()


# Compiles a list of saved posts with date, URL, title, username and subreddit name, and writes to an HTML file in
# the original order they were saved
def save_to_html(postlist, loc):
    now = datetime.datetime.now()
    date_time = str(now.strftime('%m-%d-%y %H-%M-%S'))
    filename = "saves-" + date_time + ".html"
    with open(f"{loc}/{filename}", "a+") as outfile:
        outfile.write("<!DOCTYPE html>")
        outfile.write("<html>")
        outfile.write("<body>")
        for post in postlist:
            outfile.write(f"<h3>{get_date(post)}</h3>")
            outfile.write(f'<a href="https://www.reddit.com{post.permalink}">{post.title}</a> by u/{post.author} '
                          f'in r/{post.subreddit.display_name}')
            outfile.write(" " * 3)
        outfile.write("</body>")
        outfile.write("</html>")

    #outfile.close()


# Creates the necessary directories to save each post
def create_dirs(postlist, loc):
    os.makedirs(f"{loc}", exist_ok=True)
    os.chdir(f"{loc}")
    for post in postlist:
        sub = post.subreddit.display_name
        if sub not in os.listdir():
            if is_image(post) or post.is_self:
                os.mkdir(sub)


# Download all posts (images and text)
def download_all(postlist, loc):
    saved = 0
    posts_to_save = []

    for post in postlist:
        if is_image(post) or post.selftext:
            posts_to_save.append(post)

    os.chdir(f"{loc}")

    for post in posts_to_save:
        sub = post.subreddit.display_name
        title = str(post.title)
        if len(title) > 20:
            title = f"{title[:20]}..."
        img_extension = post.url.split("/")[-1]
        filename = f'{str(get_date(post)).split(" ")[0]}-{title}'

        filename = filename.replace("/", " ")

        if is_image(post):
            if str(f"{filename}{img_extension}") not in os.listdir(sub):
                print(f'Saving "{post.title}" from r/{sub} to {loc}')
                try:
                    save_image(post, f'{sub}/{str(filename)}{post.url.split("/")[-1]}')
                except requests.ConnectionError:
                    print(f"ERROR: Cannot download {post.title}")

                saved += 1
            else:
                pass

        elif post.selftext:
            if f'{filename}.txt' not in os.listdir(sub):
                print(f'Saving "{post.title}" from r/{sub} to {loc}')
                try:
                    save_text(post, f"{sub}/{filename}.txt")
                except requests.ConnectionError:
                    print(f"ERROR: Cannot download {post.title}")
                saved += 1
            else:
                pass

    print(f"\nSuccesfully saved {saved} posts to {loc}")


def main():
    if not is_token():
        get_token()
    else:
        pass

    # Create reddit instance
    reddit = praw.Reddit(client_id=config["APP"]["CLIENT_ID"],
                         client_secret=config["APP"]["SECRET"],
                         user_agent=config["APP"]["AGENT"],
                         refresh_token=config["APP"]["TOKEN"])

    # Instance of the current logged-in user
    me = reddit.user.me()

    args = get_args()

    if args.list:
        posts = get_saved(args.num, me)
        for post in posts:
            print(post.title)
            print(str(get_date(post)).split(" ")[0])
            print(post.url)
            print(f"r/{post.subreddit.display_name}\n")
    elif args.download:
        posts = get_saved(args.num, me)
        create_dirs(posts, args.download)
        download_all(posts, args.download)
        save_to_html(posts, args.download)


if __name__ == "__main__":
    main()
