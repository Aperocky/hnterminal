import argparse
import os
import html
import textwrap
from time import strftime, localtime
from replbuilder import ReplCommand
from .get_story import print_story
from .votes import get_vote_stamp


def get_comment_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pointer', nargs="?", type=int, help="Get comments tree under previous listed pointer")
    parser.add_argument('-b', '--breadth', type=int, default=5, help="How many direct replies to get for each level")
    parser.add_argument('-d', '--depth', type=int, default=5, help="Max depth of comment chain traversed")
    parser.add_argument('-l', '--limit', type=int, default=100, help="Max number of comments retrieved")
    parser.add_argument('-i', '--item-id', type=int, help="Get comments tree under a specific item-id. must be provided if pointer isn't")
    return parser


def get_comments(args, context):
    if args.pointer:
        item_id = context.current_pointers[args.pointer]
    elif args.item_id:
        item_id = args.item_id
    else:
        raise ValueError("Must either provide --pointer or --item-id")
    context.clear_pointers()
    context.curr_pointer = 1
    context.drop_item(item_id) # Reload parent object each time.
    context.store_item(item_id)
    context.store_link("item?id={}".format(item_id))
    item = context.loaded_items[item_id]
    vote = None
    if item_id in context.stored_votes:
        vote = context.stored_votes[item_id]
    if item["type"] == "comment":
        level = 0
        parent_id = item["parent"]
        context.store_item(parent_id)
        parent_item = context.loaded_items[parent_id]
        context.store_pointer(-1, parent_id)
        if parent_item["type"] == "comment":
            print("\033[1;32mPARENT COMMENT\033[0m")
            print_comment(-1, 0, parent_item, vote)
        else:
            print("\033[1;33mPOINTER -1: \033[1;32mPARENT STORY\033[0m")
            print_story(parent_item, vote)
    else:
        level = -1
        print("\033[1;33mPOINTER -1: \033[1;32mPARENT STORY\033[0m")
        print_story(item, vote)
        context.store_pointer(-1, item_id)
    print("\033[1;32m{pointer: <19} | {text}\033[0m".format(pointer="POINTER/AUTHOR", text="COMMENTS"))
    get_comment_tree(context, item_id, args.breadth, args.depth, args.limit, level)


def print_comment(pointer, level, item, vote=None):
    if "text" not in item:
        return
    comment = item["text"]
    comment = html.unescape(comment)
    comment = comment.replace("<i>", "\033[3m")
    comment = comment.replace("</i>", "\033[0m")
    comment_lines = comment.split("<p>")
    term_width = os.get_terminal_size().columns
    text_width = term_width - 30 - level * 5

    comment_lines_lines = [textwrap.wrap(l, text_width) for l in comment_lines]
    comment_lines = [l for subl in comment_lines_lines for l in subl]
    while len(comment_lines) < 3:
        comment_lines.append("")
    comment_time = strftime('%Y-%m-%d %H:%M:%S', localtime(item["time"]))
    pad = 19 + level * 6
    big_pad = pad
    if vote:
        pointer = "{} {}".format(pointer, get_vote_stamp(vote))
        big_pad += 11
    print("\033[1;33m{pointer: <{pad}}\033[0m | {text}".format(pointer=pointer, pad=big_pad, text=comment_lines[0]))
    print("\033[1;36m{author: <{pad}}\033[0m | {text}".format(author=item["by"], pad=pad, text=comment_lines[1]))
    print("{time: <{pad}} | {text}".format(time=comment_time, pad=pad, text=comment_lines[2]))
    for line in comment_lines[3:]:
        print(" "*(pad+1) + "| " + line)
    print()


def get_comment_tree(context, item_id, breadth=5, depth=5, limit=100, level=0):
    # DFS Search
    # breadth: search only $breadth top rated direct comments
    # depth: search only $depth level commands
    # limit: only retrieve $limit commands
    if level > depth or context.curr_pointer >= limit:
        return
    context.store_item(item_id)
    item = context.loaded_items[item_id]
    if item["type"] == "comment":
        vote = None
        if item_id in context.stored_votes:
            vote = context.stored_votes[item_id]
        print_comment(context.curr_pointer, level, item, vote)
        context.store_pointer(context.curr_pointer, item_id)
        context.curr_pointer += 1
    if "kids" in item:
        for kid_id in item["kids"][:breadth]:
            get_comment_tree(context, kid_id, breadth, depth, limit, level+1)


get_tree_command = ReplCommand("get_tree", get_comment_parser(), get_comments, "Get story, comments and their children by pointer, uses DFS to construct a comment tree, you have control over recusion parameters with breadth, depth and limit arguments", use_context=True)
