import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="Print list of user's saved posts", action="store_true")
    parser.add_argument("-n", "--num", help="Set the number of posts to retrieve", type=int, default=10)
    parser.add_argument("-d", "--download", help="downloads image or text of saved post")
    args = parser.parse_args()
    return args
