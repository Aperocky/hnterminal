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

    def get_comment_tree(self, item_id, results={}, breadth=5, depth=5, limit=100, level=0):
        # DFS Search 
        # breadth: search only $breadth top rated direct comments
        # depth: search only $depth level commands
        # limit: only retrieve $limit commands
        print("loading comments with {} breadth, {} depth, and {} limit".format(breadth, depth, limit))
        if level > depth:
            return # Avoid back and forth comment chains
        item = self.get_item(item_id)
        if item["type"] == "comment":
            print(".", end="")
            results[item_id] = item
        if len(results) >= limit:
            return
        for kid_id in item["kids"][:breadth]:
            self.get_comment_tree(kid_id, breadth, limit, results, level+1)

