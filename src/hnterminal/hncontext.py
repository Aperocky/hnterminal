import argparse
from .hnclient import HNClient
from replbuilder import ReplCommand


class HNContext:

    HN_BASE_URL = "https://news.ycombinator.com/"

    @staticmethod
    def get_link_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("pointer", nargs="?", type=int, help="Get link by pointer")
        return parser

    def __init__(self):
        self.client = HNClient()
        self.current_pointers = {}
        self.story_list = []
        self.stored_votes = {}
        self.loaded_items = {}
        self.call_count = 0
        self.link = None
        self.user_cookie = None

    def get_story_list(self, story_type="TOP"):
        self.call_count += 1
        self.story_list = self.client.get_stories(story_type=story_type)

    def store_item(self, item_id):
        if item_id in self.loaded_items:
            return
        self.call_count += 1
        item = self.client.get_item(item_id)
        if item is None:
            raise ValueError("Provided id does not exist")
        self.loaded_items[item_id] = item

    def drop_item(self, item_id):
        if item_id in self.loaded_items:
            self.loaded_items.pop(item_id)

    def get_user_info(self, author_name):
        return self.client.get_user(author_name)

    def store_link(self, link):
        self.link = link

    def store_vote(self, item_id, vote_type):
        if vote_type == "un":
            if item_id in self.stored_votes:
                self.stored_votes.pop(item_id)
            return
        self.stored_votes[item_id] = vote_type

    def get_link(self, args):
        if args.pointer:
            item_id = self.current_pointers[args.pointer]
            sub_link = "item?id={}".format(item_id)
            print("\033[4;35m{}\033[0m".format(HNContext.HN_BASE_URL + sub_link))
        elif self.link is None:
            print("No link stored yet")
        else:
            print("\033[4;35m{}\033[0m".format(HNContext.HN_BASE_URL + self.link))

    def store_pointer(self, index, item_id):
        self.current_pointers[index] = item_id

    def clear_pointers(self):
        self.current_pointers = {}

    def get_cache(self, args):
        print("LOADED ITEMS COUNT : {}".format(len(self.loaded_items)))
        print("TOTAL HN API CALLS : {}".format(self.call_count))
        print("POINTERS COUNT     : {}".format(len(self.current_pointers)))
        print("STORED VOTES       : {}".format(len(self.stored_votes)))

    def clear_cache(self, args):
        self.loaded_items = {}
        self.current_pointers = {}
        # stored votes remain true, no need to update
        # call count will continue to increment

    def store_user_cookie(self, user_cookie):
        self.user_cookie = user_cookie

    def get_context_commands(self):
        return [
            ReplCommand("get_link", HNContext.get_link_parser(), self.get_link, "Get the browser link from pointers or from last command"),
            ReplCommand("get_cache", argparse.ArgumentParser(), self.get_cache, "See stored item count and call count"),
            ReplCommand("clear_cache", argparse.ArgumentParser(), self.clear_cache, "Remove all cache"),
        ]
