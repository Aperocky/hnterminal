import sys
import argparse
from http.client import HTTPSConnection
from bs4 import BeautifulSoup
from replbuilder import ReplCommand


def get_pointer_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("pointer", type=int, help="Pointers from previous command")
    return parser


def hn_get(path, user_cookie):
    if not path.startswith("/"):
        path = "/" + path
    headers = {"Cookie": user_cookie}
    conn = HTTPSConnection("news.ycombinator.com")
    conn.request("GET", path, headers=headers)
    resp = conn.getresponse()
    if str(resp.code).startswith("4"):
        print("Call REJECTED: {}".format(resp.read()))
        raise "Call is unsuccessful"
    result = resp.read()
    conn.close()
    return result


def get_vote_stamp(vote_type):
    # I VOTED!
    if vote_type == "up":
        return "\033[1;32m[UPVOTED]\033[0m"
    elif vote_type == "down":
        return "\033[1;31m[DOWNVOTED]\033[0m"
    elif vote_type == "un":
        return "\033[1m[UNVOTED]\033[0m"
    else:
        return ""


def vote(args, context, vote_type):
    if context.user_cookie is None:
        raise ValueError("Cannot upvote if not logged in")
    item_id = context.current_pointers[args.pointer]
    sub_link = "item?id={}".format(item_id)
    item_page = hn_get(sub_link, context.user_cookie)
    soup = BeautifulSoup(item_page, "html.parser")
    optional_link = soup.select("a#{}_{}".format(vote_type, item_id))
    if not optional_link:
        print("Link to {}vote does not exist".format(vote_type))
        return
    vote_link = optional_link[0]
    if "nosee" in vote_link["class"]:
        if item_id in context.stored_votes:
            if context.stored_votes[item_id] != vote_type:
                print("This item is already {}".format(get_vote_stamp(context.stored_votes[item_id])))
                return
        print("{}vote cannot be enacted, you may have already voted".format(vote_type))
        context.store_vote(item_id, vote_type)
        return
    vote_path = vote_link["href"]
    hn_get(vote_path, context.user_cookie)
    context.store_vote(item_id, vote_type)
    print("POINTER {} is {}".format(args.pointer, get_vote_stamp(vote_type)))
    sys.stdout.flush()


def upvote(args, context):
    vote(args, context, "up")


def downvote(args, context):
    vote(args, context, "down")


def unvote(args, context):
    vote(args, context, "un")


upvote_command = ReplCommand("upvote", get_pointer_parser(), upvote, "Upvote story or comment indicated by pointer from previous commands", use_context=True)
downvote_command = ReplCommand("downvote", get_pointer_parser(), downvote, "Downvote comment indicated by pointer from previous commands", use_context=True)
unvote_command = ReplCommand("unvote", get_pointer_parser(), unvote, "Unvote comment that you have previously up or downvoted", use_context=True)
