import argparse
import os
import html
import textwrap
from replbuilder import ReplCommand


def get_comment_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pointer', type=int, help="Get the comment belonging to previous listed pointer")
    parser.add_argument('-i', '--item-id', type=int, help="Get the comment child of specific item id, you're responsible for finding the id yourself")
    parser.add_argument('-b', '--breadth', type=int, default=5, help="How many direct replies to get for each level")
    parser.add_argument('-d', '--depth', type=int, default=5, help="Max depth of comment chain traversed")
    parser.add_argument('-l', '--limit', type=int, default=100, help="Max number of comments retrieved")
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
    context.store_item(item_id)
    item = context.loaded_items[item_id]
    if item["type"] == "comment":
        level = 0
    else:
        level = -1
    print("\033[1;32m{pointer: <19} | {text}\033[0m".format(pointer="POINTER/AUTHOR", text="COMMENTS"))
    get_comment_tree(context, item_id, args.breadth, args.depth, args.limit, level)


def print_comment(pointer, level, item):
    if "text" not in item:
        return
    comment = item["text"]
    comment = html.unescape(comment)
    comment_lines = comment.split("<p>")
    term_width = os.get_terminal_size().columns
    text_width = term_width - 30 - level * 5

    comment_lines_lines = [textwrap.wrap(l, text_width) for l in comment_lines]
    comment_lines = [l for subl in comment_lines_lines for l in subl]
    if len(comment_lines) < 2:
        comment_lines.append("")
    pad = 19 + level * 6
    print("\033[1;33m{pointer: <{pad}}\033[0m | {text}".format(pointer=pointer, pad=pad, text=comment_lines[0]))
    print("\033[1;36m{author: <{pad}}\033[0m | {text}".format(author=item["by"], pad=pad, text=comment_lines[1]))
    for line in comment_lines[2:]:
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
        print_comment(context.curr_pointer, level, item)
        context.store_pointer(context.curr_pointer, item_id)
        context.curr_pointer += 1
    if "kids" in item:
        for kid_id in item["kids"][:breadth]:
            get_comment_tree(context, kid_id, breadth, depth, limit, level+1)


get_comments_command = ReplCommand("get_comments", get_comment_parser(), get_comments, "Get comments by pointer, works with both stories and comments", use_context=True)
