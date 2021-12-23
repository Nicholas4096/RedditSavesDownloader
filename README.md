# RedditSavesDownloader
This script will download images and text posts that you have saved on your Reddit account, as well as create a HTML document with hyperlinks to the original posts.

In Reddit, posts that you find interesting, funny, or useful can be saved for later viewing. However, Reddit will start removing older items from your list after one thousand saves. With this script, you can download these posts for offline viewing. 

RedditSavesDownloader can simply print a list of posts in your saves, with title, date, subreddit, and URL of each post.

Or it can download images as a jpg/png/gif and save text posts to a .txt file.

This script does not download videos or images hosted by Imgur, but these features are planned for the future.


## Technologies:

* Python 3.6 or up

* PRAW 7.4.0 or up


## Getting Started:

Install PRAW (Python Reddit API Wrapper):

```bash
pip install praw
```

The next step is to register the app on Reddit. 

Go to https://www.reddit.com/prefs/apps/, and click “create an app…”

<img width="1439" alt="1" src="https://user-images.githubusercontent.com/3966361/147190306-c05293e3-aa54-4cd7-a171-562a27bf61fd.png">

Then select "script" from the list of options, name the script "SavesDownloader," and set the Redirect URI to "http://localhost:8080." It is important that the redirect URI is entered correctly, or the script will no be able to be authenticated with Reddit. Click "Create App."

<img width="887" alt="2" src="https://user-images.githubusercontent.com/3966361/147191031-4518fdcf-fd69-4510-ac49-d3ccc22cf724.png">

You will then see some information about your script. Save the Client ID (the string of text right under the name of the script) and the Client Secret. You will need to add these to the config.ini.

<img width="915" alt="3" src="https://user-images.githubusercontent.com/3966361/147193470-e470e0e7-9e66-4df6-b750-60c3dd6fbadb.png">

Open config.ini in any text editor and add the Client ID, Client Secret and Redirect URI to the config. Add "SavesDownloader" to the AGENT field.

<img width="910" alt="4" src="https://user-images.githubusercontent.com/3966361/147193482-72177c7d-5b63-45e5-8667-6e1cb4b124c2.png">

Almost done: run the script with:

```bash
python3 ./main.py
```

And a link will appear in the terminal, which will open a prompt on your Reddit account asking for you to allow "SavesDownloader" to connect to your Reddit account. Click "allow".

You can now return to the terminal and use the script!

* Display a list of posts you have saved:

<img width="877" alt="5" src="https://user-images.githubusercontent.com/3966361/147192558-8c8cb109-d1d1-4e28-a363-0230a9617267.png">

* Download posts to your device

<img width="1241" alt="6" src="https://user-images.githubusercontent.com/3966361/147193682-222eed44-47ec-4d8c-b5dd-9eebb9cf1677.png">



