import os
import re
import sys
import time
import html
import argparse
import tempfile
from subprocess import call
from urllib import parse
from http.client import HTTPSConnection
from bs4 import BeautifulSoup
from replbuilder import ReplCommand
from .votes import hn_get, get_pointer_parser


EDITOR = os.environ.get('EDITOR', 'vim')


def send_comment_request(form_data, user_cookie):
    headers = {"Cookie": user_cookie}
    data = parse.urlencode(form_data).encode()
    conn = HTTPSConnection("news.ycombinator.com")
    conn.request("POST", "/comment", data, headers=headers)
    resp = conn.getresponse()
    if str(resp.code).startswith("4"):
        print("Call REJECTED: {}".format(resp.read()))
        raise "Call is unsuccessful"
    conn.close()


def get_reply_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("pointer", type=int, help="Pointers from previous command")
    parser.add_argument("-s", "--comment", type=str, help="Your reply (comment) here as string, you can also choose to use editor")
    parser.add_argument("-e", "--editor", action="store_true", default=False, help="Use editor (e.g. vim) to edit the reply")
    return parser


def send_reply_form(item_id, text, context, is_story=True):
    if is_story:
        sub_link = "item?id={}".format(item_id)
    else:
        sub_link = "reply?id={}".format(item_id)
    reply_page = hn_get(sub_link, context.user_cookie)
    soup = BeautifulSoup(reply_page, "html.parser")
    comment_form = soup.select('form[action="comment"]')[0]
    hmac_element = comment_form.select('input[name="hmac"]')[0]
    hmac = hmac_element["value"]
    form_data = {
        "parent": item_id,
        "hmac": hmac,
        "text": text,
    }
    if is_story:
        form_data["goto"] = sub_link
    send_comment_request(form_data, context.user_cookie)
    print("\033[0;32mComment Published\033[0m")
    sys.stdout.flush()
    context.drop_item(item_id) # Parent will need to be reloaded


def editor_edit(item):
    if item["type"] == "comment":
        text = item["text"]
        text = html.unescape(text)
        text = text.replace("<p>", "\n")
    else:
        text = item["title"]
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write("YOU ARE REPLYING TO:\n\n".encode())
        tf.write(text.encode())
        tf.write("\n\n=== draft your reply below this line, do not delete this or above ===\n".encode())
        tf.flush()
        call([EDITOR, '+set backupcopy=yes', tf.name])
        edited_message = tf.read()
    return edited_message


def reply_to(args, context):
    if context.user_cookie is None:
        raise ValueError("Cannot reply if not logged in")
    item_id = context.current_pointers[args.pointer]
    context.store_item(item_id)
    item = context.loaded_items[item_id]
    comment_string = ""
    if args.editor:
        comment_string = editor_edit(item)
        print("\033[1;32mEDITOR OUTPUT:\033[0m")
        print(comment_string)
    elif args.comment:
        comment_string = args.comment
    else:
        raise ValueError("Reply must contain content")
    if item["type"] == "comment":
        send_reply_form(item_id, comment_string, context, False)
    else:
        send_reply_form(item_id, comment_string, context)


reply_to_command = ReplCommand("reply_to", get_reply_parser(), reply_to, "Reply to a story or a comment, can use editor of choice", use_context=True)
