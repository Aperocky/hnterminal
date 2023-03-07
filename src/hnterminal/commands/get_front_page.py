import argparse
from replbuilder import ReplCommand
from urllib.parse import urlsplit
from time import strftime, localtime
from datetime import datetime


HN_STORY_LINER = "\033[1;33m{rank: <7}\033[0m| {title: <80} | {score: <5} | {comment: <7} | {age: <10} | {base_url}"
HN_STORY_TITLE = "\033[1;32m{rank: <7}| {title: <80} | {score: <5} | {comment: <7} | {age: <10} | {base_url}\033[0m"


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
    parser.add_argument('-p', '--page', type=int, default=0, help="Get the X page of HN stories")
    return parser


def print_story_line(rank, item):
    age = get_age_str(item["time"])
    base_url = "NONE"
    if "url" in item:
        base_url = urlsplit(item["url"]).netloc
    if item["type"] == "job":
        print(HN_STORY_LINER.format(rank=rank, title=item["title"], score="N/A", comment="N/A", age=age, base_url=base_url))
        return
    print(HN_STORY_LINER.format(rank=rank, title=item["title"], score=item["score"], comment=item["descendants"], age=age, base_url=base_url))


def get_front_page(args, context):
    context.clear_pointers()
    context.get_story_list(args.type)
    page = args.page
    if page > 10:
        raise ValueError("Not going that far back")
    stories_of_interest = context.story_list[page*30:(page+1)*30]
    print(HN_STORY_TITLE.format(rank="POINTER", title="TITLE", score="SCORE", comment="COMMENT", age="AGE", base_url="BASE URL"))
    rank = 0
    for story_id in stories_of_interest:
        rank += 1
        context.store_item(story_id)
        print_story_line(rank, context.loaded_items[story_id])
        context.store_pointer(rank, story_id)


get_front_page_command = ReplCommand("get_front_page", get_front_page_parser(), get_front_page, "Get the front page of Hacker News", use_context=True)
