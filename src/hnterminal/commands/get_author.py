import argparse
import textwrap
import html
from time import strftime, localtime
from replbuilder import ReplCommand
from .get_comments import print_comment


def get_author_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pointer', nargs="?", type=int, help="Get the comment belonging to previous listed pointer")
    parser.add_argument('-a', '--author-name', type=str, help="Get author by name, case sensitive, must be provided if pointer isn't")
    parser.add_argument('-s', '--show-submits', action="store_true", help="Show the most recent n submits belonging to this user")
    parser.add_argument('-n', '--number', type=int, default=5, help="Number of submits to show, default to 5")
    return parser


def print_about(text):
    text = html.unescape(text)
    text = text.replace("<i>", "")
    text = text.replace("</i>", "")
    lines = text.split("<p>")
    for line in lines:
        print("\033[3;33m{}\033[0m".format(line))
        print()


def print_story_with_pointer(pointer, story):
    story_lines = []
    story_lines.append("\033[1;36m{}\033[0m".format(story["title"]))
    story_lines.append(strftime('%Y-%m-%d %H:%M:%S', localtime(story["time"])))
    if "url" in story:
        story_lines.append("FULL URL: \033[4;35m{}\033[0m".format(story["url"]))
    print("\033[1;33m{pointer: <19}\033[0m | {text}".format(pointer=pointer, text=story_lines[0]))
    print("\033[1;36m{author: <19}\033[0m | {text}".format(author=story["by"], text=story_lines[1]))
    for line in story_lines[2:]:
        print(" "*20 + "| " + line)
    if "text" in story:
        text = story["text"]
        text = html.unescape(text)
        text = text.replace("<i>", "\033[3m")
        text = text.replace("</i>", "\033[0m")
        lines = text.split("<p>")
        text_width = os.get_terminal_size().columns - 30
        lines_lines = [textwrap.wrap(l, text_width) for l in lines]
        lines = [l for subl in lines_lines for l in subl]
        for line in lines:
            print(" "*20 + "| " + line)
    print()


def get_author(args, context):
    if not args.pointer and not args.author_name:
        raise ValueError("Must either provide --pointer or --item-id")
    if args.pointer:
        item_id = context.current_pointers[args.pointer]
        context.store_item(item_id)
        item = context.loaded_items[item_id]
        author_name = item["by"]
    else:
        author_name = args.author_name
    author_info = context.get_author_info(author_name)
    print("\033[1;36mUSER: {}\033[0m".format(author_name))
    if "about" in author_info:
        print_about(author_info["about"])
    print("TOTAL SUBMITS : {}".format(len(author_info["submitted"])))
    print("KARMA         : {}".format(author_info["karma"]))
    if args.show_submits:
        print("\033[1;32mDISPLAYING RECENT SUBMISSIONS\033[0m")
        print("\033[1;32m{pointer: <19} | {text}\033[0m".format(pointer="POINTER/AUTHOR", text="STORY/COMMENTS"))
        recent_items = author_info["submitted"][:args.number]
        context.clear_pointers()
        pointer = 0
        for item_id in recent_items:
            pointer += 1
            context.store_pointer(pointer, item_id)
            context.store_item(item_id)
            item = context.loaded_items[item_id]
            if ("dead" in item and item["dead"]) or ("deleted" in item and item["deleted"]):
                print()
                print("\033[1;31m{pointer: <19} | {text}\033[0m".format(pointer=pointer, text="DELETED"))
                print()
                continue
            if item["type"] == "comment":
                print_comment(pointer, 0, item)
            else:
                print_story_with_pointer(pointer, item)


get_author_command = ReplCommand("get_author", get_author_parser(), get_author, "Get the author by pointer or name, can also show recent submissions", use_context=True)
