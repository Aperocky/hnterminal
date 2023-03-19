from urllib import request
import json
import html


class HNClient:

    HN_FIREBASE_URL = "https://hacker-news.firebaseio.com/v0/"
    STORY_TYPES = {
        "TOP": "topstories.json",
        "NEW": "newstories.json",
        "ASK": "askstories.json",
        "JOB": "jobstories.json",
        "SHOW": "showstories.json",
    }

    def get_stories(self, story_type="TOP"):
        if story_type not in HNClient.STORY_TYPES:
            raise ValueError("Story type must be one of {}".format(list(HNClient.STORY_TYPES.keys())))
        request_url = HNClient.HN_FIREBASE_URL + HNClient.STORY_TYPES[story_type]
        stories = json.loads(request.urlopen(request_url).read())
        return stories

    def get_item(self, item_id):
        request_url = HNClient.HN_FIREBASE_URL + "item/{}.json".format(item_id)
        item_info = json.loads(request.urlopen(request_url).read())
        return item_info

    def get_user(self, author_name):
        request_url = HNClient.HN_FIREBASE_URL + "user/{}.json".format(author_name)
        author_info = json.loads(request.urlopen(request_url).read())
        return author_info

