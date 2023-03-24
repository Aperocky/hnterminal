import argparse
from replbuilder import ReplCommand
from time import strftime, localtime
from .votes import get_vote_stamp
import html


def print_text(text):
    text = html.unescape(text)
    text = text.replace("<i>", "\033[3m")
    text = text.replace("</i>", "\033[0m")
    lines = text.split("<p>")
    for line in lines:
        print(line)
        print()


def get_story_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pointer', nargs="?", type=int, help="Get the story listed by rank")
    parser.add_argument('-i', '--story-id', type=int, help="Get the story listed by id, this must be provided if the pointer isn't")
    return parser


def print_story(story, vote=None):
    print("\033[1;36m{}\033[0m".format(story["title"]))
    if vote:
        print(get_vote_stamp(vote))
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
    vote = None
    if story_id in context.stored_votes:
        vote = context.stored_votes[story_id]
    if story["type"] != "story":
        raise ValueError("Provided pointer or id is not a story")
    context.store_link("item?id={}".format(story_id))
    print_story(story, vote)


get_story_command = ReplCommand("get_story", get_story_parser(), get_story, "Get story by pointer shown, use get_tree instead if you also want to see comments", use_context=True)
