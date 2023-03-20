import argparse
import os
from replbuilder import ReplCommand
from urllib.parse import urlsplit
from time import strftime, localtime
from datetime import datetime
from .votes import get_vote_stamp


HN_LINER_SHORT_TOP = "\033[1;33m{rank: <7} | {title}\033[0m"
HN_LINER_SHORT_BOTTOM = "{rank: <7} | \033[0;36m{author: <24}\033[0m | {score: <5} | {comment: <7} | {age: <10} | {base_url}"
HN_LINER_SHORT_TITLE = "\033[1;32m{rank: <7} | {author: <24} | {score: <5} | {comment: <7} | {age: <10} | {base_url}\033[0m"
HN_STORY_LINER = "\033[1;33m{rank: <7}\033[0m | {title: <80} | {score: <5} | {comment: <7} | {age: <10} | {author: <20} | {base_url}"
HN_STORY_LINER_VOTED = "\033[1;33m{rank: <7}\033[0m | {title: <91} | {score: <5} | {comment: <7} | {age: <10} | {author: <20} | {base_url}"
HN_STORY_TITLE = "\033[1;32m{rank: <7} | {title: <80} | {score: <5} | {comment: <7} | {age: <10} | {author: <20} | {base_url}\033[0m"


def get_age_str(timestamp):
    diff = int(datetime.now().timestamp() - timestamp)
    if diff < 300:
        return "just now"
    if diff < 3600:
        return "{} minutes".format(diff // 60)
    if diff < 86400:
        return "{} hours".format(diff // 3600)
    return "{} days".format(diff // 86400)


def get_front_page_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=str, default="TOP", help="HN Story types, default to TOP, also try ASK, NEW, SHOW, JOB")
    parser.add_argument('-s', '--start-index', type=int, default=0, help="Start from index, default to 0")
    parser.add_argument('-n', '--number', type=int, default=30, help="Get n number of stories, default to 30")
    return parser


def print_story_line(rank, item, width, vote=None):
    age = get_age_str(item["time"])
    base_url = "NONE"
    if "url" in item:
        base_url = urlsplit(item["url"]).netloc
    score = item["score"] if "score" in item else "N/A"
    comment = item["descendants"] if "descendants" in item else "N/A"
    author = item["by"]
    title = item["title"]
    if vote:
        title = "{} {}".format(title, get_vote_stamp(vote))
    if width >= 155:
        if vote:
            print(HN_STORY_LINER_VOTED.format(rank=rank, title=title, score=score, comment=comment, age=age, author=item["by"], base_url=base_url))
        else:
            print(HN_STORY_LINER.format(rank=rank, title=title, score=score, comment=comment, age=age, author=item["by"], base_url=base_url))
    else:
        print(HN_LINER_SHORT_TOP.format(rank=rank, title=title))
        print(HN_LINER_SHORT_BOTTOM.format(rank="", author=author, score=score, comment=comment, age=age, base_url=base_url))


def get_front_page(args, context):
    context.clear_pointers()
    context.get_story_list(args.type)
    stories_of_interest = context.story_list[args.start_index:args.start_index+args.number]
    sub_link = "" if args.type == "TOP" else args.type.lower()
    context.store_link(sub_link)

    width = os.get_terminal_size().columns
    if width >= 155:
        print(HN_STORY_TITLE.format(rank="POINTER", title="TITLE", score="SCORE", comment="COMMENT", age="AGE", author="AUTHOR", base_url="BASE URL"))
    else:
        print(HN_LINER_SHORT_TITLE.format(rank="POINTER", author="AUTHOR", score="SCORE", comment="COMMENT", age="AGE", base_url="BASE URL"))
    rank = 0
    for story_id in stories_of_interest:
        rank += 1
        context.store_item(story_id)
        vote = None
        if story_id in context.stored_votes:
            vote = context.stored_votes[story_id]
        print_story_line(rank, context.loaded_items[story_id], width, vote)
        context.store_pointer(rank, story_id)


get_front_page_command = ReplCommand("get_front_page", get_front_page_parser(), get_front_page, "Get the front page of Hacker News", use_context=True)
