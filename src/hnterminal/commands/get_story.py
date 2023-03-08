import argparse
from replbuilder import ReplCommand
from time import strftime, localtime
import html


def print_text(text):
    text = html.unescape(text)
    lines = text.split("<p>")
    for line in lines:
        print(line)
        print()


def get_story_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pointer', nargs="?", type=int, help="Get the story listed by rank")
    parser.add_argument('-i', '--story-id', type=int, help="Get the story listed by id, this must be provided if the pointer isn't")
    return parser


def print_story(story):
    print("\033[1;36m{}\033[0m".format(story["title"]))
    print(strftime('%Y-%m-%d %H:%M:%S', localtime(story["time"])))
    print("AUTHOR: {}".format(story["by"]))
    if "url" in story:
        print("FULL URL: \033[4;35m{}\033[0m".format(story["url"]))
    if "text" in story:
        print()
        print_text(story["text"])


def get_story(args, context):
    if args.pointer:
        story_id = context.current_pointers[args.pointer]
    elif args.story_id:
        story_id = args.story_id
    else:
        raise ValueError("Must either provide --pointer or --story-id")
    context.store_item(story_id)
    story = context.loaded_items[story_id]
    if story["type"] != "story":
        raise ValueError("Provided pointer or id is not a story")
    print_story(story)


get_story_command = ReplCommand("get_story", get_story_parser(), get_story, "Get story by pointer shown", use_context=True)
