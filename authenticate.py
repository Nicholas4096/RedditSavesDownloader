import praw
import random
import socket
import configparser

# Read config.ini
config = configparser.ConfigParser()
config.read("config.ini")


# Socket used to receive refresh key
def recv_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 8080))
        server.listen(1)
        client = server.accept()[0]
    return client


# Checks if a refresh token is currently stored in config.ini
def is_token():
    options = config.options("APP")
    if "token" not in options:
        return False
    else:
        return True


# Authenticates with OAuth server using Reddit App credentials, and receives a refresh key
def get_token():
    with praw.Reddit(
            client_id=config["APP"]["CLIENT_ID"],
            client_secret=config["APP"]["SECRET"],
            redirect_uri=config["APP"]["URI"],
            user_agent=config["APP"]["AGENT"]
    ) as me:
        state = random.randint(0, 65000)
        scope = ["read", "identity", "history"]
        url = me.auth.url(scope, state, "permanent")
        print("Open the URL below and click 'allow'\n")
        print("This script will have no access to your Reddit password.\n")
        print(url)
        client = recv_connection()
        data = client.recv(1024).decode("utf-8")
        param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
        params = {
            key: value for (key, value) in [token.split("=") for token in param_tokens]
        }

        refresh = me.auth.authorize(params["code"])

    config["APP"]["TOKEN"] = refresh

    with open("config.ini", "a") as configfile:
        configfile.write(f"TOKEN = {refresh}")
